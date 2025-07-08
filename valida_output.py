import os
import re
from utils.supabase_client import supabase
from utils.file_parser import _sanitizar_nome # Importa a função de sanitização

# --- CONFIGURAÇÃO DE CAMINHOS E CONSTANTES ---
BASE_CONHECIMENTO_BUCKET = "base-conhecimento"

# Estes são agora apenas nomes de arquivo, não caminhos completos
OUTPUT_FILES = [
    'plano_base.md',
    'arquitetura_tecnica.md',
    'regras_negocio.md',
    'fluxos_usuario.md',
    'backlog_mvp.md',
    'autenticacao_backend.md',
]

REQUIRED_SECTIONS = {
    'plano_base.md': ['# Objetivo', '# Visão Geral', '# Público-Alvo', '# Escopo'],
    'arquitetura_tecnica.md': ['# Arquitetura', '# Tecnologias', '# Integrações', '# Fluxos Principais'],
    'regras_negocio.md': ['# Regras de Negócio', '# Restrições', '# Exceções', '# Decisões'],
    'fluxos_usuario.md': ['# Fluxos de Usuário', '# Navegação', '# Interações'],
    'backlog_mvp.md': ['# Funcionalidades', '# Critérios de Aceitação', '# Priorização'],
    'autenticacao_backend.md': ['# Autenticação Backend', '## Objetivo', '## Tecnologias', '## Endpoints Necessários', '## Regras de Negócio'],
}

def check_file(project_name: str, file_name: str, required_headers: list) -> bool:
    """
    Verifica a existência e o conteúdo de um arquivo de conhecimento no Supabase Storage.
    """
    if not supabase:
        print("[ERRO] Cliente Supabase não está disponível para validação.")
        return False

    sanitized_project_name = _sanitizar_nome(project_name)
    storage_path = f"{sanitized_project_name}/{file_name}"

    try:
        # Download do conteúdo do arquivo do Supabase Storage
        response = supabase.storage.from_(BASE_CONHECIMENTO_BUCKET).download(storage_path)
        content = response.decode('utf-8') # Assume que é texto UTF-8

        if len(content.strip()) < 20:
            print(f'[!] Arquivo muito curto ou vazio no Supabase: {storage_path}')
            return False
        
        for header in required_headers:
            # Usa regex para encontrar o cabeçalho, ignorando espaços e case
            if not re.search(re.escape(header) + r'\s*', content, re.IGNORECASE):
                print(f'[!] Seção obrigatória ausente em {storage_path}: {header}')
                return False
        
        print(f'[OK] {storage_path} OK')
        return True

    except Exception as e:
        # Supabase Storage levanta uma exceção se o arquivo não for encontrado
        print(f'[X] Erro ao acessar arquivo no Supabase: {storage_path} - {e}')
        return False

def run_validation(project_name: str) -> bool:
    """
    Executa a validação de todos os arquivos de conhecimento para um dado projeto no Supabase.
    """
    print('--- Validação dos arquivos de conhecimento no Supabase ---')
    all_ok = True
    for file_name in OUTPUT_FILES:
        required = REQUIRED_SECTIONS.get(file_name, [])
        if not check_file(project_name, file_name, required):
            all_ok = False
    
    if all_ok:
        print('\nTodos os arquivos de conhecimento no Supabase estão completos e corretos!')
    else:
        print('\nAtenção: Revise os avisos acima para corrigir os arquivos no Supabase.')
    return all_ok
