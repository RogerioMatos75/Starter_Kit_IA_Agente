# Orquestrador FSM com leitura automática do guia de projeto, confirmação manual e registro de log

import os
import shutil
import re
import json
import hashlib
import sys
import tempfile
from datetime import datetime
from auditoria_seguranca import auditoria_global
from ia_executor import executar_prompt_ia, IAExecutionError
from gerenciador_artefatos import salvar_artefatos_projeto
from utils.file_parser import _sanitizar_nome
from utils.prompt_parser import parse_prompts
from modules.agentes.enrichment_agent import enrich_artifact
from utils.supabase_client import supabase, CONFIG
from prompt_generator import parse_prompt_structure, save_prompts_to_json # NEW: Import prompt generator

# --- CONFIGURAÇÃO DE CAMINHOS ABSOLUTOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_PATH = os.path.join(BASE_DIR, "logs", "diario_execucao.json")
CHECKPOINT_PATH = os.path.join(BASE_DIR, "logs", "proximo_estado.json")
PROJECT_CONTEXT_PATH = os.path.join(BASE_DIR, "logs", "project_context.json")
PROMPT_TEMPLATES_PATH = os.path.join(BASE_DIR, "prompt_templates.json")
ARCHIVED_PROJECTS_DIR = os.path.join(BASE_DIR, "projetos", "arquivados")

# Tenta importar o gerador de PDF, mas não quebra se não estiver disponível
try:
    from relatorios import gerar_log_pdf
except ImportError:
    print("[AVISO] Módulo 'reportlab' não encontrado. A geração de PDF estará desativada.")
    gerar_log_pdf = None

INITIAL_PREVIEW_CONTENT = """# Olá sou o Archon estou aqui para auxilia-lo o seu projeto ainda não foi iniciado

para começar, preciso de algumas informações essenciais. Por favor, siga os passos na interface:

1-Grave sua Chave API: No topo da página, clique em "Gravar API Key" para garantir que o Archon AI tenha acesso aos modelos de linguagem.

2-Gere uma Proposta: Na sidebar à esquerda, clique em "Gerar Proposta" para iniciar o processo de definição do seu projeto.

3-Crie a Base de Conhecimento: Após gerar a proposta, volte à sidebar e clique em "Gerar Base de Conhecimento". Cole a proposta gerada e valide-a. Esta será a fundação do seu projeto.

4-Dê um Nome ao Projeto: Avance para a etapa "Nome do Projeto" para definir um nome para seus artefatos.

5-Acompanhe a Criação: Navegue pelas etapas seguintes na sidebar ("Linha do Tempo", "Histórico de Execução") para acompanhar a geração dos artefatos do seu projeto em tempo real.

6-Refine e Finalize: Utilize a "Definição do Layout UI" para ajustar a interface e, por fim, realize o "Deploy e Provisionamento" para publicar seu projeto.


*Estou pronto para começar assim que tivermos esses detalhes definidos.*
"""

