# Orquestrador FSM com leitura automática do guia de projeto, confirmação manual e registro de log

# Orquestrador FSM com leitura automática do guia de projeto, confirmação manual e registro de log

import time
import os
import shutil
import json
from datetime import datetime
from guia_projeto import extrair_secoes, REQUIRED_SECTIONS, SECTION_TITLES
from ia_executor import executar_prompt_ia, IAExecutionError

LOG_PATH = os.path.join("logs", "diario_execucao.json")
CHECKPOINT_PATH = os.path.join("logs", "proximo_estado.json")
PROJECT_CONTEXT_PATH = os.path.join("logs", "project_context.json")
CACHE_DIR = "cache"

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
    os.makedirs("logs", exist_ok=True)
    logs = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            try:
                content = f.read()
                if content:
                    data = json.loads(content)
                    # Acessa a lista 'execucoes' dentro do dicionário padrão
                    logs = data.get('execucoes', [])
            except json.JSONDecodeError:
                print(f"[Aviso] Arquivo de log '{LOG_PATH}' malformado. Um novo log será iniciado.")
    logs.append(log_entry)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        # Sempre salva no formato de dicionário padrão
        json.dump({"execucoes": logs}, f, indent=2, ensure_ascii=False)
    checkpoint = {"ultimo_estado": etapa, "status": status, "data_hora": log_entry["data_hora"]}
    with open(CHECKPOINT_PATH, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, indent=2, ensure_ascii=False)

def gerar_readme_projeto(project_name, etapa_nome, ai_generated_content, generated_file_name):
    """
    Gera o conteúdo do README.md para a pasta do projeto,
    com base na etapa atual e no conteúdo gerado pela IA.
    """
    readme_content = f"""# Projeto: {project_name}

Bem-vindo ao seu projeto, gerado pelo **Archon AI**!

Este diretório (`projetos/{project_name}/`) contém os artefatos gerados pela IA.

## Status Atual: Etapa "{etapa_nome}"

Nesta etapa, a IA gerou o seguinte artefato: **`{generated_file_name}`**.

## Próximos Passos (para o Desenvolvedor):

### 1. Revisar os Artefatos Gerados:
*   **`{generated_file_name}`**: Analise o conteúdo gerado pela IA. Este é o ponto de partida para a sua implementação ou para a sua compreensão do projeto.
*   **Documentos Conceituais**: Consulte os arquivos `.md` na pasta `output/` (na raiz do Starter Kit) para entender o contexto completo do projeto (plano de base, arquitetura, regras de negócio, etc.).

### 2. Implementação e Refinamento:
*   Use os artefatos gerados como base para desenvolver o código real, refinar a lógica ou planejar a próxima fase.

## Conteúdo Gerado nesta Etapa ({etapa_nome}):

"""
    return readme_content


