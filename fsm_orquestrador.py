# Orquestrador FSM com leitura automática do guia de projeto, confirmação manual e registro de log

import time
import os
import shutil
import re
import json
import hashlib
from datetime import datetime
from guia_projeto import extrair_secoes, REQUIRED_SECTIONS, SECTION_TITLES
from auditoria_seguranca import auditoria_global
from ia_executor import executar_prompt_ia, IAExecutionError
from gerenciador_artefatos import salvar_artefatos_projeto

# --- CONFIGURAÇÃO DE CAMINHOS ABSOLUTOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_PATH = os.path.join(BASE_DIR, "logs", "diario_execucao.json")
CHECKPOINT_PATH = os.path.join(BASE_DIR, "logs", "proximo_estado.json")
PROJECT_CONTEXT_PATH = os.path.join(BASE_DIR, "logs", "project_context.json")
ARCHIVE_DIR = os.path.join(BASE_DIR, "projetos", "arquivados")
CACHE_DIR = os.path.join(BASE_DIR, "cache")

# Tenta importar o gerador de PDF, mas não quebra se não estiver disponível
try:
    from relatorios import gerar_log_pdf
except ImportError:
    print("[AVISO] Módulo 'reportlab' não encontrado. A geração de PDF estará desativada. Instale com: pip install reportlab")
    gerar_log_pdf = None

INITIAL_PREVIEW_CONTENT = """# O Projeto Ainda Não Foi Iniciado

Para começar, preciso de algumas informações essenciais. Por favor, siga os passos na interface:

**1. (Opcional) Baixe os Templates:**
Use o botão "Download Template de Documentos" para obter os arquivos `.md` que servirão como base de conhecimento para a IA.

**2. (Opcional) Faça o Upload da Base de Conhecimento:**
Após preencher os templates com os detalhes do seu projeto (objetivo, arquitetura, regras de negócio, etc.), faça o upload deles.

**3. Defina o Nome do Projeto:**
Dê um nome claro e descritivo para a pasta onde os artefatos gerados serão salvos.

**4. Inicie o Projeto:**
Clique em "Iniciar Projeto" para que o Archon comece a trabalhar na primeira etapa do workflow.

---
*Estou pronto para começar assim que tivermos esses detalhes definidos.*
"""

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

    if gerar_log_pdf:
        pdf_log_path = os.path.join(os.path.dirname(LOG_PATH), "log_execucao.pdf")
        gerar_log_pdf(logs, pdf_log_path)

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

def _get_cache_path(project_name, etapa_nome):
    """Gera um caminho de arquivo seguro para o cache."""
    sanitized_project = "".join(c for c in project_name if c.isalnum() or c in ("_", "-")).rstrip()
    sanitized_etapa = "".join(c for c in etapa_nome if c.isalnum() or c in ("_", "-")).rstrip()
    filename = f"{sanitized_project}_{sanitized_etapa}.cache"
    return os.path.join(CACHE_DIR, filename)