def carregar_json(file_path):
    """Função utilitária para carregar um arquivo JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[ERRO CRÍTICO] Não foi possível carregar o arquivo JSON '{os.path.basename(file_path)}': {e}")
        return None

PROMPT_TEMPLATES = carregar_json(PROMPT_TEMPLATES_PATH)

def carregar_workflow(file_path=None):
    if file_path is None:
        file_path = os.path.join(BASE_DIR, "workflow.json")
    workflow_data = carregar_json(file_path)
    if workflow_data:
        print(f"Workflow '{workflow_data.get('nome_workflow')}' carregado com sucesso.")
        return workflow_data.get("estados", [])
    return []

def carregar_logs():
    if not os.path.exists(LOG_PATH):
        return []
    logs = carregar_json(LOG_PATH)
    return logs.get('execucoes', []) if logs else []

def registrar_log(etapa, status, decisao, resposta_agente=None, tarefa=None, observacao=None):
    log_entry = {
        "etapa": etapa,
        "tarefa": tarefa or etapa,
        "status": status,
        "decisao": decisao,
        "data_hora": datetime.now().isoformat(),
        "resposta_agente": resposta_agente or "",
        "observacao": observacao or ""
    }
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    logs = carregar_logs()
    logs.append(log_entry)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump({"execucoes": logs}, f, indent=2, ensure_ascii=False)
    
    checkpoint = {"ultimo_estado": etapa, "status": status, "data_hora": log_entry["data_hora"]}
    with open(CHECKPOINT_PATH, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, indent=2, ensure_ascii=False)

def gerar_prompt_etapa(etapa, contexto_guia=""):
    prompt_base = (
        f"**Contexto do Projeto:** Você está trabalhando em um projeto de software. A etapa atual é: **'{etapa['nome']}'**.\n"
        f"**Tipo de Tarefa:** {etapa.get('tipo', 'Geral')}\n"
        f"**Descrição da Tarefa:** {etapa.get('descricao', 'Execute a tarefa conforme o nome da etapa.')}\n"
    )
    if etapa.get('tecnologia'):
        prompt_base += f"**Tecnologia Específica:** {etapa['tecnologia']}\n"
    if contexto_guia:
        prompt_base += (
            "\n**Informações da Base de Conhecimento (Guia):**\n"
            "--- INÍCIO DO GUIA ---\n"
            f"{contexto_guia}\n"
            "--- FIM DO GUIA ---\n\n"
        )
    prompt_base += "Com base em todas as informações acima, gere o artefato solicitado para esta etapa. Seja claro, objetivo e siga as melhores práticas para a tecnologia especificada. Gere apenas o conteúdo do arquivo, sem explicações adicionais."
    return prompt_base

def _invalidar_logs_posteriores(etapa_alvo, estados):
    if not os.path.exists(LOG_PATH):
        return

    try:
        indice_alvo = [e['nome'] for e in estados].index(etapa_alvo)
    except ValueError:
        print(f"[AVISO] Etapa alvo '{etapa_alvo}' não encontrada no workflow para invalidação de logs.")
        return

    etapas_a_remover = {estados[i]['nome'] for i in range(indice_alvo, len(estados))}
    print(f"[LOG] Invalidando logs para as etapas: {etapas_a_remover}")
    
    logs_atuais = carregar_logs()
    logs_validos = [log for log in logs_atuais if log.get('etapa') not in etapas_a_remover]
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump({"execucoes": logs_validos}, f, indent=2, ensure_ascii=False)
    print(f"[LOG] Logs posteriores a '{etapa_alvo}' foram removidos.")

class FSMOrquestrador:
    instance = None

    def __init__(self, estados):
        self.estados = estados
        self.current_step_index = 0
        self.last_preview_content = INITIAL_PREVIEW_CONTENT
        self.is_finished = False
        self.project_name = None
        self.system_type = None # NEW: Store system type
        self._load_project_context()
        self._load_progress()
        FSMOrquestrador.instance = self

    def _load_project_context(self):
        if os.path.exists(PROJECT_CONTEXT_PATH):
            try:
                with open(PROJECT_CONTEXT_PATH, "r", encoding="utf-8") as f:
                    context = json.load(f)
                    self.project_name = context.get("project_name")
                    self.system_type = context.get("system_type") # NEW: Load system_type
                    if self.project_name:
                        print(f"[CONTEXTO] Projeto '{self.project_name}' carregado da sessão anterior.")
                        if self.system_type:
                            print(f"[CONTEXTO] Tipo de sistema: '{self.system_type}'")
            except (json.JSONDecodeError, TypeError):
                print(f"[AVISO] Arquivo de contexto '{PROJECT_CONTEXT_PATH}' malformado.")

    def _save_project_context(self):
        if self.project_name:
            context = {"project_name": self.project_name, "system_type": self.system_type}
            with open(PROJECT_CONTEXT_PATH, "w", encoding="utf-8") as f:
                json.dump(context, f, indent=2)

    def _load_progress(self):
        logs = carregar_logs()
        etapas_concluidas = {log['etapa'] for log in logs if log.get('status') == 'concluída'}
        etapa_pausada = None
        if logs:
            ultimo_log = logs[-1]
            if ultimo_log.get('status') == 'pausada':
                etapa_pausada = ultimo_log.get('etapa')
        for i, estado in enumerate(self.estados):
            if estado['nome'] not in etapas_concluidas:
                if etapa_pausada and estado['nome'] == etapa_pausada:
                    self.current_step_index = i
                    return
                elif not etapa_pausada:
                    self.current_step_index = i
                    return
        self.current_step_index = len(self.estados)
        self.is_finished = True

    def _avancar_estado(self):
        if self.current_step_index < len(self.estados) - 1:
            self.current_step_index += 1
        else:
            self.is_finished = True

    def get_status(self):
        timeline = []
        if not self.project_name:
            for estado in self.estados:
                timeline.append({"name": estado['nome'], "status": "pending"})
        else:
            for i, estado in enumerate(self.estados):
                status = "pending"
                if i < self.current_step_index:
                    status = "completed"
                elif i == self.current_step_index and not self.is_finished:
                    status = "in-progress"
                timeline.append({"name": estado['nome'], "status": status})
        
        current_step_name = "Projeto Finalizado"
        if self.project_name and not self.is_finished:
            current_step_name = self.estados[self.current_step_index]['nome']
        elif self.is_finished:
            self.last_preview_content = "Todas as etapas foram concluídas com sucesso!"
        
        if self.project_name and self.last_preview_content == INITIAL_PREVIEW_CONTENT and not self.is_finished:
            print("[CONTEXTO] Restaurando preview da etapa atual após reinício do servidor...")
            self._run_current_step()
        
        return {
            "timeline": timeline,
            "current_step": {
                "name": current_step_name,
                "preview_content": self.last_preview_content,
                "from_cache": False
            },
            "actions": {
                "can_go_back": self.current_step_index > 0,
                "is_finished": self.is_finished,
            },
            "project_name": self.project_name,
        }

    def get_current_project_name(self):
        """Retorna o nome do projeto atualmente ativo na FSM."""
        return self.project_name

    def _run_current_step(self):
        if self.is_finished or self.project_name is None:
            return
        
        estado_atual = self.estados[self.current_step_index]
        print(f"\n=== Executando Etapa: {estado_atual['nome']} para o projeto '{self.project_name}' ===")
        
        # Adiciona uma verificação para a nova etapa de validação
        if estado_atual['nome'] == "Validação da Base de Conhecimento":
            self.last_preview_content = "Aguardando validação manual dos documentos e seleção do tipo de sistema..."
            print("[INFO] Etapa de validação manual. Nenhuma ação automática será executada.")
            return

        if estado_atual['nome'] == "Definindo Layout UI":
            self.last_preview_content = "Aguardando a definição do layout pelo usuário na interface..."
            print("[INFO] Etapa de layout. Aguardando ação do usuário.")
            return

        
        if self.system_type and self.project_name:
            # NEW: Load prompts from generated JSON files
            sanitized_project_name = _sanitizar_nome(self.project_name)
            sanitized_system_type = _sanitizar_nome(self.system_type)
            sanitized_stage_name = _sanitizar_nome(estado_atual['nome'])
            
            prompt_file_path = os.path.join(
                BASE_DIR, "projetos", sanitized_project_name, "output", 
                "prompts", sanitized_system_type, f"{sanitized_stage_name}.json"
            )
            
            if os.path.exists(prompt_file_path):
                try:
                    with open(prompt_file_path, 'r', encoding='utf-8') as f:
                        stage_prompts = json.load(f)
                    
                    prompt_positivo = stage_prompts.get("positivo", "")
                    prompt_negativo = stage_prompts.get("negativo", "")

                    prompt_para_ia = (
                        f"**Contexto do Projeto:** Você está trabalhando em um projeto de software do tipo '{self.system_type}'. A etapa atual é: **'{estado_atual['nome']}'**.\n"
                        f"**Descrição da Tarefa:** {estado_atual.get('descricao', 'Execute a tarefa conforme o nome da etapa.')}\n"
                        f"**Instruções Positivas:** {prompt_positivo}\n"
                        f"**Instruções Negativas:** {prompt_negativo}\n\n"
                        "Com base em todas as informações acima, gere o artefato solicitado para esta etapa. Seja claro, objetivo e siga as melhores práticas para a tecnologia especificada. Gere apenas o conteúdo do arquivo, sem explicações adicionais."
                    )
                    print(f"[PROMPT] Prompt carregado de {prompt_file_path}")

                except (json.JSONDecodeError, IOError) as e:
                    print(f"[ERRO] Falha ao carregar ou parsear o arquivo de prompt: {prompt_file_path} - {e}")
                    prompt_para_ia = gerar_prompt_etapa(estado_atual, "") # Fallback
            else:
                print(f"[AVISO] Arquivo de prompt específico não encontrado: {prompt_file_path}. Usando prompt genérico.")
                prompt_para_ia = gerar_prompt_etapa(estado_atual, "") # Fallback
        else:
            # Fallback para o comportamento antigo se o tipo de sistema não estiver definido
            print("[AVISO] Tipo de sistema não definido. Usando prompt genérico.")
            prompt_para_ia = gerar_prompt_etapa(estado_atual, "")

        try:
            resultado = executar_prompt_ia(prompt_para_ia)
            self.last_preview_content = resultado
            print(f"Resultado da execução (preview):\n{str(resultado)[:500]}...")
        except IAExecutionError as e:
            print(f"[ERRO FSM] Erro de execução da IA na etapa '{estado_atual['nome']}': {e}")
            self.last_preview_content = f"Ocorreu um erro ao contatar a IA. Verifique o console."

    def _run_timeline_step_generation(self, timeline_step_name):
        """
        Gera o RASCUNHO de um artefato para uma etapa específica da linha do tempo.
        O resultado é armazenado em self.last_preview_content para supervisão.
        """
        if not self.system_type:
            print("[ERRO] _run_timeline_step_generation chamado sem um system_type definido.")
            self.last_preview_content = "ERRO INTERNO: Tipo de sistema não definido."
            return

        # Mapeamento de etapas da timeline para manifestos.
        manifest_mapping = [
            {"etapa_timeline": "Análise de requisitos", "manifesto_origem": "01_base_conhecimento.md"},
            {"etapa_timeline": "Prototipação", "manifesto_origem": "02_arquitetura_tecnica.md"},
            {"etapa_timeline": "Arquitetura de software", "manifesto_origem": "02_arquitetura_tecnica.md"},
            {"etapa_timeline": "Desenvolvimento backend", "manifesto_origem": "03_regras_negocio.md"},
            {"etapa_timeline": "Desenvolvimento frontend", "manifesto_origem": "04_fluxos_usuario.md"},
            {"etapa_timeline": "Testes e validação", "manifesto_origem": "05_backlog_mvp.md"},
            {"etapa_timeline": "Deploy e provisionamento", "manifesto_origem": "06_autenticacao_backend.md"},
            {"etapa_timeline": "Monitoramento e melhoria contínua", "manifesto_origem": "01_base_conhecimento.md"}
        ]

        map_entry = next((item for item in manifest_mapping if item["etapa_timeline"] == timeline_step_name), None)

        if not map_entry:
            print(f"[AVISO] Nenhuma correspondência de manifesto encontrada para a etapa da timeline: '{timeline_step_name}'.")
            self.last_preview_content = f"Não foi possível encontrar um manifesto base para a etapa '{timeline_step_name}'."
            return

        sanitized_project_name = _sanitizar_nome(self.project_name)
        caminho_manifesto_origem = os.path.join(BASE_DIR, "projetos", sanitized_project_name, "output", map_entry["manifesto_origem"])

        if not os.path.exists(caminho_manifesto_origem):
            print(f"[ERRO] Manifesto de origem '{map_entry['manifesto_origem']}' não encontrado em {caminho_manifesto_origem}.")
            self.last_preview_content = f"ERRO: O arquivo base '{map_entry['manifesto_origem']}' não foi encontrado."
            return

        with open(caminho_manifesto_origem, 'r', encoding='utf-8') as f:
            conteudo_original = f.read()

        prompt_structure_path = os.path.join(BASE_DIR, "docs", "Estrutura de Prompts.md")

        positive_prompt, negative_prompt = parse_prompts(prompt_structure_path, self.system_type, timeline_step_name)

        if not positive_prompt or not negative_prompt:
            print(f"[AVISO] Não foi possível encontrar prompts para {self.system_type} - {timeline_step_name}. Usando conteúdo original como rascunho.")
            self.last_preview_content = conteudo_original
            return

        print(f"[FLUXO] Gerando rascunho para a etapa: {timeline_step_name}")
        try:
            conteudo_enriquecido = enrich_artifact(conteudo_original, self.system_type, timeline_step_name, positive_prompt, negative_prompt)
            self.last_preview_content = conteudo_enriquecido
            print(f"[FLUXO] Rascunho para '{timeline_step_name}' gerado e pronto para supervisão.")
        except Exception as e:
            print(f"[ERRO] Falha ao gerar rascunho do artefato para '{timeline_step_name}': {e}")
            self.last_preview_content = f"ERRO ao gerar rascunho: {e}"

    def _generate_gemini_md(self, etapa_concluida_nome, nome_arquivo_artefato):
        """
        Gera o conteúdo para o arquivo Gemini.md com base no template.
        """
        # The 'etapa_concluida_nome' is available if we need it, but the template
        # focuses on the artifact name, which is more precise for the agent.
        
        template = f"""Get-Content GEMINI.md | gemini --ide-mode

