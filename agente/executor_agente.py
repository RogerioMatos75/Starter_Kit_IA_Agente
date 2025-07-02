import os
import argparse
import re
import json
import sys

# Adiciona o diretório raiz ao sys.path para encontrar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ia_executor import executar_prompt_ia, IAExecutionError

class AgentExecutionError(Exception):
    """Exceção customizada para erros na execução do agente."""
    pass

def gerar_prompt_plano_acao(artifact_content: str, artifact_name: str) -> str:
    """
    Cria um prompt para a IA gerar um plano de ação estruturado em JSON.
    """
    return f"""Você é um arquiteto de software e engenheiro sênior.
Sua tarefa é analisar o conteúdo de um artefato de projeto e convertê-lo em um plano de ação estruturado em JSON.

O plano deve conter uma lista de ações, que podem ser:
- `create_file`: Para criar um novo arquivo.
- `replace_content`: Para substituir o conteúdo de um arquivo existente.
- `run_command`: Para executar um comando no terminal.

**Estrutura do JSON de Saída:**
```json
{{
  "plan": [
    {{
      "action": "create_file",
      "file_path": "caminho/para/o/arquivo.py",
      "content": "conteúdo do arquivo..."
    }},
    {{
      "action": "replace_content",
      "file_path": "caminho/existente/arquivo.py",
      "old_string": "bloco de código a ser substituído",
      "new_string": "novo bloco de código"
    }},
    {{
      "action": "run_command",
      "command": "pip install -r requirements.txt"
    }}
  ]
}}
```

**Artefato a ser Analisado:**
- **Nome do Arquivo:** `{artifact_name}`
- **Conteúdo:**
---
{artifact_content}
---

Analise o conteúdo acima e gere **APENAS** o JSON com o plano de ação. Não inclua nenhuma outra explicação ou texto fora do JSON.
"""

def parse_gemini_md(content: str) -> dict:
    """
    Analisa o conteúdo de um arquivo Gemini.md para extrair as instruções.
    Retorna um dicionário com as ações a serem tomadas.
    """
    instructions = {}
    try:
        # Extrai o nome do artefato principal usando uma expressão regular
        artifact_match = re.search(r"O artefato gerado para esta etapa é: \*\*`([^`]+)`\*\*.", content)
        if artifact_match:
            instructions['artifact_file'] = artifact_match.group(1)
        else:
            instructions['artifact_file'] = None

        instructions['raw_content'] = content
        
        print(f"[AGENTE] Roteiro analisado. Artefato principal identificado: {instructions.get('artifact_file')}")
        return instructions
    except Exception as e:
        raise AgentExecutionError(f"Erro ao analisar o Gemini.md: {e}")

def execute_action_plan(project_path: str, plan: list, default_api):
    """
    Executa as ações definidas no plano gerado pela IA.
    """
    print("\n--- Iniciando Execução do Plano de Ação ---")
    for i, action_item in enumerate(plan):
        action_type = action_item.get("action")
        print(f"\n[AÇÃO {i+1}/{len(plan)}] - {action_type.upper()}")

        try:
            if action_type == "create_file":
                file_path = os.path.join(project_path, action_item["file_path"])
                content = action_item["content"]
                
                # Garante que o diretório exista antes de criar o arquivo
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  -> Arquivo criado/sobrescrito: {file_path}")

            elif action_type == "run_command":
                command = action_item["command"]
                # Lógica para rodar o servidor em segundo plano
                if "gunicorn" in command or ("python" in command and "app.py" in command):
                    command += " &"
                    print(f"  -> Executando comando em segundo plano: {command}")
                else:
                    print(f"  -> Executando comando: {command}")
                
                # A ferramenta `run_shell_command` precisa ser chamada aqui
                result = default_api.run_shell_command(command=command, directory=project_path)
                print(f"     -> Resultado: {result}")

            else:
                print(f"  -> [AVISO] Ação desconhecida ou não implementada: {action_type}")

        except KeyError as e:
            print(f"  -> [ERRO] Ação malformada. Falta a chave: {e}")
        except Exception as e:
            print(f"  -> [ERRO] Falha ao executar a ação: {e}")

def execute_mission(project_path: str, default_api):
    """
    Função principal que executa a missão do agente para um determinado projeto.
    """
    print(f"--- Iniciando Missão do Agente para o Projeto em: {project_path} ---")

    # 1. Localizar e ler o roteiro Gemini.md
    gemini_md_path = os.path.join(project_path, "Gemini.md")
    if not os.path.exists(gemini_md_path):
        raise AgentExecutionError(f"Arquivo 'Gemini.md' não encontrado em: {project_path}")
    
    print(f"[AGENTE] Lendo o roteiro de execução: {gemini_md_path}")
    with open(gemini_md_path, 'r', encoding='utf-8') as f:
        gemini_md_content = f.read()

    # 2. Interpretar as instruções do roteiro
    try:
        instructions = parse_gemini_md(gemini_md_content)
    except AgentExecutionError as e:
        print(f"[ERRO] {e}")
        return

    # 3. Ler o artefato principal
    artifact_to_read = instructions.get('artifact_file')
    if not artifact_to_read:
        print("[AGENTE] Nenhum artefato principal encontrado no roteiro. Missão concluída por enquanto.")
        return

    artifact_path = os.path.join(project_path, artifact_to_read)
    if not os.path.exists(artifact_path):
        raise AgentExecutionError(f"Artefato principal '{artifact_path}' não encontrado.")

    print(f"[AGENTE] Lendo o conteúdo do artefato: {artifact_path}")
    with open(artifact_path, 'r', encoding='utf-8') as f:
        artifact_content = f.read()

    # 4. Gerar plano de ação com a IA
    print("\n[AGENTE] Solicitando plano de ação para a IA...")
    prompt = gerar_prompt_plano_acao(artifact_content, artifact_to_read)
    
    try:
        ia_response = executar_prompt_ia(prompt)
        cleaned_response = re.sub(r"^`{3}(json)?|`{3}$", "", ia_response.strip())
        action_plan = json.loads(cleaned_response)
        
        print("\n--- Plano de Ação Recebido da IA ---")
        print(json.dumps(action_plan, indent=2, ensure_ascii=False))
        print("-------------------------------------")

        # 5. Executar o plano de ação
        execute_action_plan(project_path, action_plan.get("plan", []), default_api)

    except IAExecutionError as e:
        print(f"[ERRO IA] Falha ao gerar o plano de ação: {e}")
    except json.JSONDecodeError as e:
        print(f"[ERRO JSON] A resposta da IA não é um JSON válido: {e}")
        print(f"Resposta recebida:\n{ia_response}")

    print("\n--- Missão do Agente Concluída ---")


