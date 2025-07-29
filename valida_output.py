import os
import re
from utils.file_parser import _sanitizar_nome # Importa a função de sanitização

# --- CONFIGURAÇÃO DE CAMINHOS E CONSTANTES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "projetos"))

# Nomes dos arquivos de saída esperados na pasta 'output' de cada projeto
OUTPUT_FILES = [
    '01_base_conhecimento.md',
    '02_arquitetura_tecnica.md',
    '03_regras_negocio.md',
    '04_fluxos_usuario.md',
    '05_backlog_mvp.md',
    '06_autenticacao_backend.md',
]

# Seções obrigatórias para cada tipo de documento
REQUIRED_SECTIONS = {
    '01_base_conhecimento.md': ['# Regras de Negócio', '# Requisitos Funcionais', '# Requisitos Não Funcionais', '# Personas de Usuário', '# Fluxos de Usuário'],
    '02_arquitetura_tecnica.md': ['# Arquitetura', '# Tecnologias', '# Integrações', '# Fluxos Principais'],
    '03_regras_negocio.md': ['# Regras de Negócio', '# Restrições', '# Exceções', '# Decisões'],
    '04_fluxos_usuario.md': ['# Fluxos de Usuário', '# Navegação', '# Interações'],
    '05_backlog_mvp.md': ['# Funcionalidades', '# Critérios de Aceitação', '# Priorização'],
    '06_autenticacao_backend.md': ['# Autenticação Backend', '## Método de Autenticação', '## Fluxo de Autenticação', '## Tecnologias/Bibliotecas', '## Considerações de Segurança'],
}

def check_file(project_name: str, file_name: str) -> dict:
    """
    Verifica a existência e o conteúdo de um arquivo de conhecimento localmente.
    Retorna um dicionário com status e mensagem.
    """
    sanitized_project_name = _sanitizar_nome(project_name)
    file_path = os.path.join(PROJECTS_ROOT_DIR, sanitized_project_name, "output", file_name)
    
    result = {
        "file_name": file_name,
        "found": False,
        "valid": False,
        "message": "Arquivo não encontrado."
    }

    if not os.path.exists(file_path):
        return result

    result["found"] = True
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if len(content.strip()) < 50: # Aumentado para 50 para garantir conteúdo mínimo
            result["message"] = "Conteúdo muito curto ou vazio."
            return result
        
        required_headers = REQUIRED_SECTIONS.get(file_name, [])
        all_headers_found = True
        missing_headers = []

        for header in required_headers:
            if not re.search(re.escape(header) + r'\s*', content, re.IGNORECASE):
                all_headers_found = False
                missing_headers.append(header)
        
        if not all_headers_found:
            result["message"] = f"Seções obrigatórias ausentes: {', '.join(missing_headers)}."
            return result
        
        result["valid"] = True
        result["message"] = "OK"
        return result

    except Exception as e:
        result["message"] = f"Erro ao ler ou validar o arquivo: {e}"
        return result

def run_validation(project_name: str) -> dict:
    """
    Executa a validação de todos os arquivos de conhecimento para um dado projeto localmente.
    Retorna um dicionário com o status geral e detalhes de cada arquivo.
    """
    print(f'--- Validação dos arquivos de conhecimento para o projeto: {project_name} ---')
    validation_results = []
    all_valid = True

    for file_name in OUTPUT_FILES:
        result = check_file(project_name, file_name)
        validation_results.append(result)
        if not result["valid"]:
            all_valid = False
    
    final_message = "Todos os arquivos de conhecimento estão completos e corretos!" if all_valid \
                    else "Atenção: Alguns arquivos de conhecimento estão incompletos ou ausentes. Revise-os."
    
    print(f'[VALIDAÇÃO] {final_message}')
    return {"all_valid": all_valid, "details": validation_results, "message": final_message}

