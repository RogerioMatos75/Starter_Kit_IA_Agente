import os

OUTPUT_FILES = [
    'output/plano_base.md',
    'output/arquitetura_tecnica.md',
    'output/regras_negocio.md',
    'output/fluxos_usuario.md',
    'output/backlog_mvp.md',
]

REQUIRED_SECTIONS = {
    'plano_base.md': ['# Objetivo', '# Visão Geral', '# Público-Alvo', '# Escopo'],
    'arquitetura_tecnica.md': ['# Arquitetura', '# Tecnologias', '# Integrações', '# Fluxos Principais'],
    'regras_negocio.md': ['# Regras de Negócio', '# Restrições', '# Exceções', '# Decisões'],
    'fluxos_usuario.md': ['# Fluxos de Usuário', '# Navegação', '# Interações'],
    'backlog_mvp.md': ['# Funcionalidades', '# Critérios de Aceitação', '# Priorização'],
}

def check_file(path, required_headers):
    if not os.path.exists(path):
        print(f'❌ Arquivo não encontrado: {path}')
        return False
    with open(path, encoding='utf-8') as f:
        content = f.read()
        if len(content.strip()) < 20:
            print(f'⚠️ Arquivo muito curto ou vazio: {path}')
            return False
        for header in required_headers:
            if header not in content:
                print(f'⚠️ Seção obrigatória ausente em {path}: {header}')
                return False
    print(f'✅ {path} OK')
    return True

def main():
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

if __name__ == '__main__':
    main()
