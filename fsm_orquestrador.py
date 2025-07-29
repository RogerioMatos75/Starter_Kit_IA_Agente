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

    def _run_current_step(self):
        if self.is_finished or self.project_name is None:
            return
        
        estado_atual = self.estados[self.current_step_index]
        print(f"\n=== Executando Etapa: {estado_atual['nome']} para o projeto '{self.project_name}' ===")
        
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

    def process_action(self, action, observation="", project_name=None, current_preview_content=None, system_type=None):
        if project_name and not self.project_name:
            self.project_name = project_name
            self._save_project_context()
            print(f"[PROJETO] Contexto do projeto restaurado para: '{self.project_name}'")

        # NEW: If system_type is provided, update the FSM's system_type
        if system_type and self.system_type is None:
            self.system_type = system_type
            self._save_project_context()
            print(f"[PROJETO] Tipo de sistema definido para: '{self.system_type}'")

        if self.is_finished or self.project_name is None:
            if action == 'reset':
                # A ação de reset agora é chamada pela rota /action
                # O project_name já é passado como argumento para process_action
                return self.reset_project(project_name_to_reset=project_name)
            return self.get_status()
        
        estado_atual = self.estados[self.current_step_index]

        if current_preview_content is not None:
            self.last_preview_content = current_preview_content

        if action == 'approve':
            print(f"[FSM] Aprovando etapa '{estado_atual['nome']}'.")
            
            # Lógica especial para a primeira etapa: Salvar o manifesto E gerar prompts específicos
            if estado_atual['nome'] == self.estados[0]['nome']: # Compara com a primeira etapa do workflow
                try:
                    # The base knowledge documents (01_base_conhecimento.md, etc.) are already generated
                    # and saved to the project's output directory by the /api/setup/generate_project_base route.
                    # self.last_preview_content already holds the summary of these generated files.
                    print("[FLUXO] Base de Conhecimento (múltiplos arquivos) já gerada pela Etapa 1.")

                    # NEW: Generate and save structured prompts based on system type
                    if self.system_type and self.project_name:
                        print(f"[FLUXO] Gerando prompts para o tipo de sistema: {self.system_type}")
                        prompt_structure_md_path = os.path.join(BASE_DIR, "docs", "Estrutura de Prompts.md")
                        
                        if os.path.exists(prompt_structure_md_path):
                            with open(prompt_structure_md_path, 'r', encoding='utf-8') as f:
                                prompt_structure_content = f.read()
                            
                            parsed_prompts = parse_prompt_structure(prompt_structure_content)
                            save_prompts_to_json(self.project_name, self.system_type, parsed_prompts, BASE_DIR)
                            print(f"[FLUXO] Prompts específicos para '{self.system_type}' gerados e salvos.")
                        else:
                            print(f"[AVISO] Arquivo 'Estrutura de Prompts.md' não encontrado em {prompt_structure_md_path}. Não foi possível gerar prompts específicos.")
                    else:
                        print("[AVISO] Tipo de sistema não definido ou nome do projeto ausente. Não foi possível gerar prompts específicos.")
                    
                    registrar_log(estado_atual['nome'], 'concluída', decisao="Base de Conhecimento aprovada", resposta_agente=self.last_preview_content)
                    self._avancar_estado()
                    # Não executa _run_current_step() aqui, pois a próxima etapa é de validação manual
                    self.last_preview_content = f"Base de Conhecimento aprovada. Agora, valide os itens na Etapa 2 e selecione o tipo de sistema."

                except Exception as e:
                    print(f"[ERRO FSM] Falha ao processar aprovação da Base de Conhecimento ou gerar prompts: {e}")
                    self.last_preview_content = f"Erro ao processar aprovação: {e}"
            
            # Lógica para as etapas subsequentes (gerar roteiro, etc.)
            else:
                print("[FLUXO] Gerando roteiro para a próxima etapa...")
                artefato_final = self.last_preview_content
                
                # NEW: Load GEMINI.md template and fill placeholders
                gemini_template_path = os.path.join(BASE_DIR, "arquivados", "Gemini.md")
                roteiro_gemini_md = ""
                if os.path.exists(gemini_template_path):
                    try:
                        with open(gemini_template_path, 'r', encoding='utf-8') as f:
                            gemini_template_content = f.read()
                        
                        # Replace placeholders
                        roteiro_gemini_md = gemini_template_content.replace(
                            "`nome_do_projeto`", self.project_name or "Projeto Desconhecido"
                        ).replace(
                            "`artefato.md`", estado_atual.get('artefato_gerado', 'artefato_desconhecido.md')
                        )
                        print("[FLUXO] GEMINI.md dinâmico gerado.")
                    except IOError as e:
                        print(f"[ERRO] Falha ao ler o template GEMINI.md: {e}")
                        roteiro_gemini_md = "ERRO: Template GEMINI.md não encontrado ou ilegível!"
                else:
                    print("[AVISO] Template GEMINI.md não encontrado. Gerando roteiro básico.")
                    roteiro_gemini_md = f"# Roteiro para {self.project_name}\n\nArtefato gerado: {estado_atual.get('artefato_gerado', 'artefato_desconhecido.md')}\n\nAnalise este artefato e prossiga com o desenvolvimento."

                try:
                    # A IA não precisa mais gerar o roteiro, apenas o artefato final
                    # roteiro_gemini_md = executar_prompt_ia(prompt_roteiro) # REMOVED
                    salvar_artefatos_projeto(self.project_name, estado_atual, artefato_final, roteiro_gemini_md)
                    registrar_log(estado_atual['nome'], 'concluída', decisao=observation, resposta_agente=artefato_final, observacao=observation)
                    self._avancar_estado()
                    self._run_current_step()
                except IAExecutionError as e:
                    print(f"[ERRO FSM] Falha ao gerar roteiro para a próxima etapa: {e}")
                    self.last_preview_content = f"Erro ao gerar o roteiro: {e}"
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

    def setup_project(self, project_name, initial_preview_content=None, system_type=None):
        """Define o nome do projeto, sanitiza-o e armazena o preview inicial."""
        if not project_name or not project_name.strip():
            print("[ERRO] O nome do projeto é obrigatório para iniciar.")
            return self.get_status()
        
        # Sanitiza o nome do projeto para criar um nome de diretório seguro e consistente
        self.project_name = _sanitizar_nome(project_name)
        self.system_type = system_type # NEW: Store system_type
        self._save_project_context()
        
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
        if os.path.exists(LOG_PATH):
            os.remove(LOG_PATH)
        if os.path.exists(CHECKPOINT_PATH):
            os.remove(CHECKPOINT_PATH)
        if os.path.exists(PROJECT_CONTEXT_PATH):
            os.remove(PROJECT_CONTEXT_PATH)
        
        self._clean_temp_directory() # NEW: Clean temp directory

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