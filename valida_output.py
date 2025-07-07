import os
import re

# --- CONFIGURAÇÃO DE CAMINHOS ABSOLUTOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

OUTPUT_FILES = [
    os.path.join(OUTPUT_DIR, 'plano_base.md'),
    os.path.join(OUTPUT_DIR, 'arquitetura_tecnica.md'),
    os.path.join(OUTPUT_DIR, 'regras_negocio.md'),
    os.path.join(OUTPUT_DIR, 'fluxos_usuario.md'),
    os.path.join(OUTPUT_DIR, 'backlog_mvp.md'),
    os.path.join(OUTPUT_DIR, 'autenticacao_backend.md'),
]

REQUIRED_SECTIONS = {
    'plano_base.md': ['# Objetivo', '# Visão Geral', '# Público-Alvo', '# Escopo'],
    'arquitetura_tecnica.md': ['# Arquitetura', '# Tecnologias', '# Integrações', '# Fluxos Principais'],
    'regras_negocio.md': ['# Regras de Negócio', '# Restrições', '# Exceções', '# Decisões'],
    'fluxos_usuario.md': ['# Fluxos de Usuário', '# Navegação', '# Interações'],
    'backlog_mvp.md': ['# Funcionalidades', '# Critérios de Aceitação', '# Priorização'],
    'autenticacao_backend.md': ['# Autenticação Backend', '## Objetivo', '## Tecnologias', '## Endpoints Necessários', '## Regras de Negócio'],
}

def check_file(path, required_headers):
    if not os.path.exists(path):
        print(f'[X] Arquivo não encontrado: {path}')
        return False
    with open(path, encoding='utf-8') as f:
        content = f.read()
        if len(content.strip()) < 20:
            print(f'[!] Arquivo muito curto ou vazio: {path}')
            return False
        for header in required_headers:
            if not re.search(re.escape(header) + r'\s*', content, re.IGNORECASE):
                print(f'[!] Seção obrigatória ausente em {path}: {header}')
                return False
    print(f'[OK] {path} OK')
    return True

def run_validation():
    print('--- Validação dos arquivos de output ---')
    all_ok = True
    for file_path in OUTPUT_FILES:
        file_name = os.path.basename(file_path)
        required = REQUIRED_SECTIONS.get(file_name, [])
        if not check_file(file_path, required):
            all_ok = False
    if all_ok:
        print('\nTodos os arquivos de output estão completos e corretos!')
    else:
        print('\nAtenção: Revise os avisos acima para corrigir os arquivos.')
    return all_ok

if __name__ == '__main__':
    run_validation()