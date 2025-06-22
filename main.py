import os
from agente.executor_agente import executar_interacao

def salvar_arquivo_projeto(nome_projeto, nome_arquivo, conteudo):
    base_dir = os.path.join("projetos", nome_projeto)
    os.makedirs(base_dir, exist_ok=True)
    caminho_arquivo = os.path.join(base_dir, nome_arquivo)
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"Arquivo salvo em: {caminho_arquivo}")

if __name__ == "__main__":
    nome_projeto = input("Nome do projeto para salvar os arquivos gerados: ").strip()
    while True:
        prompt = input("Digite seu prompt (ou 'sair'): ")
        if prompt.lower() == 'sair':
            break
        resposta, nome_arquivo, conteudo_arquivo = executar_interacao(prompt)
        print("Resposta da IA:", resposta)
        if nome_arquivo and conteudo_arquivo:
            salvar_arquivo_projeto(nome_projeto, nome_arquivo, conteudo_arquivo)
