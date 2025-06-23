# Orquestrador FSM com leitura automática do guia de projeto, confirmação manual e registro de log

import time
import os
import json
from datetime import datetime
from guia_projeto import extrair_secoes, REQUIRED_SECTIONS, OUTPUT_FILES, SECTION_TITLES
from valida_output import run_validation as validar_base_conhecimento

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
        self.estado_atual = 0

    def executar(self):
        # ETAPA 0: Validação da Base de Conhecimento
        print("--- Iniciando validação da Base de Conhecimento ---")
        if not validar_base_conhecimento():
            print("\n[FALHA] A execução do orquestrador foi interrompida devido a falhas na validação.")
            print("Por favor, corrija os arquivos na pasta 'output/' e tente novamente.")
            return  # Interrompe a execução
        print("-" * 50)
        print("Validação concluída com sucesso. Iniciando orquestrador FSM...\n")

        # Retomada automática do ponto de parada
        i = 0
        logs = []
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                try:
                    content = f.read()
                    if content: # Garante que o arquivo não está vazio
                        data = json.loads(content)
                        if isinstance(data, dict) and 'execucoes' in data:
                            logs = data['execucoes']
                        elif isinstance(data, list):
                            logs = data
                except json.JSONDecodeError:
                    print(f"[Aviso] Arquivo de log '{LOG_PATH}' malformado. Iniciando sem histórico.")

        while i < len(self.estados):
            etapas_concluidas = {log['etapa'] for log in logs if log.get('status') == 'concluída'}
            estado = self.estados[i]

            if estado['nome'] in etapas_concluidas:
                print(f"[Retomada] Etapa '{estado['nome']}' já foi concluída. Pulando...")
                i += 1
                continue

            print(f"\n=== Etapa {i + 1}/{len(self.estados)}: {estado['nome']} ===")
            # ... (código para extrair seções e gerar prompt) ...
            # (O código existente aqui dentro permanece o mesmo)
            # ...
            while True: # Loop de interação com o usuário
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
                
                prompt = gerar_prompt_etapa(estado['nome'], secoes)
                resultado = executar_codigo_real(prompt, estado['nome'])
                print(f"Resultado da execução:\n{resultado}")

                acao = input("\nEscolha uma ação: (s)eguir, (r)epetir, (v)oltar, (p)ausar: ").strip().lower()

                if acao == 's':
                    obs = input("Observação ou decisão relevante (opcional): ")
                    registrar_log(estado['nome'], "concluída", "aprovada", resposta_agente=resultado, observacao=obs)
                    logs.append({"etapa": estado['nome'], "status": "concluída"}) # Atualiza log em memória
                    i += 1
                    break
                elif acao == 'r':
                    print("Repetindo a etapa atual...")
                    continue # Reinicia o loop de interação para a mesma etapa
                elif acao == 'p':
                    obs = input("Descreva o motivo da pausa (opcional): ")
                    registrar_log(estado['nome'], "pausada", "revisão manual", resposta_agente=resultado, observacao=obs)
                    print("Execução pausada. Rode o script novamente para continuar.")
                    return # Encerra o programa
                elif acao == 'v':
                    print("Etapas anteriores concluídas:")
                    etapas_validas = [e['nome'] for e in self.estados[:i]]
                    if not etapas_validas:
                        print("Nenhuma etapa anterior para voltar.")
                        continue
                    for idx, nome_etapa in enumerate(etapas_validas):
                        print(f"  {idx + 1}: {nome_etapa}")
                    try:
                        escolha = int(input("Digite o número da etapa para a qual deseja voltar: ")) - 1
                        if 0 <= escolha < len(etapas_validas):
                            etapa_alvo = etapas_validas[escolha]
                            _invalidar_logs_posteriores(etapa_alvo, self.estados)
                            i = escolha # Define o índice para a etapa escolhida
                            break # Sai do loop de interação e vai para a etapa escolhida
                        else:
                            print("Escolha inválida.")
                    except ValueError:
                        print("Entrada inválida. Digite um número.")
                else:
                    print("Ação inválida. Escolha 's', 'r', 'v' ou 'p'.")
            
            while True:
                # Este bloco foi movido e integrado ao loop de interação acima.
                # Pode ser removido.
                break

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
