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
from prompt_generator import parse_prompt_structure, save_prompts_to_json

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

1-Grave sua Chave API: No topo da página, clique em \"Gravar API Key\" para garantir que o Archon AI tenha acesso aos modelos de linguagem.
2-Gere uma Proposta: Na sidebar à esquerda, clique em \"Gerar Proposta\" para iniciar o processo de definição do seu projeto.
3-Crie a Base de Conhecimento: Após gerar a proposta, volte à sidebar e clique em \"Gerar Base de Conhecimento\". Cole a proposta gerada e valide-a. Esta será a fundação do seu projeto.
4-Dê um Nome ao Projeto: Avance para a etapa \"Nome do Projeto\" para definir um nome para seus artefatos.
5-Acompanhe a Criação: Navegue pelas etapas seguintes na sidebar (\"Linha do Tempo\", \"Histórico de Execução\") para acompanhar a geração dos artefatos do seu projeto em tempo real.
6-Refine e Finalize: Utilize a \"Definição do Layout UI\" para ajustar a interface e, por fim, realize o \"Deploy e Provisionamento\" para publicar seu projeto.

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
        self.system_type = None
        self._load_project_context()
        self._load_progress()
        FSMOrquestrador.instance = self

    def _load_project_context(self):
        if os.path.exists(PROJECT_CONTEXT_PATH):
            try:
                with open(PROJECT_CONTEXT_PATH, "r", encoding="utf-8") as f:
                    context = json.load(f)
                    self.project_name = context.get("project_name")
                    self.system_type = context.get("system_type")
                    if self.project_name:
                        print(f"[CONTEXTO] Projeto '{self.project_name}' carregado da sessão anterior.")
                        if self.system_type:
                            print(f"[CONTEXTO] Tipo de sistema: '{self.system_type}'")
            except (json.JSONDecodeError, TypeError):
                print(f"[AVISO] Arquivo de contexto '{PROJECT_CONTEXT_PATH}' malformado.")

    def _save_project_context(self):
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
                self.current_step_index = i
                if i == 0:
                    self.last_preview_content = "Aguardando a validação da proposta e a seleção do tipo de sistema para gerar a estrutura de prompts e iniciar o projeto."
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
        
        # Lógica Aprimorada: Verifica se a etapa atual é uma etapa de timeline
        is_current_step_on_timeline = False
        if not self.is_finished:
            current_fsm_step = self.estados[self.current_step_index]
            if current_fsm_step.get('tipo') == 'timeline_step':
                is_current_step_on_timeline = True

        for i, estado in enumerate(self.estados):
            if estado.get('tipo') != 'timeline_step':
                continue

            status = "pending"
            if i < self.current_step_index:
                status = "completed"
            elif i == self.current_step_index and is_current_step_on_timeline and not self.is_finished:
                status = "in-progress"
            
            # Adiciona a correção: Se o projeto terminou, todas as etapas devem ser marcadas como concluídas.
            if self.is_finished:
                status = "completed"
            
            timeline.append({"name": estado['nome'], "status": status})
        
        current_step_name = "Projeto Finalizado"
        if not self.is_finished:
            current_step_name = self.estados[self.current_step_index]['nome']
        else:
            self.last_preview_content = "Todas as etapas foram concluídas com sucesso!"
        
        is_paused = False
        logs = carregar_logs()
        if logs and logs[-1].get('status') == 'pausada':
            is_paused = True

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
                "is_paused": is_paused,
            },
            "project_name": self.project_name,
        }

    def get_current_project_name(self):
        return self.project_name

    def _handle_prompt_generation(self, observation):
        """Lida com a etapa 'gate' para gerar os arquivos de prompt."""
        if not self.system_type:
            print("[ERRO FSM] Tipo de sistema não definido. Não é possível gerar prompts.")
            self.last_preview_content = "ERRO: Por favor, selecione um tipo de sistema antes de aprovar."
            return

        print(f"[FLUXO] Aprovada a validação. Iniciando a geração de prompts para o tipo de sistema: '{self.system_type}'.")
        try:
            prompt_structure_path = os.path.join(BASE_DIR, "docs", "Estrutura de Prompts.md")
            with open(prompt_structure_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            parsed_prompts = parse_prompt_structure(markdown_content)
            
            if not save_prompts_to_json(self.project_name, self.system_type, parsed_prompts, BASE_DIR):
                raise Exception("Falha ao salvar os arquivos de prompt JSON.")

            print(f"[FLUXO] Arquivos de prompt JSON gerados com sucesso para '{self.system_type}'.")
            
            estado_atual = self.estados[self.current_step_index]
            registrar_log(estado_atual['nome'], 'concluída', decisao=observation or "Validação aprovada, iniciando linha do tempo")
            
            self._avancar_estado()
            
            proxima_etapa = self.estados[self.current_step_index]
            self._generate_artifact_draft(proxima_etapa)

        except Exception as e:
            print(f"[ERRO CRÍTICO] Falha ao gerar a estrutura de prompts: {e}")
            self.last_preview_content = f"ERRO CRÍTICO: Não foi possível gerar os prompts para o projeto. Verifique os logs."

    def _handle_artifact_generation(self, observation, current_preview_content):
        """Lida com a aprovação de um artefato e a geração do próximo."""
        estado_atual = self.estados[self.current_step_index]
        artefato_final_aprovado = current_preview_content or self.last_preview_content
        
        nome_arquivo_artefato = estado_atual.get("artefato_gerado", f"{_sanitizar_nome(estado_atual['nome'])}.md")
        caminho_artefatos_destino = os.path.join(BASE_DIR, "projetos", _sanitizar_nome(self.project_name), "artefatos")
        os.makedirs(caminho_artefatos_destino, exist_ok=True)
        caminho_arquivo_final = os.path.join(caminho_artefatos_destino, nome_arquivo_artefato)

        try:
            with open(caminho_arquivo_final, 'w', encoding='utf-8') as f:
                f.write(artefato_final_aprovado)
            print(f"[FLUXO] Artefato final da etapa '{estado_atual['nome']}' salvo em: {caminho_arquivo_final}")

            self._create_project_meta_files(nome_arquivo_artefato)

            registrar_log(estado_atual['nome'], 'concluída', decisao=observation or "Aprovado pelo supervisor", resposta_agente=f"Artefato salvo em {nome_arquivo_artefato}", observacao=observation)

            self._avancar_estado()
            if not self.is_finished:
                proxima_etapa = self.estados[self.current_step_index]
                if proxima_etapa.get('handler') == 'artifact_generation':
                    self._generate_artifact_draft(proxima_etapa)
                else:
                    self.last_preview_content = f"Aguardando ação para a etapa: {proxima_etapa['nome']}"
            else:
                self.last_preview_content = "PROJETO CONCLUÍDO! Todos os artefatos foram gerados e aprovados."
                print("[FLUXO] Todas as etapas da linha do tempo foram concluídas.")

        except Exception as e:
            print(f"[ERRO FSM] Falha ao processar aprovação da etapa '{estado_atual['nome']}': {e}")
            self.last_preview_content = f"Erro ao processar aprovação: {e}"

    def _generate_artifact_draft(self, etapa_alvo):
        """
Gera o RASCUNHO de um artefato para uma etapa específica da linha do tempo.
        O resultado é armazenado em self.last_preview_content para supervisão.
        """
        if not self.system_type or not self.project_name:
            self.last_preview_content = "ERRO INTERNO: Contexto do projeto (nome ou tipo) não definido."
            return

        manifesto_origem = etapa_alvo.get("manifesto_origem")
        if not manifesto_origem:
            self.last_preview_content = f"ERRO: A etapa '{etapa_alvo['nome']}' não possui um 'manifesto_origem' definido no workflow.json."
            return

        sanitized_project_name = _sanitizar_nome(self.project_name)
        caminho_manifesto_origem = os.path.join(BASE_DIR, "projetos", sanitized_project_name, "output", manifesto_origem)

        if not os.path.exists(caminho_manifesto_origem):
            self.last_preview_content = f"ERRO: O arquivo base '{manifesto_origem}' não foi encontrado."
            conteudo_original = f"# Rascunho para {etapa_alvo['nome']}\n\nO arquivo base '{manifesto_origem}' não foi encontrado. Este é um conteúdo de fallback. Por favor, descreva os requisitos para esta etapa."
        else:
            with open(caminho_manifesto_origem, 'r', encoding='utf-8') as f:
                conteudo_original = f.read()

        prompt_structure_path = os.path.join(BASE_DIR, "docs", "Estrutura de Prompts.md")
        positive_prompt, negative_prompt = parse_prompts(prompt_structure_path, self.system_type, etapa_alvo['nome'])

        if not positive_prompt or not negative_prompt:
            print(f"[AVISO] Não foi possível encontrar prompts para {self.system_type} - {etapa_alvo['nome']}. Usando conteúdo original como rascunho.")
            self.last_preview_content = conteudo_original
            return

        print(f"[FLUXO] Gerando rascunho para a etapa: {etapa_alvo['nome']}")
        try:
            conteudo_enriquecido = enrich_artifact(conteudo_original, self.system_type, etapa_alvo['nome'], positive_prompt, negative_prompt)
            self.last_preview_content = conteudo_enriquecido
            registrar_log(etapa_alvo['nome'], 'em andamento', decisao="Rascunho inicial gerado para supervisão.")
            print(f"[FLUXO] Rascunho para '{etapa_alvo['nome']}' gerado e pronto para supervisão.")
        except Exception as e:
            print(f"[ERRO] Falha ao gerar rascunho do artefato para '{etapa_alvo['nome']}': {e}")
            self.last_preview_content = f"ERRO ao gerar rascunho: {e}"

    def _create_project_meta_files(self, nome_arquivo_artefato):
        """Cria ou atualiza os arquivos README.md e GEMINI.md do projeto."""
        project_root = os.path.join(BASE_DIR, "projetos", _sanitizar_nome(self.project_name))
        
        readme_path = os.path.join(project_root, "README.md")
        if not os.path.exists(readme_path):
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f"# Projeto: {self.project_name}\n\nEste é o README do projeto. Ele será preenchido conforme o desenvolvimento avança.")
            print(f"[FLUXO] Arquivo README.md criado.")

        gemini_md_content = self._generate_gemini_md(nome_arquivo_artefato)
        gemini_md_path = os.path.join(project_root, "GEMINI.md")
        with open(gemini_md_path, 'w', encoding='utf-8') as f:
            f.write(gemini_md_content)
        print(f"[FLUXO] Arquivo GEMINI.md atualizado.")

    def _generate_gemini_md(self, nome_arquivo_artefato):
        """Gera o conteúdo para o arquivo Gemini.md com base no template."""
        template = f"""Get-Content GEMINI.md | gemini --ide-mode

# Roteiro de Execução para o Agente

## Projeto: **projetos/{self.project_name}/**
## Etapa Atual: **`{nome_arquivo_artefato}`**

### Missão do Agente
Sua missão é continuar o desenvolvimento deste projeto com base nos artefatos gerados pelo Archon AI.

### Instruções Imediatas:
1.  **Analise o Artefato Principal:**
    *   O artefato gerado para esta etapa é: **`artefatos/{nome_arquivo_artefato}`**.
    *   Leia e compreenda completamente o conteúdo deste arquivo. Ele contém a especificação ou o código que você deve usar como base.
2.  **Execute as Ações Necessárias:**
    *   Com base na análise, crie ou modifique os arquivos do projeto.
3.  **Reporte o Progresso:**
    *   Ao concluir, descreva as ações que você tomou e aguarde a próxima instrução.
---
# PERSONA
Você é um assistente de engenharia de software especialista e de classe mundial, focado no desenvolvimento full-stack de sistemas e software para o projeto Archon AI. Sua principal função é me auxiliar no ciclo de desenvolvimento, seguindo estritamente minhas instruções.

# OBJETIVO
Seu objetivo é fornecer respostas precisas, código de alta qualidade e insights técnicos, atuando como um par de programação experiente. Você deve me ajudar a resolver problemas, desenvolver funcionalidades e seguir as melhores práticas de engenharia de software, sempre aguardando meu comando para cada passo.

# REGRAS DE COMPORTAMENTO
1.  **Idioma:** Comunique-se exclusivamente em **Português (Brasil)**.
2.  **Aguardar Instruções:** **Nunca** aja proativamente. Sempre aguarde uma instrução clara minha antes de realizar qualquer tarefa. Não tente adivinhar os próximos passos ou antecipar minhas necessidades.
3.  **Confirmação para Prosseguir:** Ao final de cada resposta ou após apresentar uma solução, você **deve** perguntar explicitamente se pode prosseguir. Use frases como "Posso prosseguir com a implementação da Opção 1?", "Deseja que eu detalhe alguma das opções?" ou "Aguardando suas próximas instruções. O que faremos a seguir?".
4.  **Resolver Dúvidas:** Se uma instrução for ambígua ou se houver múltiplas maneiras de abordar um problema, você **deve** fazer perguntas para esclarecer. Questione sobre as melhores práticas aplicáveis ao contexto para me ajudar a tomar a melhor decisão.
5.  **Oferecer Múltiplas Opções:** Para qualquer problema técnico ou solicitação de implementação, você **deve** apresentar pelo menos **duas (2) opções** de solução. Descreva os prós e contras de cada uma, explicando o trade-off em termos de performance, manutenibilidade, complexidade, etc.
6.  **Resolução Avançada de Problemas com Servidores MCP:** Ao enfrentar dificuldades (ex: loops de execução, código incompleto, erros persistentes) ou ao lidar com tarefas que exigem conhecimento preciso e atualizado de APIs, SDKs ou bibliotecas externas, devo proativamente sugerir o uso de um dos servidores MCP configurados (ex: `context7`, `microsoft-docs`, `playwright`). Devo explicar como ele pode fornecer a documentação e os exemplos mais recentes para superar o obstáculo e, então, solicitar sua permissão para consultá-lo.

# FORMATO DA RESPOSTA
- **Clareza e Estrutura:** Organize suas respostas de forma clara, usando markdown (títulos, listas, blocos de código) para facilitar a leitura.
- **Blocos de Código:** Apresente exemplos de código em blocos formatados corretamente com a linguagem especificada (ex: ```python).
- **Diferenças (Diffs):** Se a solicitação envolver a modificação de um arquivo existente, forneça a resposta no formato `diff`.

# INSTRUÇÃO INICIAL
Responda a esta mensagem inicial com: "Gemini pronto e aguardando suas instruções."
"""
        return template

    def process_action(self, action, observation="", project_name=None, current_preview_content=None, system_type=None):
        if project_name and not self.project_name:
            self.project_name = project_name
        if system_type:
            self.system_type = system_type
        self._save_project_context()

        if self.is_finished or not self.project_name:
            if action == 'reset':
                return self.reset_project(project_name_to_reset=project_name)
            return self.get_status()

        estado_atual = self.estados[self.current_step_index]
        handler = estado_atual.get("handler")

        if action == 'approve':
            print(f"[FSM] Aprovando etapa '{estado_atual['nome']}' com handler '{handler}'.")
            if handler == 'prompt_generation':
                self._handle_prompt_generation(observation)
            elif handler == 'artifact_generation':
                self._handle_artifact_generation(observation, current_preview_content)
            else:
                print(f"[ERRO] Handler desconhecido '{handler}' para a etapa '{estado_atual['nome']}'.")
                self.last_preview_content = f"Erro de configuração: Handler '{handler}' não reconhecido."

        elif action == 'repeat':
            print(f"[FSM] Repetindo etapa '{estado_atual['nome']}'.")
            if handler == 'artifact_generation':
                self._generate_artifact_draft(estado_atual)
            else:
                self.last_preview_content = "A ação 'Repetir' não se aplica a esta etapa de validação."

        elif action == 'pause':
            print(f"[FSM] Pausando etapa '{estado_atual['nome']}'.")
            registrar_log(estado_atual['nome'], 'pausada', decisao="Projeto pausado pelo supervisor.", observacao=observation)

        elif action == 'back':
            if self.current_step_index > 0:
                print(f"[FSM] Voltando para a etapa anterior.")
                self.current_step_index -= 1
                etapa_alvo = self.estados[self.current_step_index]
                _invalidar_logs_posteriores(etapa_alvo['nome'], self.estados)
                
                if etapa_alvo.get('handler') == 'artifact_generation':
                    self._generate_artifact_draft(etapa_alvo)
                else:
                    self.last_preview_content = "Aguardando a validação da proposta e a seleção do tipo de sistema."

        elif action == 'update_preview':
            print(f"[FSM] Atualizando preview com refinamento do supervisor.")
            if current_preview_content is not None:
                self.last_preview_content = current_preview_content
                registrar_log(estado_atual['nome'], 'em andamento', decisao="Supervisor refinou o artefato com IA.", observacao=observation)
        
        return self.get_status()

    def setup_project(self, project_name, initial_preview_content=None, system_type=None):
        if not project_name or not project_name.strip():
            return self.get_status()
        
        self.project_name = _sanitizar_nome(project_name)
        self.system_type = system_type
        self._save_project_context()
        
        if initial_preview_content:
            self.last_preview_content = initial_preview_content
        
        self.current_step_index = 0
        self.is_finished = False
        self.last_preview_content = "Aguardando a validação da proposta e a seleção do tipo de sistema para gerar a estrutura de prompts e iniciar o projeto."

        print(f"[PROJETO] Projeto '{self.project_name}' iniciado. Aguardando aprovação na etapa '{self.estados[0]['nome']}'.")
        return self.get_status()

    def reset_project(self, project_name_to_reset=None):
        """Reseta o estado do projeto. Se um nome de projeto for fornecido, arquiva esse projeto específico."""
        print("\n[RESET] Iniciando reset completo do projeto...")
        
        project_to_reset = project_name_to_reset or self.project_name
        if project_to_reset:
            sanitized_name = _sanitizar_nome(project_to_reset)
            project_dir = os.path.join(BASE_DIR, "projetos", sanitized_name)
            
            os.makedirs(ARCHIVED_PROJECTS_DIR, exist_ok=True)

            if os.path.exists(project_dir):
                try:
                    archive_name = f"{sanitized_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    archive_path = os.path.join(ARCHIVED_PROJECTS_DIR, archive_name)
                    shutil.make_archive(archive_path, 'zip', project_dir)
                    print(f"[RESET] Projeto '{project_to_reset}' arquivado em: {archive_path}.zip")
                    shutil.rmtree(project_dir)
                    print(f"[RESET] Diretório do projeto '{project_to_reset}' removido.")
                except Exception as e:
                    print(f"[ERRO RESET] Falha ao arquivar ou remover o projeto '{project_to_reset}': {e}")

        self.reset_fsm_state_and_logs()
        return self.get_status()

    def reset_fsm_state_and_logs(self):
        """Reseta o estado interno da FSM e limpa os arquivos de log e contexto."""
        print("\n[RESET FSM] Limpando estado da FSM e arquivos de log...")
        
        for file_path in [LOG_PATH, CHECKPOINT_PATH, PROJECT_CONTEXT_PATH]:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError as e:
                    print(f"[ERRO RESET FSM] Falha ao remover o arquivo '{file_path}': {e}")

        self.current_step_index = 0
        self.last_preview_content = INITIAL_PREVIEW_CONTENT
        self.is_finished = False
        self.project_name = None
        self.system_type = None
        print("[RESET FSM] Estado da FSM e arquivos de log foram limpos.")

    def create_temp_archive_for_download(self, project_name):
        """Cria um arquivo ZIP do projeto em um local temporário e retorna o caminho."""
        sanitized_name = _sanitizar_nome(project_name)
        project_path = os.path.join(BASE_DIR, "projetos", sanitized_name)
        if not os.path.isdir(project_path):
            raise FileNotFoundError(f"Diretório do projeto '{project_name}' não encontrado.")
        
        temp_dir = tempfile.mkdtemp()
        zip_path = shutil.make_archive(os.path.join(temp_dir, sanitized_name), 'zip', project_path)
        return zip_path, temp_dir

# --- Inicialização da FSM ---
project_states = carregar_workflow()
if not project_states:
    sys.exit("ERRO CRÍTICO: Falha no carregamento do workflow.json. O sistema não pode iniciar.")

fsm_instance = FSMOrquestrador(project_states)
