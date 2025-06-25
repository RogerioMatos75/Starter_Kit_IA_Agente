# Orquestrador FSM com leitura automática do guia de projeto, confirmação manual e registro de log

import time
import os
import json
from datetime import datetime
from guia_projeto import extrair_secoes, REQUIRED_SECTIONS, OUTPUT_FILES, SECTION_TITLES
from valida_output import run_validation as validar_base_conhecimento
from ia_executor import executar_prompt_ia

LOG_PATH = os.path.join("logs", "diario_execucao.json")
CHECKPOINT_PATH = os.path.join("logs", "proximo_estado.json")

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
                if content: # Garante que o arquivo não está vazio
                    data = json.loads(content)
                    # Lida com o formato de objeto {"execucoes": []} ou de lista []
                    if isinstance(data, dict) and 'execucoes' in data:
                        logs = data['execucoes']
                    elif isinstance(data, list):
                        logs = data
            except json.JSONDecodeError:
                print(f"[Aviso] Arquivo de log '{LOG_PATH}' malformado. Um novo log será iniciado.")
    logs.append(log_entry)
    # A partir daqui, o log será sempre salvo como uma lista simples, padronizando o arquivo.
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)
    # Atualiza checkpoint
    checkpoint = {"ultimo_estado": etapa, "status": status, "data_hora": log_entry["data_hora"]}
    with open(CHECKPOINT_PATH, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, indent=2, ensure_ascii=False)

def gerar_readme_projeto(project_name, etapa_nome, ai_generated_content, generated_file_name):
    """
    Gera o conteúdo do README.md para a pasta do projeto,
    com base na etapa atual e no conteúdo gerado pela IA.
    """
    readme_content = f"""# Projeto: {project_name}

Bem-vindo ao seu projeto, gerado pelo **Starter Kit: Agente de IA com Workflow Supervisionado**!

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

```
{ai_generated_content}
```
"""
    return readme_content

# Carregar templates customizados de prompt, se existirem
PROMPT_TEMPLATES_PATH = os.path.join("prompt_templates.json")
def carregar_templates():
    if os.path.exists(PROMPT_TEMPLATES_PATH):
        try:
            with open(PROMPT_TEMPLATES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Aviso] Erro ao carregar templates customizados: {e}. Usando templates padrão.")
    return {}
TEMPLATES_CUSTOM = carregar_templates()

def gerar_prompt_etapa(etapa, secoes):
    # Permite customização via arquivo externo
    template = TEMPLATES_CUSTOM.get(etapa)
    if template:
        try:
            return template.replace('{secoes}', secoes)
        except Exception as e:
            print(f"[Aviso] Erro ao aplicar template customizado: {e}. Usando template padrão.")
    if etapa == "Coleta de requisitos":
        return f"Com base no objetivo, visão, público-alvo e escopo abaixo, gere um resumo do domínio do projeto.\n{secoes}"
    if etapa == "Definição de arquitetura":
        return f"Com base na arquitetura, tecnologias, integrações e fluxos principais abaixo, gere um esqueleto de arquitetura para o projeto.\n{secoes}"
    if etapa == "Regras de negócio":
        return f"Liste e explique as regras de negócio, restrições, exceções e decisões abaixo.\n{secoes}"
    if etapa == "Fluxos de usuário":
        return f"Descreva os fluxos de usuário, navegação e interações abaixo.\n{secoes}"
    if etapa == "Backlog MVP":
        return f"Com base nas funcionalidades, critérios de aceitação e priorização abaixo, gere um backlog inicial para o MVP.\n{secoes}"
    if etapa == "Implementação do sistema":
        return f"Implemente o código real para o sistema, considerando todas as informações anteriores.\n{secoes}"
    return f"Prompt genérico para etapa {etapa}.\n{secoes}"

# Simulação de executor de código real
# Substitua por integração com IA ou engine real

def executar_codigo_real(prompt, etapa_nome, project_name):
    print(f"\n[EXECUTOR] Prompt enviado para a IA para a etapa: {etapa_nome}\n")
    # Substitui a simulação pela chamada real à IA
    codigo_gerado = executar_prompt_ia(prompt)

    # Sanitiza o nome do projeto para ser um nome de pasta válido
    sanitized_project_name = "".join(
        c for c in project_name if c.isalnum() or c in (" ", "_", "-")
    ).rstrip()
    if not sanitized_project_name:
        sanitized_project_name = "projeto_sem_nome"
    projetos_dir = os.path.join("projetos", sanitized_project_name)
    os.makedirs(projetos_dir, exist_ok=True)
    arquivo_codigo = os.path.join(projetos_dir, f"{etapa_nome.replace(' ', '_').lower()}.py")
    try:
        with open(arquivo_codigo, "w", encoding="utf-8") as f:
            f.write(codigo_gerado)
    except Exception as e:
        print(f"[Erro] Não foi possível salvar o código gerado: {e}")
        return f"[Erro ao salvar código]: {e}"
    # Salvar prompt usado
    try:
        with open(os.path.join(projetos_dir, f"{etapa_nome.replace(' ', '_').lower()}_prompt.txt"), "w", encoding="utf-8") as f:
            f.write(prompt)
    except Exception as e:
        print(f"[Erro] Não foi possível salvar o prompt: {e}")
    # Executar o código Python gerado
    try:
        import subprocess
        resultado = subprocess.run(["python", arquivo_codigo], capture_output=True, text=True, check=True)
        saida = resultado.stdout
    except subprocess.CalledProcessError as e:
        saida = f"[Erro na execução do código]: {e}\nSaída de erro:\n{e.stderr}"
    except Exception as e:
        saida = f"[Erro inesperado na execução do código]: {e}"
    return saida