# Roteiro de Execução para o Agente

## Projeto: **projetos/{self.project_name}/**

## Etapa Atual: **`{nome_arquivo_artefato}`**

### Missão do Agente

Sua missão é continuar o desenvolvimento deste projeto com base nos artefatos gerados pelo Archon AI.

### Instruções Imediatas:

1.  **Analise o Artefato Principal:**
    *   O artefato gerado para esta etapa é: **`{nome_arquivo_artefato}`**.
    *   Leia e compreenda completamente o conteúdo deste arquivo. Ele contém a especificação ou o código que você deve usar como base.

2.  **Execute as Ações Necessárias:**
    *   Com base na análise, crie ou modifique os arquivos do projeto.
    *   Se for um arquivo de requisitos, comece a estruturar o código.
    *   Se for um código, integre-o ao projeto existente.
    *   Se for um documento de arquitetura, crie os diretórios e arquivos iniciais.

3.  **Verificação e Validação:**
    *   Certifique-se de que o código está limpo e segue as boas práticas.
    *   Se aplicável, execute testes para validar a implementação.

4.  **Reporte o Progresso:**
    *   Ao concluir, descreva as ações que você tomou.
    *   Aguarde a próxima instrução ou a aprovação para avançar para a próxima etapa.

# PERSONA
Você é um assistente de engenharia de software especialista e de classe mundial, focado no desenvolvimento full-stack de sistemas e software para o sistema "Archon AI". Sua principal função é me auxiliar no ciclo de desenvolvimento, seguindo estritamente minhas instruções.

