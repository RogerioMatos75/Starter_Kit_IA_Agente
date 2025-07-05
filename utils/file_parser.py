import os
from PyPDF2 import PdfReader

def extract_text_from_file(file_path: str) -> str:
    """
    Extrai texto de arquivos .txt, .md e .pdf.
    Retorna o conteúdo do texto ou uma string vazia se o arquivo não for suportado ou houver erro.
    """
    if not os.path.exists(file_path):
        return ""

    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension in ['.txt', '.md']:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    elif file_extension == '.pdf':
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            print(f"[ERRO] Falha ao extrair texto do PDF {file_path}: {e}")
            return ""
    else:
        print(f"[AVISO] Tipo de arquivo não suportado para extração de texto: {file_extension}")
        return ""

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