def executar_codigo_real(prompt, etapa_atual, project_name, use_cache=True):
    """Executa a chamada à IA, salva o artefato e o README, e retorna o conteúdo para preview."""
    etapa_nome = etapa_atual['nome']
    print(f"\n[EXECUTOR] Prompt enviado para a IA para a etapa: {etapa_nome}")
 
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = _get_cache_path(project_name, etapa_nome)
    from_cache = False

    if use_cache and os.path.exists(cache_path):
        print(f"[CACHE] Resultado encontrado em cache para a etapa '{etapa_nome}'. Usando cache.")
        with open(cache_path, "r", encoding="utf-8") as f:
            codigo_gerado = f.read()
        from_cache = True
    else:
        if not use_cache:
            print("[CACHE] Forçando nova execução (sem cache) para a etapa.")
        try:
            codigo_gerado = executar_prompt_ia(prompt)
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(codigo_gerado)
            print(f"[CACHE] Resultado salvo em cache: {cache_path}")
        except IAExecutionError as e:
            print(f"[ERRO FSM] Erro de execução da IA na etapa '{etapa_nome}': {e}")
            return f"Ocorreu um erro ao contatar a IA. Verifique o console do servidor para detalhes.\n\nErro: {e}", False
 
    try:
        arquivo_gerado_path = salvar_artefatos_projeto(project_name, etapa_atual, codigo_gerado)
        auditoria_global.log_artefacto_gerado(
            project_name=project_name,
            file_path=arquivo_gerado_path,
            file_content=codigo_gerado
        )
        return codigo_gerado, from_cache
    except Exception as e:
        error_message = f"Erro ao processar artefatos para a etapa '{etapa_nome}': {e}"
        print(f"[ERRO FSM] {error_message}")
        return f"Erro ao salvar artefatos: {error_message}", False
    
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
        self.last_step_from_cache = False
        self.project_name = None
        self._load_project_context()
        self._load_progress()
        FSMOrquestrador.instance = self

    def _load_project_context(self):
        """Carrega o nome do último projeto ativo para persistir entre reinicializações."""
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
        """Salva o nome do projeto atual para persistência."""
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
            self.last_step_from_cache = False
        else:
            self.is_finished = True

    def _calculate_file_hash(self, file_path):
        """Calcula o hash SHA-256 de um único arquivo."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _hash_directory(self, directory_path):
        """Calcula um hash consolidado para um diretório inteiro."""
        hashes = []
        for root, _, files in os.walk(directory_path):
            for file in sorted(files):
                file_path = os.path.join(root, file)
                file_hash = self._calculate_file_hash(file_path)
                relative_path = os.path.relpath(file_path, directory_path)
                hashes.append(f"{file_hash}  {relative_path.replace(os.sep, '/')}")

        manifest_content = "\n".join(sorted(hashes))
        final_hash = hashlib.sha256(manifest_content.encode('utf-8')).hexdigest()
        
        manifest_path = os.path.join(directory_path, "manifest.txt")
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)
        return final_hash

    def _archive_project(self):
        """Arquiva o projeto atual antes de resetar."""
        if not self.project_name:
            print("[ARQUIVAMENTO] Nenhum projeto ativo para arquivar.")
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_project_name = f"{self.project_name}_{timestamp}"
        target_archive_dir = os.path.join(ARCHIVE_DIR, archive_project_name)

        os.makedirs(target_archive_dir, exist_ok=True)
        print(f"[ARQUIVAMENTO] Criando arquivo morto em: {target_archive_dir}")

        source_project_dir = os.path.join(BASE_DIR, "projetos", self.project_name)
        if os.path.exists(source_project_dir):
            shutil.copytree(source_project_dir, os.path.join(target_archive_dir, "artefatos_gerados"))
            print(f"[ARQUIVAMENTO] Artefatos do projeto '{self.project_name}' copiados.")

        if os.path.exists(LOG_PATH):
            shutil.copy2(LOG_PATH, os.path.join(target_archive_dir, "log_final_execucao.json"))
            print(f"[ARQUIVAMENTO] Log de execução copiado.")

        output_dir_abs = os.path.join(BASE_DIR, "output")
        if os.path.exists(output_dir_abs):
            shutil.copytree(output_dir_abs, os.path.join(target_archive_dir, "base_conhecimento_usada"))
            print(f"[ARQUIVAMENTO] Base de conhecimento (output) copiada.")

        integrity_hash = None
        try:
            print(f"[ARQUIVAMENTO] Calculando hash de integridade para {target_archive_dir}...")
            integrity_hash = self._hash_directory(target_archive_dir)
            hash_file_path = os.path.join(target_archive_dir, "integridade_sha256.txt")
            with open(hash_file_path, "w", encoding="utf-8") as f:
                f.write(f"SHA-256: {integrity_hash}\n")
            print(f"[ARQUIVAMENTO] Hash de integridade salvo em: {hash_file_path}")
        except Exception as e:
            print(f"[ERRO] Falha ao gerar o hash de integridade: {e}")

        return {
            "path": target_archive_dir,
            "hash": integrity_hash
        }

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
                "from_cache": self.last_step_from_cache
            },
            "actions": {
                "can_go_back": self.current_step_index > 0,
                "is_finished": self.is_finished,
            },
            "project_name": self.project_name,
        }

    def _run_current_step(self, use_cache=True):
        """Executa a lógica da etapa atual e atualiza o preview."""
        if self.is_finished or self.project_name is None:
            return
        estado = self.estados[self.current_step_index]
        print(f"\n=== Executando Etapa: {estado['nome']} para o projeto '{self.project_name}' ===")
        
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
        resultado, from_cache = executar_codigo_real(prompt, estado, self.project_name, use_cache=use_cache)
        self.last_preview_content = resultado
        self.last_step_from_cache = from_cache
        print(f"Resultado da execução (preview):\n{resultado[:500]}...")

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
            self._run_current_step(use_cache=False)
        
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
        """Reseta o projeto para o estado inicial."""
        print("\n[RESET] Iniciando reset do projeto...")
        
        archive_info = self._archive_project()

        if os.path.exists(LOG_PATH):
            os.remove(LOG_PATH)
            print(f"[RESET] Arquivo de log '{LOG_PATH}' removido.")
        if os.path.exists(CHECKPOINT_PATH):
            os.remove(CHECKPOINT_PATH)
            print(f"[RESET] Arquivo de checkpoint '{CHECKPOINT_PATH}' removido.")
        if os.path.exists(PROJECT_CONTEXT_PATH):
            os.remove(PROJECT_CONTEXT_PATH)
            print(f"[RESET] Arquivo de contexto '{PROJECT_CONTEXT_PATH}' removido.")
        if os.path.exists(CACHE_DIR):
            shutil.rmtree(CACHE_DIR)
            print(f"[RESET] Pasta de cache '{CACHE_DIR}' removida.")
        
        projetos_dir = os.path.join(BASE_DIR, "projetos")
        if os.path.exists(projetos_dir):
            shutil.rmtree(projetos_dir)
            print(f"[RESET] Pasta de trabalho de projetos '{os.path.basename(projetos_dir)}' removida.")
        
        os.makedirs(projetos_dir, exist_ok=True)
        os.makedirs(ARCHIVE_DIR, exist_ok=True)

        output_dir = os.path.join(BASE_DIR, "output")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            print(f"[RESET] Pasta de output '{os.path.basename(output_dir)}' removida.")
        os.makedirs(output_dir, exist_ok=True)
        
        self.current_step_index = 0
        self.last_preview_content = INITIAL_PREVIEW_CONTENT
        self.is_finished = False
        self.project_name = None
        print("[RESET] Projeto resetado com sucesso.")
        
        status = self.get_status()
        if archive_info:
            status['archive_info'] = archive_info
        return status