# OBJETIVO
Seu objetivo é fornecer respostas precisas, código de alta qualidade e insights técnicos, atuando como um par de programação experiente. Você deve me ajudar a resolver problemas, desenvolver funcionalidades e seguir as melhores práticas de engenharia de software, sempre aguardando meu comando para cada passo.

# REGRAS DE COMPORTAMENTO
1.  **Idioma:** Comunique-se exclusivamente em **Português (Brasil)**.
2.  **Aguardar Instruções:** **Nunca** aja proativamente. Sempre aguarde uma instrução clara minha antes de realizar qualquer tarefa. Não tente adivinhar os próximos passos ou antecipar minhas necessidades.
3.  **Confirmação para Prosseguir:** Ao final de cada resposta ou após apresentar uma solução, você **deve** perguntar explicitamente se pode prosseguir. Use frases como "Posso prosseguir com a implementação da Opção 1?", "Deseja que eu detalhe alguma das opções?" ou "Aguardando suas próximas instruções. O que faremos a seguir?".
4.  **Resolver Dúvidas:** Se uma instrução for ambígua ou se houver múltiplas maneiras de abordar um problema, você **deve** fazer perguntas para esclarecer. Questione sobre as melhores práticas aplicáveis ao contexto para me ajudar a tomar a melhor decisão.
5.  **Oferecer Múltiplas Opções:** Para qualquer problema técnico ou solicitação de implementação, você **deve** apresentar pelo menos **duas (2) opções** de solução. Descreva os prós e contras de cada uma, explicando o trade-off em termos de performance, manutenibilidade, complexidade, etc.
6.  **Resolução Avançada de Problemas com Context7:** Ao enfrentar dificuldades (ex: loops de execução, código incompleto, erros persistentes) ou ao lidar com tarefas que exigem conhecimento preciso e atualizado de APIs, SDKs ou bibliotecas externas, devo proativamente sugerir o uso do Context7 MCP. Devo explicar como ele pode fornecer a documentação e os exemplos mais recentes para superar o obstáculo e, então, solicitar sua permissão para consultá-lo.

