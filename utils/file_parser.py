import os
import re
from unidecode import unidecode

def _sanitizar_nome(nome):
    """Converte para ASCII, remove caracteres inválidos e espaços para criar um caminho seguro."""
    # Converte caracteres acentuados para a versão ASCII mais próxima (ex: 'ç' -> 'c')
    nome_ascii = unidecode(nome)
    # Substitui espaços e outros separadores por hífens
    nome_limpo = re.sub(r'[\s/\\:*?"<>|]', '-', nome_ascii)
    # Remove quaisquer caracteres que não sejam alfanuméricos, hífens ou underscores
    nome_sanitizado = re.sub(r'[^a-zA-Z0-9_-]', '', nome_limpo)
    # Remove hífens duplicados
    nome_final = re.sub(r'--+', '-', nome_sanitizado)
    return nome_final.lower()

def extract_text_from_file(file_input) -> str:
    """
    Extrai texto de diferentes tipos de entrada: caminho de arquivo (str) ou objeto de arquivo em memória.
    Retorna o conteúdo do texto ou uma string vazia se o tipo não for suportado ou houver erro.
    """
    text = ""
    filename = ""

    if isinstance(file_input, str):
        # Se a entrada é uma string, tratamos como um caminho de arquivo
        if not os.path.exists(file_input):
            return ""
        filename = file_input
        file_stream = open(filename, 'rb') # Abre em modo binário para consistência com PDF
    elif hasattr(file_input, 'filename') and hasattr(file_input, 'read'):
        # Se a entrada é um objeto de arquivo (como FileStorage do Flask)
        filename = file_input.filename
        file_stream = file_input
    else:
        print(f"[AVISO] Tipo de entrada não suportado para extração de texto: {type(file_input)}")
        return ""

    try:
        _, file_extension = os.path.splitext(filename)
        file_extension = file_extension.lower()

        if file_extension in ['.txt', '.md']:
            # Lê o stream e decodifica como texto
            text = file_stream.read().decode('utf-8', errors='ignore')
        elif file_extension == '.pdf':
            try:
                # PdfReader pode lidar com streams de arquivo em memória
                reader = PdfReader(file_stream)
                pdf_text = []
                for page in reader.pages:
                    pdf_text.append(page.extract_text() or "")
                text = "\n".join(pdf_text)
            except Exception as e:
                print(f"[ERRO] Falha ao extrair texto do PDF {filename}: {e}")
                text = ""
        else:
            print(f"[AVISO] Tipo de arquivo não suportado para extração de texto: {filename}")
            text = ""
    finally:
        # Se abrimos o arquivo a partir de um caminho, precisamos fechá-lo
        if isinstance(file_input, str):
            file_stream.close()

    return text

if __name__ == '__main__':
    # Exemplo de uso (apenas para teste local)
    # Crie alguns arquivos de teste para verificar
    with open("test.txt", "w") as f:
        f.write("Este é um arquivo de texto de teste.")
    with open("test.md", "w") as f:
        f.write("# Título\nEste é um arquivo Markdown.")
    
    # Para testar PDF, você precisaria de um arquivo PDF real
    # Ex: with open("test.pdf", "wb") as f: f.write(b"%PDF-1.4...")

    print(f"Texto de test.txt: {extract_text_from_file('test.txt')}")
    print(f"Texto de test.md: {extract_text_from_file('test.md')}")
    # print(f"Texto de test.pdf: {extract_text_from_file('test.pdf')}") # Descomente para testar com PDF real