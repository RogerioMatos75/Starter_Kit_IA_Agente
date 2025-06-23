# Orquestrador FSM com leitura automática do guia de projeto, confirmação manual e registro de log

import time
import os
import json
from datetime import datetime
from guia_projeto import extrair_secoes, REQUIRED_SECTIONS, OUTPUT_FILES, SECTION_TITLES

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
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(log_entry)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)
    # Atualiza checkpoint
    checkpoint = {"ultimo_estado": etapa, "status": status, "data_hora": log_entry["data_hora"]}
    with open(CHECKPOINT_PATH, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, indent=2, ensure_ascii=False)

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

def executar_codigo_real(prompt, etapa_nome):
    print(f"\n[EXECUTOR] Prompt enviado para execução:\n{prompt}\n")
    codigo_gerado = f"print('Execução automática da etapa: {etapa_nome}')\nprint('Prompt usado:')\nprint('''{prompt}''')"
    projetos_dir = os.path.join("projetos")
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

class FSMOrquestrador:
    def __init__(self, estados):
        self.estados = estados
        self.estado_atual = 0

    def executar(self):
        # Retomada automática do ponto de parada
        logs = []
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                logs = json.load(f)
        etapas_concluidas = [log['etapa'] for log in logs if log['status'] == 'concluída']
        for i, estado in enumerate(self.estados):
            if estado['nome'] in etapas_concluidas:
                print(f"[Retomada] Etapa '{estado['nome']}' já concluída. Pulando...")
                continue
            print(f"\n=== Etapa {i+1}: {estado['nome']} ===")
            file_path = estado.get('guia')
            secoes = ""
            if file_path:
                file_name = os.path.basename(file_path)
                titulo = SECTION_TITLES.get(file_name, file_name)
                headers = REQUIRED_SECTIONS.get(file_name, [])
                secoes_dict = extrair_secoes(file_path, headers)
                print(f"\n# {titulo}")
                for header in headers:
                    print(f"\n{header}")
                    print(secoes_dict.get(header, '[Seção não encontrada ou vazia]'))
                print("\n" + ("-"*40) + "\n")
                secoes = "\n".join([f"{h}\n{secoes_dict.get(h, '')}" for h in headers])
            # Gera prompt automático para a etapa
            prompt = gerar_prompt_etapa(estado['nome'], secoes)
            resultado = executar_codigo_real(prompt, estado['nome'])
            print(f"Resultado da execução real:\n{resultado}")
            while True:
                confirm = input("Deseja prosseguir para a próxima etapa? (s/n): ").strip().lower()
                if confirm == 's':
                    obs = input("Observação ou decisão relevante (opcional): ")
                    registrar_log(estado['nome'], "concluída", "aprovada", resposta_agente=resultado, tarefa=estado['nome'], observacao=obs)
                    try:
                        import subprocess
                        subprocess.run(["python", "registrador_tarefas.py"], check=True)
                    except Exception as e:
                        print(f"[Aviso] Não foi possível gerar o PDF automaticamente: {e}")
                    break
                elif confirm == 'n':
                    obs = input("Descreva o motivo da pausa ou ajuste (opcional): ")
                    registrar_log(estado['nome'], "pausada", "revisão", resposta_agente=resultado, tarefa=estado['nome'], observacao=obs)
                    print("Execução pausada. Faça ajustes e confirme para continuar.")
                else:
                    print("Digite 's' para sim ou 'n' para não.")

def exemplo_acao():
    return "Ação executada com sucesso!"

if __name__ == "__main__":
    fsm = FSMOrquestrador([
        {"nome": "Coleta de requisitos", "acao": exemplo_acao, "guia": OUTPUT_FILES[0]},
        {"nome": "Definição de arquitetura", "acao": exemplo_acao, "guia": OUTPUT_FILES[1]},
        {"nome": "Regras de negócio", "acao": exemplo_acao, "guia": OUTPUT_FILES[2]},
        {"nome": "Fluxos de usuário", "acao": exemplo_acao, "guia": OUTPUT_FILES[3]},
        {"nome": "Backlog MVP", "acao": exemplo_acao, "guia": OUTPUT_FILES[4]},
        {"nome": "Implementação do sistema", "acao": exemplo_acao}
    ])
    fsm.executar()
