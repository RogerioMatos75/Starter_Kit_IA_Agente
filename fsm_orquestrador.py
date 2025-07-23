# Orquestrador FSM com leitura automática do guia de projeto, confirmação manual e registro de log

import time
import os
import shutil
import re
import json
import hashlib
import sys
from datetime import datetime
from auditoria_seguranca import auditoria_global
from ia_executor import executar_prompt_ia, IAExecutionError
from gerenciador_artefatos import salvar_artefatos_projeto
from utils.file_parser import _sanitizar_nome
from utils.supabase_client import supabase, CONFIG

# --- CONFIGURAÇÃO DE CAMINHOS ABSOLUTOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_PATH = os.path.join(BASE_DIR, "logs", "diario_execucao.json")
CHECKPOINT_PATH = os.path.join(BASE_DIR, "logs", "proximo_estado.json")
PROJECT_CONTEXT_PATH = os.path.join(BASE_DIR, "logs", "project_context.json")
PROMPT_TEMPLATES_PATH = os.path.join(BASE_DIR, "prompt_templates.json")

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
        self._load_project_context()
        self._load_progress()
        FSMOrquestrador.instance = self

    def _load_project_context(self):
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
        if self.project_name:
            context = {"project_name": self.project_name}
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

    def _run_current_step(self):
        if self.is_finished or self.project_name is None:
            return
        
        estado_atual = self.estados[self.current_step_index]
        print(f"\n=== Executando Etapa: {estado_atual['nome']} para o projeto '{self.project_name}' ===")
        
        if estado_atual['nome'] == "Definindo Layout UI":
            self.last_preview_content = "Aguardando a definição do layout pelo usuário na interface..."
            print("[INFO] Etapa de layout. Aguardando ação do usuário.")
            return

        contexto_guia = ""
        caminho_guia_template = estado_atual.get('guia')
        if caminho_guia_template:
            caminho_guia_real = caminho_guia_template.format(project_name=_sanitizar_nome(self.project_name))
            guia_path_abs = os.path.join(BASE_DIR, caminho_guia_real)
            
            if os.path.exists(guia_path_abs):
                try:
                    with open(guia_path_abs, 'r', encoding='utf-8') as f:
                        contexto_guia = f.read()
                    print(f"[CONTEXTO] Guia '{caminho_guia_real}' carregado para a etapa.")
                except IOError as e:
                    print(f"[AVISO] Não foi possível ler o arquivo de guia: {e}")
            else:
                print(f"[AVISO] Arquivo de guia especificado não encontrado: {guia_path_abs}")

        prompt = gerar_prompt_etapa(estado_atual, contexto_guia)
        try:
            resultado = executar_prompt_ia(prompt)
            self.last_preview_content = resultado
            print(f"Resultado da execução (preview):\n{str(resultado)[:500]}...")
        except IAExecutionError as e:
            print(f"[ERRO FSM] Erro de execução da IA na etapa '{estado_atual['nome']}': {e}")
            self.last_preview_content = f"Ocorreu um erro ao contatar a IA. Verifique o console."

    def process_action(self, action, observation="", project_name=None, current_preview_content=None):
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

        if action == 'approve':
            artefato_final = self.last_preview_content
            print(f"[FSM] Aprovando etapa '{estado_atual['nome']}'. Gerando roteiro para a próxima etapa...")
            
            meta_prompt_template = PROMPT_TEMPLATES.get("gerar_roteiro_gemini_md")
            if not meta_prompt_template:
                self.last_preview_content = "ERRO: Template de roteiro não encontrado!"
                return self.get_status()

            prompt_roteiro = meta_prompt_template.format(conteudo_artefato=artefato_final)
            try:
                roteiro_gemini_md = executar_prompt_ia(prompt_roteiro)
                salvar_artefatos_projeto(self.project_name, estado_atual, artefato_final, roteiro_gemini_md)
                registrar_log(estado_atual['nome'], 'concluída', decisao=observation, resposta_agente=artefato_final, observacao=observation)
                self._avancar_estado()
                self._run_current_step()
            except IAExecutionError as e:
                print(f"[ERRO FSM] Falha ao gerar roteiro para a próxima etapa: {e}")
                self.last_preview_content = f"Erro ao gerar o roteiro para a próxima etapa: {e}"
            except Exception as e:
                print(f"[ERRO FSM] Falha ao salvar artefatos após aprovação: {e}")
                self.last_preview_content = f"Erro ao salvar os artefatos: {e}"

        elif action == 'repeat':
            self._run_current_step()
        
        elif action == 'back':
            if self.current_step_index > 0:
                self.current_step_index -= 1
                etapa_alvo = self.estados[self.current_step_index]['nome']
                _invalidar_logs_posteriores(etapa_alvo, self.estados)
                self._run_current_step()
        
        return self.get_status()

    def setup_project(self, project_name):
        if not project_name or not project_name.strip():
            print("[ERRO] O nome do projeto é obrigatório para iniciar.")
            return self.get_status()
        self.project_name = project_name.strip()
        self._save_project_context()
        print(f"[PROJETO] Nome do projeto definido como: '{self.project_name}'")
        self._run_current_step()
        return self.get_status()

    def reset_project(self, project_name_to_reset=None):
        """Reseta o estado do projeto. Se um nome de projeto for fornecido, arquiva esse projeto específico."""
        print("\n[RESET] Iniciando reset completo do projeto...")
        
        # Usa o nome do projeto fornecido, caso contrário, usa o do estado da FSM como fallback
        project_to_archive = project_name_to_reset or self.project_name
        print(f"[DEBUG] Nome do projeto para arquivar: '{project_to_archive}'")

        if project_to_archive:
            sanitized_name = _sanitizar_nome(project_to_archive)
            projetos_dir = os.path.join(BASE_DIR, "projetos", sanitized_name)
            
            if os.path.exists(projetos_dir):
                try:
                    archive_dir = os.path.join(BASE_DIR, "projetos", "arquivados")
                    os.makedirs(archive_dir, exist_ok=True)
                    
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    archive_path = os.path.join(archive_dir, f"{sanitized_name}_{timestamp}")
                    
                    shutil.move(projetos_dir, archive_path)
                    print(f"[RESET] Projeto '{project_to_archive}' arquivado em '{archive_path}'.")
                except (OSError, shutil.Error) as e:
                    print(f"[ERRO RESET] Falha ao arquivar o projeto '{project_to_archive}': {e}")
            else:
                print(f"[AVISO RESET] Diretório do projeto '{projetos_dir}' não encontrado para arquivamento.")

            # Limpeza do Supabase (se habilitado)
            if supabase and CONFIG.get("SUPABASE_ENABLED"):
                try:
                    files_to_delete = supabase.storage.from_("artefatos-projetos").list(path=sanitized_name)
                    if files_to_delete:
                        file_paths = [f"{sanitized_name}/{f['name']}" for f in files_to_delete]
                        supabase.storage.from_("artefatos-projetos").remove(file_paths)
                        print(f"[SUPABASE] Artefatos do projeto '{project_to_archive}' removidos do Storage.")
                except Exception as e:
                    print(f"[ERRO SUPABASE] Falha ao remover artefatos do projeto '{project_to_archive}': {e}")

        # Limpeza geral de logs e contexto
        if os.path.exists(LOG_PATH):
            os.remove(LOG_PATH)
        if os.path.exists(CHECKPOINT_PATH):
            os.remove(CHECKPOINT_PATH)
        if os.path.exists(PROJECT_CONTEXT_PATH):
            os.remove(PROJECT_CONTEXT_PATH)
        
        # Reseta o estado da FSM
        self.current_step_index = 0
        self.last_preview_content = INITIAL_PREVIEW_CONTENT
        self.is_finished = False
        self.project_name = None
        print("[RESET] Estado da FSM e arquivos de log foram limpos. O sistema está pronto para um novo projeto.")
        
        return self.get_status()

project_states = carregar_workflow()
if not project_states or not PROMPT_TEMPLATES:
    sys.exit("ERRO CRÍTICO: Falha no carregamento do workflow.json ou prompt_templates.json.")

fsm_instance = FSMOrquestrador(project_states)