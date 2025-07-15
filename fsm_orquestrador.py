# Orquestrador FSM com leitura automática do guia de projeto, confirmação manual e registro de log

import time
import os
import shutil
import re
import json
import hashlib
import sys
from datetime import datetime
from guia_projeto import extrair_secoes, REQUIRED_SECTIONS, SECTION_TITLES
from auditoria_seguranca import auditoria_global
from ia_executor import executar_prompt_ia, IAExecutionError
from gerenciador_artefatos import salvar_artefatos_projeto, BUCKET_NAME
from utils.file_parser import _sanitizar_nome # Importa a função de sanitização
from utils.supabase_client import supabase

# --- CONFIGURAÇÃO DE CAMINHOS ABSOLUTOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_PATH = os.path.join(BASE_DIR, "logs", "diario_execucao.json")
CHECKPOINT_PATH = os.path.join(BASE_DIR, "logs", "proximo_estado.json")
PROJECT_CONTEXT_PATH = os.path.join(BASE_DIR, "logs", "project_context.json")

# Tenta importar o gerador de PDF, mas não quebra se não estiver disponível
try:
    from relatorios import gerar_log_pdf
except ImportError:
    print("[AVISO] Módulo 'reportlab' não encontrado. A geração de PDF estará desativada.")
    gerar_log_pdf = None

INITIAL_PREVIEW_CONTENT = """# O Projeto Ainda Não Foi Iniciado

Para começar, preciso de algumas informações essenciais. Por favor, siga os passos na interface:

**1. Defina o Nome do Projeto:**
Dê um nome claro e descritivo para o projeto.

**2. Descreva o Projeto:**
Forneça uma descrição detalhada do que você deseja construir.

**3. (Opcional) Forneça Documentos de Contexto:**
Faça o upload de arquivos (.pdf, .txt, .md) que possam ajudar a IA a entender melhor o projeto.

**4. Gere a Base de Conhecimento:**
Clique em "Gerar Base de Conhecimento" para que a IA crie os documentos fundamentais do projeto.

---
*Estou pronto para começar assim que tivermos esses detalhes definidos.*
"""