def gerar_gemini_md(project_name, etapa_nome, generated_file_name):
    """
    Gera o conteúdo do Gemini.md para guiar o agente de IA.
    """
    gemini_content = f"""# Roteiro de Execução para o Agente Gemini

## Projeto: {project_name}
## Etapa Atual: {etapa_nome}

### Missão do Agente

Sua missão é continuar o desenvolvimento deste projeto com base nos artefatos gerados pelo Archon AI.

### Instruções Imediatas:

1.  **Analise o Artefato Principal:**
    *   O artefato gerado para esta etapa é: **`{generated_file_name}`**.
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

---
*Este roteiro foi gerado automaticamente pelo Archon AI. Siga as instruções para garantir a continuidade e o sucesso do projeto.*
"""
    return gemini_content

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
 
    # --- Lógica de Cache ---
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = _get_cache_path(project_name, etapa_nome)
    from_cache = False # Flag para indicar a origem do resultado

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
            # Salva o novo resultado no cache
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(codigo_gerado)
            print(f"[CACHE] Resultado salvo em cache: {cache_path}")
        except IAExecutionError as e:
            print(f"[ERRO FSM] Erro de execução da IA na etapa '{etapa_nome}': {e}")
            return f"Ocorreu um erro ao contatar a IA. Verifique o console do servidor para detalhes.\n\nErro: {e}", False
 
    try:
        # O código abaixo só será executado se a chamada à IA for bem-sucedida.
        sanitized_project_name = "".join(c for c in project_name if c.isalnum() or c in (" ", "_", "-")).rstrip()
        if not sanitized_project_name:
            sanitized_project_name = "projeto_sem_nome"

        projetos_dir = os.path.join("projetos", sanitized_project_name)
        os.makedirs(projetos_dir, exist_ok=True)

        # Usa o nome do artefato definido no workflow.json. Muito mais robusto!
        generated_file_name = etapa_atual.get('artefato_gerado')
        if not generated_file_name:
            # Fallback caso o campo não exista no JSON
            generated_file_name = f"{etapa_nome.replace(' ', '_').lower()}.txt"

        arquivo_gerado_path = os.path.join(projetos_dir, generated_file_name)

        with open(arquivo_gerado_path, "w", encoding="utf-8") as f:
            f.write(codigo_gerado)
        print(f"[INFO] Artefato salvo em: {arquivo_gerado_path}")

        # Gerar/Atualizar README.md na pasta do projeto
        readme_path = os.path.join(projetos_dir, "README.md")
        readme_content = gerar_readme_projeto(project_name, etapa_nome, codigo_gerado, generated_file_name)
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        print(f"[INFO] README.md atualizado em: {readme_path}")

        # Gerar/Atualizar Gemini.md na pasta do projeto
        gemini_path = os.path.join(projetos_dir, "Gemini.md")
        gemini_content = gerar_gemini_md(project_name, etapa_nome, generated_file_name)
        with open(gemini_path, "w", encoding="utf-8") as f:
            f.write(gemini_content)
        print(f"[INFO] Gemini.md atualizado em: {gemini_path}")

        # O preview será sempre o conteúdo gerado pela IA.
        saida = codigo_gerado
        return saida, from_cache

    except Exception as e:
        # Captura qualquer erro durante o salvamento dos arquivos
        error_message = f"Erro ao processar artefatos para a etapa '{etapa_nome}': {e}"
        print(f"[ERRO FSM] {error_message}")

def _invalidar_logs_posteriores(etapa_alvo, estados):
    """
    Remove do log todas as entradas de etapas posteriores à etapa_alvo.
    Isso é usado quando o usuário decide 'Voltar' no fluxo.
    """
    if not os.path.exists(LOG_PATH):
        return

    # Encontra o índice da etapa alvo para saber quais são as posteriores
    try:
        indice_alvo = [e['nome'] for e in estados].index(etapa_alvo)
    except ValueError:
        print(f"[AVISO] Etapa alvo '{etapa_alvo}' não encontrada no workflow para invalidação de logs.")
        return

    # Cria um conjunto com os nomes das etapas a serem removidas
    # A etapa alvo também é removida para ser re-executada
    etapas_a_remover = {estados[i]['nome'] for i in range(indice_alvo, len(estados))}
    print(f"[LOG] Invalidando logs para as etapas: {etapas_a_remover}")

    logs_atuais = []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            logs_atuais = data.get('execucoes', [])
        except (json.JSONDecodeError, TypeError):
            return # Não faz nada se o log estiver corrompido

    logs_validos = [log for log in logs_atuais if log.get('etapa') not in etapas_a_remover]
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump({"execucoes": logs_validos}, f, indent=2, ensure_ascii=False)
    print(f"[LOG] Logs posteriores a '{etapa_alvo}' foram removidos.")