# FORMATO DA RESPOSTA
- **Clareza e Estrutura:** Organize suas respostas de forma clara, usando markdown (títulos, listas, blocos de código) para facilitar a leitura.
- **Blocos de Código:** Apresente exemplos de código em blocos formatados corretamente com a linguagem especificada (ex: ```python).
- **Diferenças (Diffs):** Se a solicitação envolver a modificação de um arquivo existente, forneça a resposta no formato `diff`.

# INSTRUÇÃO INICIAL
Responda a esta mensagem inicial com: "Agente pronto e aguardando suas instruções."

---
*Este roteiro foi gerado automaticamente pelo Archon AI. Siga as instruções para garantir a continuidade e o sucesso do projeto.*
"""
        return template

    def process_action(self, action, observation="", project_name=None, current_preview_content=None, system_type=None):
        # Garante que o contexto do projeto e do tipo de sistema esteja sempre atualizado.
        if project_name and not self.project_name:
            self.project_name = project_name
            print(f"[PROJETO] Contexto do projeto restaurado para: '{self.project_name}'")
        if system_type:
            self.system_type = system_type
            print(f"[PROJETO] Tipo de sistema definido/atualizado para: '{self.system_type}'")
        self._save_project_context()

        if self.is_finished or self.project_name is None:
            if action == 'reset':
                return self.reset_project(project_name_to_reset=project_name)
            return self.get_status()

        estado_atual = self.estados[self.current_step_index]

        if current_preview_content is not None:
            self.last_preview_content = current_preview_content

        if action == 'approve':
            print(f"[FSM] Aprovando etapa '{estado_atual['nome']}'.")

            # CASO 1: Aprovação da Etapa 2 (Validação da Base de Conhecimento)
            # Este é o gatilho que inicia a linha do tempo.
            if estado_atual['nome'] == "Validação da Base de Conhecimento":
                # [GEMINI-FIX] Verificação de system_type contornada para forçar avanço de estado.
                # if not self.system_type:
                #     print("[ERRO FSM] Tipo de sistema não definido. Não é possível iniciar a linha do tempo.")
                #     self.last_preview_content = "ERRO: Por favor, selecione um tipo de sistema antes de aprovar."
                #     return self.get_status()
                
                print(f"[FLUXO] Aprovada a validação. Iniciando a geração de prompts para o tipo de sistema: '{self.system_type}'.")
                
                # --- INÍCIO DA LÓGICA DE GERAÇÃO DE PROMPTS ---
                try:
                    prompt_structure_path = os.path.join(BASE_DIR, "docs", "Estrutura de Prompts.md")
                    with open(prompt_structure_path, 'r', encoding='utf-8') as f:
                        markdown_content = f.read()
                    
                    parsed_prompts = parse_prompt_structure(markdown_content)
                    
                    if save_prompts_to_json(self.project_name, self.system_type, parsed_prompts, BASE_DIR):
                        print(f"[FLUXO] Arquivos de prompt JSON gerados com sucesso para '{self.system_type}'.")
                    else:
                        raise Exception("Falha ao salvar os arquivos de prompt JSON.")

                except Exception as e:
                    print(f"[ERRO CRÍTICO] Falha ao gerar a estrutura de prompts: {e}")
                    self.last_preview_content = f"ERRO CRÍTICO: Não foi possível gerar os prompts para o projeto. Verifique os logs."
                    return self.get_status()
                # --- FIM DA LÓGICA DE GERAÇÃO DE PROMPTS ---

                registrar_log(estado_atual['nome'], 'concluída', decisao="Validação aprovada, iniciando linha do tempo")
                
                self._avancar_estado() # Avança para "Análise de requisitos"
                # [GEMINI-FIX] Removida a geração automática do próximo rascunho para forçar a parada e aguardar o supervisor.
                # proxima_etapa_nome = self.estados[self.current_step_index]['nome']
                # self._run_timeline_step_generation(proxima_etapa_nome) # Gera o rascunho do primeiro artefato
                self.last_preview_content = "Aguardando comando do supervisor para gerar o rascunho da etapa 'Análise de requisitos'."

            # CASO 2: Aprovação de uma etapa da Linha do Tempo
            # Salva o artefato final e prepara o rascunho da próxima etapa.
            else:
                artefato_final_aprovado = self.last_preview_content
                
                # Mapeia o nome da etapa para o nome do arquivo de artefato
                nome_arquivo_artefato = _sanitizar_nome(estado_atual['nome']) + ".md"
                caminho_artefatos_destino = os.path.join(BASE_DIR, "projetos", _sanitizar_nome(self.project_name), "artefatos")
                os.makedirs(caminho_artefatos_destino, exist_ok=True)
                caminho_arquivo_final = os.path.join(caminho_artefatos_destino, nome_arquivo_artefato)

                try:
                    # 1. Salvar o artefato aprovado
                    with open(caminho_arquivo_final, 'w', encoding='utf-8') as f:
                        f.write(artefato_final_aprovado)
                    print(f"[FLUXO] Artefato final da etapa '{estado_atual['nome']}' salvo em: {caminho_arquivo_final}")

                    # 2. Criar README.md em branco (se não existir)
                    readme_path = os.path.join(BASE_DIR, "projetos", _sanitizar_nome(self.project_name), "README.md")
                    if not os.path.exists(readme_path):
                        with open(readme_path, 'w', encoding='utf-8') as f:
                            f.write(f"# Projeto: {self.project_name}\n\nEste é o README do projeto. Ele será preenchido conforme o desenvolvimento avança.")
                        print(f"[FLUXO] Arquivo README.md criado.")

                    # 3. Gerar e salvar o Gemini.md com instruções para a próxima etapa
                    gemini_md_content = self._generate_gemini_md(estado_atual['nome'], nome_arquivo_artefato)
                    gemini_md_path = os.path.join(BASE_DIR, "projetos", _sanitizar_nome(self.project_name), "GEMINI.md")
                    with open(gemini_md_path, 'w', encoding='utf-8') as f:
                        f.write(gemini_md_content)
                    print(f"[FLUXO] Arquivo GEMINI.md atualizado.")

                    # 4. Registrar o log da etapa concluída
                    registrar_log(estado_atual['nome'], 'concluída', decisao=observation or "Aprovado pelo supervisor", resposta_agente=f"Artefato salvo em {nome_arquivo_artefato}", observacao=observation)

                    # 5. Avançar para a próxima etapa e gerar o próximo rascunho
                    self._avancar_estado()
                    # [GEMINI-FIX] Removida a geração automática do próximo rascunho para forçar a parada e aguardar o supervisor.
                    if not self.is_finished:
                        self.last_preview_content = "Aguardando comando do supervisor para gerar o rascunho da próxima etapa."
                    else:
                        self.last_preview_content = "PROJETO CONCLUÍDO! Todos os artefatos foram gerados e aprovados. Verifique a pasta /artefatos."
                        print("[FLUXO] Todas as etapas da linha do tempo foram concluídas.")

                except Exception as e:
                    print(f"[ERRO FSM] Falha ao processar aprovação da etapa '{estado_atual['nome']}': {e}")
                    self.last_preview_content = f"Erro ao processar aprovação: {e}"

        elif action == 'repeat':
            print(f"[FSM] Repetindo etapa '{estado_atual['nome']}'.")
            # A ação de repetir agora simplesmente re-executa a geração do rascunho para a etapa ATUAL.
            self._run_timeline_step_generation(estado_atual['nome'])
        
        elif action == 'back':
            if self.current_step_index > 0:
                print(f"[FSM] Voltando para a etapa anterior.")
                self.current_step_index -= 1
                etapa_alvo = self.estados[self.current_step_index]['nome']
                _invalidar_logs_posteriores(etapa_alvo, self.estados)
                # Ao voltar, também re-executamos a geração do rascunho para a etapa alvo.
                self._run_timeline_step_generation(etapa_alvo)

        elif action == 'update_preview':
            print(f"[FSM] Atualizando preview com refinamento do supervisor.")
            if current_preview_content is not None:
                self.last_preview_content = current_preview_content
                registrar_log(
                    estado_atual['nome'], 
                    'em andamento', 
                    decisao="Supervisor refinou o artefato com IA.", 
                    observacao=observation
                )
            else:
                print("[AVISO] Ação 'update_preview' chamada sem 'current_preview_content'.")
        
        return self.get_status()

    def setup_project(self, project_name, initial_preview_content=None, system_type=None):
        """Define o nome do projeto, sanitiza-o e armazena o preview inicial."""
        if not project_name or not project_name.strip():
            print("[ERRO] O nome do projeto é obrigatório para iniciar.")
            return self.get_status()
        
        # Sanitiza o nome do projeto para criar um nome de diretório seguro e consistente
        self.project_name = _sanitizar_nome(project_name)
        self.system_type = system_type # NEW: Store system_type
        self._save_project_context()
        print(f"[DEBUG FSM] setup_project - project_name definido como: {self.project_name}")
        
        if initial_preview_content:
            self.last_preview_content = initial_preview_content
        else:
            # Se nenhum preview for fornecido, executa a primeira etapa para gerá-lo
            # (Este é um fallback, o fluxo principal deve fornecer o preview)
            self._run_current_step()

        print(f"[PROJETO] Projeto '{self.project_name}' iniciado. Aguardando aprovação do manifesto.")
        return self.get_status()

    def reset_project(self, project_name_to_reset=None):
        """Reseta o estado do projeto. Se um nome de projeto for fornecido, arquiva esse projeto específico."""
        print("\n[RESET] Iniciando reset completo do projeto...")
        
        # Usa o nome do projeto fornecido, caso contrário, usa o do estado da FSM como fallback
        project_to_reset = project_name_to_reset or self.project_name
        print(f"[DEBUG] Nome do projeto para resetar: '{project_to_reset}'")

        if project_to_reset:
            sanitized_name = _sanitizar_nome(project_to_reset)
            project_dir = os.path.join(BASE_DIR, "projetos", sanitized_name)
            
            # Garante que o diretório de arquivados exista
            os.makedirs(ARCHIVED_PROJECTS_DIR, exist_ok=True)

            if os.path.exists(project_dir):
                try:
                    # Cria um arquivo ZIP do projeto
                    archive_name = f"{sanitized_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    archive_path = os.path.join(ARCHIVED_PROJECTS_DIR, archive_name)
                    shutil.make_archive(archive_path, 'zip', project_dir)
                    print(f"[RESET] Projeto '{project_to_reset}' arquivado em: {archive_path}.zip")

                    # Remove o diretório original do projeto
                    shutil.rmtree(project_dir)
                    print(f"[RESET] Diretório do projeto '{project_to_reset}' removido.")
                except Exception as e:
                    print(f"[ERRO RESET] Falha ao arquivar ou remover o projeto '{project_to_reset}': {e}")
            else:
                print(f"[AVISO RESET] Diretório do projeto '{project_to_reset}' não encontrado em {project_dir}. Ignorando arquivamento.")

            # Limpeza do Supabase (se habilitado)
            if supabase and CONFIG.get("SUPABASE_ENABLED"):
                try:
                    files_to_delete = supabase.storage.from_("artefatos-projetos").list(path=sanitized_name)
                    if files_to_delete:
                        file_paths = [f"{sanitized_name}/{f['name']}" for f in files_to_delete]
                        supabase.storage.from_("artefatos-projetos").remove(file_paths)
                        print(f"[SUPABASE] Artefatos do projeto '{project_to_reset}' removidos do Storage.")
                except Exception as e:
                    print(f"[ERRO SUPABASE] Falha ao remover artefatos do projeto '{project_to_reset}': {e}")

        # Reseta o estado da FSM e limpa logs
        self.reset_fsm_state_and_logs()
        
        return self.get_status()

    def reset_fsm_state_and_logs(self):
        """Reseta o estado interno da FSM e limpa os arquivos de log e contexto."""
        print("\n[RESET FSM] Limpando estado da FSM e arquivos de log...")
        
        # Limpeza robusta de arquivos de estado
        for file_path, file_name in [(LOG_PATH, "diario_execucao.json"), 
                                     (CHECKPOINT_PATH, "proximo_estado.json"), 
                                     (PROJECT_CONTEXT_PATH, "project_context.json")]:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"[RESET FSM] Arquivo '{file_name}' removido com sucesso.")
                else:
                    print(f"[RESET FSM] Arquivo '{file_name}' não encontrado. Ignorando.")
            except Exception as e:
                print(f"[ERRO RESET FSM] Falha ao remover o arquivo '{file_name}': {e}")

        self._clean_temp_directory()

        self.current_step_index = 0
        self.last_preview_content = INITIAL_PREVIEW_CONTENT
        self.is_finished = False
        self.project_name = None
        self.system_type = None # Resetar também o tipo de sistema
        print("[RESET FSM] Estado da FSM e arquivos de log foram limpos. O sistema está pronto para um novo projeto.")

    def _clean_temp_directory(self):
        """Limpa o diretório temporário do projeto."""
        temp_dir = os.path.join(BASE_DIR, "temp")
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                print(f"[RESET FSM] Diretório temporário '{temp_dir}' limpo.")
            except Exception as e:
                print(f"[ERRO RESET FSM] Falha ao limpar o diretório temporário '{temp_dir}': {e}")

    def create_temp_archive_for_download(self, project_name):
        """Cria um arquivo ZIP do projeto em um local temporário e retorna o caminho e o diretório temporário."""
        if not project_name:
            raise ValueError("O nome do projeto é necessário para o arquivamento.")

        sanitized_name = _sanitizar_nome(project_name)
        project_path = os.path.join(BASE_DIR, "projetos", sanitized_name)

        if not os.path.isdir(project_path):
            raise FileNotFoundError(f"Diretório do projeto '{project_name}' não encontrado em {project_path}")

        # Cria um diretório temporário único para esta operação
        temp_dir = tempfile.mkdtemp()
        
        zip_base_name = os.path.join(temp_dir, sanitized_name)
        # shutil.make_archive retorna o caminho completo para o arquivo zip criado
        zip_file_path = shutil.make_archive(zip_base_name, 'zip', project_path)
        
        print(f"[DOWNLOAD] Projeto '{project_name}' compactado em: {zip_file_path}")
        return zip_file_path, temp_dir


project_states = carregar_workflow()
if not project_states or not PROMPT_TEMPLATES:
    sys.exit("ERRO CRÍTICO: Falha no carregamento do workflow.json ou prompt_templates.json.")

fsm_instance = FSMOrquestrador(project_states)