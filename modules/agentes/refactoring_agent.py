# modules/agentes/refactoring_agent.py

import os
from ia_executor import executar_prompt_ia, IAExecutionError
from utils.file_parser import _sanitizar_nome

# --- CONFIGURAÇÃO DE CAMINHOS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECTS_ROOT_DIR = os.path.join(BASE_DIR, "projetos")

def refactor_manifest_file(project_name: str, file_name: str, error_reason: str) -> dict:
    """
    Usa a IA para corrigir um arquivo de manifesto que falhou na validação.

    Args:
        project_name: O nome do projeto.
        file_name: O nome do arquivo de manifesto a ser corrigido.
        error_reason: A mensagem de erro da validação, que será usada como contexto.

    Returns:
        Um dicionário com o status da operação.
    """
    sanitized_project_name = _sanitizar_nome(project_name)
    file_path = os.path.join(PROJECTS_ROOT_DIR, sanitized_project_name, "output", file_name)

    if not os.path.exists(file_path):
        return {"success": False, "message": f"Arquivo {file_name} não encontrado."}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        # Monta um prompt poderoso e específico para a correção
        prompt = f"""
        **TAREFA DE REATORAÇÃO AUTOMÁTICA**

        **Contexto:** O arquivo '{file_name}' do projeto '{project_name}' falhou na validação automática.
        **Motivo do Erro:** {error_reason}
        **Conteúdo Original do Arquivo:**
        ---
        {original_content}
        ---

        **Sua Missão:**
        1.  **Analise o 'Motivo do Erro'** para entender exatamente o que precisa ser corrigido. O erro pode ser desde seções inteiras faltando até conteúdo muito curto.
        2.  **Reescreva o 'Conteúdo Original do Arquivo'** para corrigir o problema apontado.
        3.  **Se uma seção estiver faltando**, adicione-a com um conteúdo relevante e coerente com o resto do documento.
        4.  **Se o conteúdo estiver muito curto**, expanda-o com informações úteis e detalhadas.
        5.  **Mantenha toda a estrutura e o conteúdo que já estavam corretos.** Não remova informações válidas.
        6.  **Responda APENAS com o conteúdo completo e corrigido do arquivo.** Não inclua nenhuma explicação, introdução ou cabeçalho extra na sua resposta. A sua saída será usada para sobrescrever o arquivo original diretamente.
        """

        print(f"[Refactoring Agent] Chamando IA para corrigir {file_name}...")
        corrected_content = executar_prompt_ia(prompt)

        # Salva o conteúdo corrigido de volta no arquivo
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(corrected_content)

        print(f"[Refactoring Agent] Arquivo {file_name} corrigido e salvo com sucesso.")
        return {"success": True, "message": f"Arquivo {file_name} foi corrigido pela IA."}

    except IAExecutionError as e:
        print(f"[Refactoring Agent] Erro de IA ao corrigir {file_name}: {e}")
        return {"success": False, "message": f"Erro da IA ao tentar corrigir o arquivo: {e}"}
    except Exception as e:
        print(f"[Refactoring Agent] Erro inesperado ao processar {file_name}: {e}")
        return {"success": False, "message": f"Erro inesperado: {e}"}