def carregar_workflow(file_path=None):
    if file_path is None:
        file_path = os.path.join(BASE_DIR, "workflow.json")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)
        print(f"Workflow '{workflow_data.get('nome_workflow')}' carregado com sucesso.")
        return workflow_data.get("estados", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[ERRO CRÍTICO] Não foi possível carregar o workflow de '{file_path}': {e}")
        return []

def carregar_logs():
    """Carrega os logs de execução do arquivo JSON, tratando erros de forma centralizada."""
    if not os.path.exists(LOG_PATH):
        return []
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            if not content:
                return []
            data = json.loads(content)
            return data.get('execucoes', [])
    except (json.JSONDecodeError, TypeError):
        print(f"[AVISO] Arquivo de log '{LOG_PATH}' malformado ou corrompido. Tratando como vazio.")
        return []

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

def gerar_prompt_etapa(etapa, secoes):
    """Gera um prompt dinâmico com base nos detalhes da etapa do workflow."""
    prompt_base = (
        f"**Contexto do Projeto:** Você está trabalhando em um projeto de software. A etapa atual é: **'{etapa['nome']}'**.\n"
        f"**Tipo de Tarefa:** {etapa.get('tipo', 'Geral')}\n"
        f"**Descrição da Tarefa:** {etapa.get('descricao', 'Execute a tarefa conforme o nome da etapa.')}\n"
    )

    if etapa.get('tecnologia'):
        prompt_base += f"**Tecnologia Específica:** {etapa['tecnologia']}\n"

    if secoes:
        prompt_base += (
            "\n**Informações da Base de Conhecimento (Guia):**\n"
            "--- INÍCIO DO GUIA ---\n"
            f"{secoes}\n"
            "--- FIM DO GUIA ---\n\n"
        )

    prompt_base += "Com base em todas as informações acima, gere o artefato solicitado para esta etapa. Seja claro, objetivo e siga as melhores práticas para a tecnologia especificada. Gere apenas o conteúdo do arquivo, sem explicações adicionais."
    return prompt_base

def executar_codigo_real(prompt, etapa_atual, project_name):
    """Executa a chamada à IA, salva o artefato no Supabase e retorna o conteúdo para preview."""
    etapa_nome = etapa_atual['nome']
    print(f"\n[EXECUTOR] Prompt enviado para a IA para a etapa: {etapa_nome}")
 
    try:
        codigo_gerado = executar_prompt_ia(prompt)
    except IAExecutionError as e:
        print(f"[ERRO FSM] Erro de execução da IA na etapa '{etapa_nome}': {e}")
        return f"Ocorreu um erro ao contatar a IA. Verifique o console do servidor para detalhes.\n\nErro: {e}"
 
    try:
        arquivo_gerado_path = salvar_artefatos_projeto(project_name, etapa_atual, codigo_gerado)
        auditoria_global.log_artefacto_gerado(
            project_name=project_name,
            file_path=arquivo_gerado_path,
            file_content=codigo_gerado
        )
        return codigo_gerado
    except Exception as e:
        error_message = f"Erro ao processar artefatos para a etapa '{etapa_nome}': {e}"
        print(f"[ERRO FSM] {error_message}")
        return f"Erro ao salvar artefatos: {error_message}"
    
def _invalidar_logs_posteriores(etapa_alvo, estados):
    """Remove do log todas as entradas de etapas posteriores à etapa_alvo."""
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
        self._load_project_context()
        self._load_progress()
        FSMOrquestrador.instance = self

    def _load_project_context(self):
        """Carrega o nome do último projeto ativo (efêmero na Vercel)."""
        if os.path.exists(PROJECT_CONTEXT_PATH):
            try:
                with open(PROJECT_CONTEXT_PATH, "r", encoding="utf-8") as f:
                    context = json.load(f)
                    self.project_name = context.get("project_name")
                    if self.project_name:
                        print(f"[CONTEXTO] Projeto '{self.project_name}' carregado da sessão anterior.")
            except (json.JSONDecodeError, TypeError):
                print(f"[AVISO] Arquivo de contexto '{PROJECT_CONTEXT_PATH}' malformado.")

    def _save_project_context(self):
        """Salva o nome do projeto atual (efêmero na Vercel)."""
        if self.project_name:
            context = {"project_name": self.project_name}
            with open(PROJECT_CONTEXT_PATH, "w", encoding="utf-8") as f:
                json.dump(context, f, indent=2)

    def _load_progress(self):
        """Lê o log para encontrar a última etapa concluída e retomar o progresso."""
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
        """Avança o FSM para a próxima etapa, se houver."""
        if self.current_step_index < len(self.estados) - 1:
            self.current_step_index += 1
        else:
            self.is_finished = True

    def get_status(self):
        """Prepara o dicionário de status para a API."""
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

    def _run_current_step(self):
        """Executa a lógica da etapa atual e atualiza o preview."""
        if self.is_finished or self.project_name is None:
            return
        estado = self.estados[self.current_step_index]
        print(f"\n=== Executando Etapa: {estado['nome']} para o projeto '{self.project_name}' ===")
        
        if estado['nome'] == "Definindo Layout UI":
            self.last_preview_content = "Aguardando a definição do layout pelo usuário na interface..."
            print("[INFO] Etapa de layout. Aguardando ação do usuário via API /api/define_layout.")
            return

        file_path = estado.get('guia')
        if file_path:
            file_path = os.path.join(BASE_DIR, file_path)

        secoes = ""
        if file_path and os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            headers = REQUIRED_SECTIONS.get(file_name, [])
            secoes_dict = extrair_secoes(file_path, headers)
            secoes = "\n".join([f"## {h.strip('# ')}\n{secoes_dict.get(h, '')}" for h in headers])
        
        prompt = gerar_prompt_etapa(estado, secoes)
        resultado = executar_codigo_real(prompt, estado, self.project_name)
        self.last_preview_content = resultado
        print(f"Resultado da execução (preview):\n{resultado[:500]}...")

    def process_layout_definition(self, project_name, layout_spec):
        """Recebe os dados do layout da API e salva o artefato."""
        print(f"[FSM] Processando definição de layout para o projeto: {project_name}")
        
        etapa_layout = next((e for e in self.estados if e['nome'] == "Definindo Layout UI"), None)
        if not etapa_layout:
            raise ValueError("A etapa 'Definindo Layout UI' não foi encontrada no workflow.json")

        layout_content_str = json.dumps(layout_spec, indent=2)

        salvar_artefatos_projeto(project_name, etapa_layout, layout_content_str)
        
        self.last_preview_content = layout_content_str
        
        registrar_log(
            etapa=etapa_layout['nome'], 
            status='concluída', 
            decisao='Layout definido pelo usuário via interface.',
            resposta_agente=layout_content_str
        )
        print(f"[FSM] Artefato 'layout_spec.json' salvo e log registrado para o projeto {project_name}.")

    def setup_project(self, project_name):
        """Configura o nome do projeto e executa a primeira etapa."""
        if not project_name or not project_name.strip():
            print("[ERRO] O nome do projeto é obrigatório para iniciar.")
            return self.get_status()
        self.project_name = project_name.strip()
        self._save_project_context()
        print(f"[PROJETO] Nome do projeto definido como: '{self.project_name}'")
        self._run_current_step()
        return self.get_status()

    def process_action(self, action, observation="", project_name=None, current_preview_content=None):
        """Processa uma ação vinda da UI e retorna o novo estado."""
        if project_name and not self.project_name:
            self.project_name = project_name
            self._save_project_context()
            print(f"[PROJETO] Contexto do projeto restaurado para: '{self.project_name}'")

        if self.is_finished or self.project_name is None:
            if action == 'reset':
                return self.reset_project()
            return self.get_status()
        
        estado_atual = self.estados[self.current_step_index]

        if current_preview_content is not None:
            self.last_preview_content = current_preview_content

        if action == 'confirm_suggestion':
            if current_preview_content is None:
                return self.get_status()
            registrar_log(estado_atual['nome'], 'concluída', decisao=f"Sugestão da IA confirmada. {observation}", resposta_agente=current_preview_content, observacao=observation)
            salvar_artefatos_projeto(project_name, estado_atual, current_preview_content)
            self._avancar_estado()
            self._run_current_step()

        elif action == 'approve':
            registrar_log(estado_atual['nome'], 'concluída', decisao=observation, resposta_agente=self.last_preview_content, observacao=observation)
            self._avancar_estado()
            self._run_current_step()

        elif action == 'repeat':
            self._run_current_step()
        
        elif action == 'back':
            if self.current_step_index > 0:
                self.current_step_index -= 1
                etapa_alvo = self.estados[self.current_step_index]['nome']
                _invalidar_logs_posteriores(etapa_alvo, self.estados)
                self._run_current_step()
        
        elif action == 'pause':
            registrar_log(estado_atual['nome'], "pausada", "revisão manual", resposta_agente=self.last_preview_content, observacao=observation)
        
        elif action == 'start':
            registrar_log(estado_atual['nome'], "em andamento", "retomado", resposta_agente=self.last_preview_content, observacao=observation)
        
        return self.get_status()

    def reset_project(self):
        """Reseta o projeto, limpando os artefatos no Supabase, os diretórios locais e os logs."""
        print("\n[RESET] Iniciando reset completo do projeto...")

        # --- Limpeza de Artefatos Locais ---
        if self.project_name:
            sanitized_name = _sanitizar_nome(self.project_name)
            
            # 1. Limpar diretório de output
            output_dir = os.path.join(BASE_DIR, "output", sanitized_name)
            if os.path.exists(output_dir):
                try:
                    shutil.rmtree(output_dir)
                    print(f"[RESET] Diretório de output local '{output_dir}' removido.")
                except OSError as e:
                    print(f"[ERRO RESET] Falha ao remover o diretório de output '{output_dir}': {e}")

            # 2. Limpar diretório de projetos (exceto 'arquivados')
            projetos_dir = os.path.join(BASE_DIR, "projetos")
            if os.path.exists(projetos_dir):
                for item in os.listdir(projetos_dir):
                    item_path = os.path.join(projetos_dir, item)
                    if item != "arquivados": # Condição para não apagar a pasta de arquivados
                        try:
                            if os.path.isdir(item_path):
                                shutil.rmtree(item_path)
                                print(f"[RESET] Diretório de projeto '{item_path}' removido.")
                            else:
                                os.remove(item_path)
                                print(f"[RESET] Arquivo de projeto '{item_path}' removido.")
                        except OSError as e:
                            print(f"[ERRO RESET] Falha ao remover '{item_path}': {e}")
            
            # 3. Limpar artefatos do Supabase (lógica existente)
            if supabase:
                try:
                    files_to_delete = supabase.storage.from_(BUCKET_NAME).list(path=sanitized_name)
                    if files_to_delete:
                        file_paths = [f"{sanitized_name}/{f['name']}" for f in files_to_delete]
                        supabase.storage.from_(BUCKET_NAME).remove(file_paths)
                        print(f"[SUPABASE] Artefatos do projeto '{self.project_name}' removidos do Storage.")
                except Exception as e:
                    print(f"[ERRO SUPABASE] Falha ao remover artefatos do projeto '{self.project_name}': {e}")

        # --- Limpeza de Logs e Contexto ---
        if os.path.exists(LOG_PATH):
            os.remove(LOG_PATH)
        if os.path.exists(CHECKPOINT_PATH):
            os.remove(CHECKPOINT_PATH)
        if os.path.exists(PROJECT_CONTEXT_PATH):
            os.remove(PROJECT_CONTEXT_PATH)
        
        # --- Reset do Estado Interno ---
        self.current_step_index = 0
        self.last_preview_content = INITIAL_PREVIEW_CONTENT
        self.is_finished = False
        self.project_name = None
        print("[RESET] Projeto resetado com sucesso.")
        
        status = self.get_status()
        return status

project_states = carregar_workflow()
if not project_states:
    sys.exit("ERRO CRÍTICO: Falha no carregamento do workflow.json.")

fsm_instance = FSMOrquestrador(project_states)