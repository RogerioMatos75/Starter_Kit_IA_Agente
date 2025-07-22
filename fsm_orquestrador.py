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
from utils.supabase_client import supabase

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

def executar_etapa_ia(prompt, etapa_atual, project_name, contexto_guia=""):
    etapa_nome = etapa_atual['nome']
    print(f"\n[EXECUTOR] Gerando artefato principal para a etapa: {etapa_nome}")
    
    prompt_artefato = gerar_prompt_etapa(etapa_atual, contexto_guia)
    
    try:
        artefato_gerado = executar_prompt_ia(prompt_artefato)
    except IAExecutionError as e:
        print(f"[ERRO FSM] Erro de execução da IA na etapa '{etapa_nome}': {e}")
        return f"Ocorreu um erro ao contatar a IA. Verifique o console para detalhes.\n\nErro: {e}", None

    print(f"[EXECUTOR] Gerando roteiro GEMINI.md para a próxima etapa...")
    meta_prompt_template = PROMPT_TEMPLATES.get("gerar_roteiro_gemini_md")
    if not meta_prompt_template:
        return "Erro: Template 'gerar_roteiro_gemini_md' não encontrado em prompt_templates.json.", None

    prompt_roteiro = meta_prompt_template.format(conteudo_artefato=artefato_gerado)
    
    try:
        roteiro_gemini_md = executar_prompt_ia(prompt_roteiro)
    except IAExecutionError as e:
        print(f"[ERRO FSM] Erro de execução da IA ao gerar o roteiro GEMINI.md: {e}")
        return f"Ocorreu um erro ao contatar a IA para gerar o roteiro. Verifique o console.", None

    try:
        caminho_artefato = salvar_artefatos_projeto(project_name, etapa_atual, artefato_gerado, roteiro_gemini_md)
        auditoria_global.log_artefacto_gerado(
            project_name=project_name,
            file_path=caminho_artefato,
            file_content=artefato_gerado
        )
        return artefato_gerado, roteiro_gemini_md
    except Exception as e:
        error_message = f"Erro ao processar artefatos para a etapa '{etapa_nome}': {e}"
        print(f"[ERRO FSM] {error_message}")
        return f"Erro ao salvar artefatos: {error_message}", None

def _invalidar_logs_posteriores(etapa_alvo, estados):
    # ... (lógica existente sem alterações)
    pass

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

    # ... (_load_project_context, _save_project_context, _load_progress, _avancar_estado sem alterações)

    def get_status(self):
        # ... (lógica existente sem alterações)
        pass

    def _run_current_step(self):
        if self.is_finished or self.project_name is None:
            return
        
        estado_atual = self.estados[self.current_step_index]
        print(f"\n=== Executando Etapa: {estado_atual['nome']} para o projeto '{self.project_name}' ===")
        
        if estado_atual['nome'] == "Definindo Layout UI":
            self.last_preview_content = "Aguardando a definição do layout pelo usuário na interface..."
            print("[INFO] Etapa de layout. Aguardando ação do usuário via API /api/define_layout.")
            return

        contexto_guia = ""
        caminho_guia_template = estado_atual.get('guia')
        if caminho_guia_template:
            # Substitui o placeholder {project_name} pelo nome real do projeto
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

        resultado, _ = executar_etapa_ia(None, estado_atual, self.project_name, contexto_guia)
        self.last_preview_content = resultado
        print(f"Resultado da execução (preview):\n{str(resultado)[:500]}...")

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
            # Na aprovação, o conteúdo do preview é o artefato finalizado.
            artefato_final = self.last_preview_content
            
            # Gerar o roteiro para a *próxima* etapa
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
        
        # ... (outras ações como pause, start)
        
        return self.get_status()

    # ... (setup_project, reset_project, etc. sem alterações significativas na lógica principal)
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

    def reset_project(self):
        """Reseta o projeto, limpando os artefatos no Supabase, os diretórios locais e os logs."""
        print("\n[RESET] Iniciando reset completo do projeto...")

        # --- Limpeza de Artefatos Locais ---
        if self.project_name:
            sanitized_name = _sanitizar_nome(self.project_name)
            
            # Limpar diretório de projetos (exceto 'arquivados')
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
            
            # Limpar artefatos do Supabase (lógica existente)
            if supabase and CONFIG.get("SUPABASE_ENABLED"):
                try:
                    files_to_delete = supabase.storage.from_("artefatos-projetos").list(path=sanitized_name)
                    if files_to_delete:
                        file_paths = [f"{sanitized_name}/{f['name']}" for f in files_to_delete]
                        supabase.storage.from_("artefatos-projetos").remove(file_paths)
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
        
        return self.get_status()

project_states = carregar_workflow()
if not project_states or not PROMPT_TEMPLATES:
    sys.exit("ERRO CRÍTICO: Falha no carregamento do workflow.json ou prompt_templates.json.")

fsm_instance = FSMOrquestrador(project_states)