def _invalidar_logs_posteriores(etapa_alvo, todas_etapas):
    """Apaga do log todas as entradas de etapas que vêm depois da etapa_alvo."""
    try:
        nomes_etapas = [e['nome'] for e in todas_etapas]
        if etapa_alvo not in nomes_etapas:
            return

        indice_alvo = nomes_etapas.index(etapa_alvo)
        etapas_a_manter = set(nomes_etapas[:indice_alvo + 1])

        logs = []
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                logs = json.load(f)

        logs_filtrados = [log for log in logs if log.get('etapa') in etapas_a_manter]

        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(logs_filtrados, f, indent=2, ensure_ascii=False)
        print(f"[Controle de Fluxo] Histórico redefinido para a etapa '{etapa_alvo}'.")
    except Exception as e:
        print(f"[Erro] Falha ao invalidar logs: {e}")


class FSMOrquestrador:
    def __init__(self, estados):
        self.estados = estados
        self.current_step_index = 0
        self.last_preview_content = "O projeto ainda não foi iniciado. Defina um nome para o projeto e clique em 'Iniciar Projeto' para começar."
        self.is_finished = False
        self.project_name = None
        self._load_progress()

    def _load_progress(self):
        """Lê o log para encontrar a última etapa concluída e retomar o progresso."""
        logs = []
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                try:
                    content = f.read()
                    if content:
                        data = json.loads(content)
                        logs = data['execucoes'] if isinstance(data, dict) and 'execucoes' in data else data
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
        if not self.is_finished:
            current_step_name = self.estados[self.current_step_index]['nome']
        else:
            self.last_preview_content = "Todas as etapas foram concluídas com sucesso!"

        return {
            "timeline": timeline,
            "current_step": {
                "name": current_step_name,
                "preview_content": self.last_preview_content,
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
        file_path = estado.get('guia')
        secoes = ""
        if file_path:
            file_name = os.path.basename(file_path)
            titulo = SECTION_TITLES.get(file_name, file_name)
            headers = REQUIRED_SECTIONS.get(file_name, [])
            secoes_dict = extrair_secoes(file_path, headers)
            secoes = "\n".join([f"{h}\n{secoes_dict.get(h, '')}" for h in headers])
        prompt = gerar_prompt_etapa(estado['nome'], secoes)
        resultado = executar_codigo_real(prompt, estado['nome'], self.project_name)
        self.last_preview_content = resultado
        print(f"Resultado da execução:\n{resultado}")

    def setup_project(self, project_name):
        """Configura o nome do projeto e executa a primeira etapa para gerar o preview inicial."""
        if not project_name or not project_name.strip():
            print("[ERRO] O nome do projeto é obrigatório para iniciar.")
            return self.get_status() # Retorna status atual sem mudanças
        self.project_name = project_name.strip()
        print(f"[PROJETO] Nome do projeto definido como: '{self.project_name}'")
        self._run_current_step()
        return self.get_status()

    def process_action(self, action, observation="", project_name=None):
        """Processa uma ação vinda da UI e retorna o novo estado."""
        if self.is_finished or self.project_name is None:
            return self.get_status()

        estado_atual = self.estados[self.current_step_index]
        action_map = {'approve': 's', 'repeat': 'r', 'back': 'v', 'pause': 'p'}
        
        if action_map.get(action) == 's':
            self._run_current_step() # Executa a etapa atual com o nome do projeto já definido
            registrar_log(estado_atual['nome'], "concluída", "aprovada", resposta_agente=self.last_preview_content, observacao=observation)
            self.current_step_index += 1
            if self.current_step_index >= len(self.estados):
                self.is_finished = True
            else:
                self._run_current_step()
        elif action_map.get(action) == 'r':
            self._run_current_step()
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
        # Limpar arquivos de log
        if os.path.exists(LOG_PATH):
            os.remove(LOG_PATH)
            print(f"[RESET] Arquivo de log '{LOG_PATH}' removido.")
        if os.path.exists(CHECKPOINT_PATH):
            os.remove(CHECKPOINT_PATH)
            print(f"[RESET] Arquivo de checkpoint '{CHECKPOINT_PATH}' removido.")

        # Limpar a pasta 'projetos/'
        projetos_dir = os.path.join("projetos")
        if os.path.exists(projetos_dir):
            import shutil
            shutil.rmtree(projetos_dir)
            print(f"[RESET] Pasta de projetos '{projetos_dir}' e seu conteúdo removidos.")
        os.makedirs(projetos_dir, exist_ok=True) # Recria a pasta vazia

        # Resetar o estado interno do FSM
        self.current_step_index = 0
        self.last_preview_content = "O projeto ainda não foi iniciado. Defina um nome para o projeto e clique em 'Iniciar Projeto' para começar."
        self.is_finished = False
        self.project_name = None
        print("[RESET] Projeto resetado com sucesso. Pronto para um novo início!")
        return self.get_status() # Retorna o status inicial