class FSMOrquestrador:
    instance = None  # Singleton para acesso externo

    def __init__(self, estados):
        self.estados = estados
        self.current_step_index = 0
        self.last_preview_content = INITIAL_PREVIEW_CONTENT
        self.is_finished = False
        self.last_step_from_cache = False
        self.project_name = None
        self._load_progress()
        FSMOrquestrador.instance = self

    def _load_progress(self):
        """Lê o log para encontrar a última etapa concluída e retomar o progresso."""
        logs = []
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                try:
                    content = f.read()
                    if content:
                        data = json.loads(content)
                        # Acessa a lista 'execucoes' dentro do dicionário padrão
                        logs = data.get('execucoes', [])
                except (json.JSONDecodeError, TypeError):
                    pass
        etapas_concluidas = {log['etapa'] for log in logs if log.get('status') == 'concluída'}
        for i, estado in enumerate(self.estados):
            if estado['nome'] not in etapas_concluidas:
                self.current_step_index = i
                return
        self.current_step_index = len(self.estados)
        self.is_finished = True

    def get_status(self):
        """Prepara o dicionário de status para a API."""
        timeline = []
        for i, estado in enumerate(self.estados):
            status = "pending"
            if i < self.current_step_index:
                status = "completed"
            elif i == self.current_step_index and not self.is_finished:
                status = "in-progress"
            timeline.append({"name": estado['nome'], "status": status})
        current_step_name = "Projeto Finalizado"
        # A etapa atual só deve ter um nome do workflow se o projeto JÁ FOI INICIADO
        if self.project_name and not self.is_finished:
            current_step_name = self.estados[self.current_step_index]['nome']
        elif self.is_finished:
            self.last_preview_content = "Todas as etapas foram concluídas com sucesso!"
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
        """Configura o nome do projeto e executa a primeira etapa para gerar o preview inicial."""
        if not project_name or not project_name.strip():
            print("[ERRO] O nome do projeto é obrigatório para iniciar.")
            return self.get_status()
        self.project_name = project_name.strip()
        print(f"[PROJETO] Nome do projeto definido como: '{self.project_name}'")
        self._run_current_step()
        return self.get_status()

    def process_action(self, action, observation="", project_name=None):
        """Processa uma ação vinda da UI e retorna o novo estado."""
        # Restaura o nome do projeto a partir do parâmetro, se não estiver definido
        if project_name and not self.project_name:
            self.project_name = project_name
            print(f"[PROJETO] Contexto do projeto restaurado para: '{self.project_name}'")

        if self.is_finished or self.project_name is None:
            # Adiciona uma verificação para o caso de a ação ser um 'reset'
            if action == 'reset':
                return self.reset_project()
            return self.get_status()
        estado_atual = self.estados[self.current_step_index]
        action_map = {'approve': 's', 'repeat': 'r', 'back': 'v', 'pause': 'p'}
        if action_map.get(action) == 's':
            registrar_log(estado_atual['nome'], "concluída", "aprovada", resposta_agente=self.last_preview_content, observacao=observation)
            self.current_step_index += 1
            if self.current_step_index >= len(self.estados):
                self.is_finished = True
            else:
                self._run_current_step()
        elif action_map.get(action) == 'r':
            self._run_current_step(use_cache=False)
        elif action_map.get(action) == 'v':
            if self.current_step_index > 0:
                self.current_step_index -= 1
                etapa_alvo = self.estados[self.current_step_index]['nome']
                _invalidar_logs_posteriores(etapa_alvo, self.estados)
                self._run_current_step()
        elif action_map.get(action) == 'p':
            registrar_log(estado_atual['nome'], "pausada", "revisão manual", resposta_agente=self.last_preview_content, observacao=observation)
        return self.get_status()

    def reset_project(self):
        """Reseta o projeto para o estado inicial, limpando logs e arquivos gerados."""
        print("\n[RESET] Iniciando reset do projeto...")
        if os.path.exists(LOG_PATH):
            os.remove(LOG_PATH)
            print(f"[RESET] Arquivo de log '{LOG_PATH}' removido.")
        if os.path.exists(CHECKPOINT_PATH):
            os.remove(CHECKPOINT_PATH)
            print(f"[RESET] Arquivo de checkpoint '{CHECKPOINT_PATH}' removido.")
        if os.path.exists(CACHE_DIR):
            shutil.rmtree(CACHE_DIR)
            print(f"[RESET] Pasta de cache '{CACHE_DIR}' e seu conteúdo removidos.")
        projetos_dir = "projetos"
        if os.path.exists(projetos_dir):
            shutil.rmtree(projetos_dir)
            print(f"[RESET] Pasta de projetos '{projetos_dir}' e seu conteúdo removidos.")
        os.makedirs(projetos_dir, exist_ok=True)
        self.current_step_index = 0
        self.last_preview_content = INITIAL_PREVIEW_CONTENT
        self.is_finished = False
        self.project_name = None
        print("[RESET] Projeto resetado com sucesso. Pronto para um novo início!")
        return self.get_status()
