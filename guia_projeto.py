import os
import re
from valida_output import REQUIRED_SECTIONS

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
            # Usa regex para encontrar o cabeçalho, ignorando espaços e case
            # Adiciona \s* para permitir qualquer número de espaços (ou nenhum)
            # Adiciona re.IGNORECASE para ignorar maiúsculas/minúsculas
            match = re.search(re.escape(header) + r'\s*\n', content, re.IGNORECASE)
            if not match:
                continue
            start = match.end()
            
            # Encontra o próximo cabeçalho para definir o fim da seção
            end = len(content)
            for j in range(i + 1, len(headers)):
                next_header_match = re.search(re.escape(headers[j]) + r'\s*\n', content, re.IGNORECASE)
                if next_header_match:
                    end = next_header_match.start()
                    break
            secoes[header] = content[start:end].strip()
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



if __name__ == '__main__':
    mostrar_guia()
    print("Guia extraído! Use este painel para supervisionar as próximas etapas do workflow.")
