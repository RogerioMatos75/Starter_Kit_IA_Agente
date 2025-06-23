import os

OUTPUT_FILES = [
    'output/plano_base.md',
    'output/arquitetura_tecnica.md',
    'output/regras_negocio.md',
    'output/fluxos_usuario.md',
    'output/backlog_mvp.md',
]

SECTION_TITLES = {
    'plano_base.md': 'PLANO BASE',
    'arquitetura_tecnica.md': 'ARQUITETURA TÉCNICA',
    'regras_negocio.md': 'REGRAS DE NEGÓCIO',
    'fluxos_usuario.md': 'FLUXOS DE USUÁRIO',
    'backlog_mvp.md': 'BACKLOG DO MVP',
}

def extrair_secoes(path, headers):
    secoes = {}
    if not os.path.exists(path):
        return secoes
    with open(path, encoding='utf-8') as f:
        content = f.read()
        for i, header in enumerate(headers):
            start = content.find(header)
            if start == -1:
                continue
            end = content.find(headers[i+1], start) if i+1 < len(headers) else len(content)
            secoes[header] = content[start+len(header):end].strip()
    return secoes

def mostrar_guia():
    print("\n=== GUIA DO PROJETO (extraído dos arquivos de output) ===\n")
    for file_path in OUTPUT_FILES:
        file_name = os.path.basename(file_path)
        titulo = SECTION_TITLES.get(file_name, file_name)
        print(f"# {titulo}")
        headers = REQUIRED_SECTIONS.get(file_name, [])
        secoes = extrair_secoes(file_path, headers)
        for header in headers:
            print(f"\n{header}")
            print(secoes.get(header, '[Seção não encontrada ou vazia]'))
        print("\n" + ("-"*40) + "\n")

REQUIRED_SECTIONS = {
    'plano_base.md': ['# Objetivo', '# Visão Geral', '# Público-Alvo', '# Escopo'],
    'arquitetura_tecnica.md': ['# Arquitetura', '# Tecnologias', '# Integrações', '# Fluxos Principais'],
    'regras_negocio.md': ['# Regras de Negócio', '# Restrições', '# Exceções', '# Decisões'],
    'fluxos_usuario.md': ['# Fluxos de Usuário', '# Navegação', '# Interações'],
    'backlog_mvp.md': ['# Funcionalidades', '# Critérios de Aceitação', '# Priorização'],
}

if __name__ == '__main__':
    mostrar_guia()
    print("Guia extraído! Use este painel para supervisionar as próximas etapas do workflow.")
