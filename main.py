import os

def executar_interacao(prompt):
    resposta = f"[IA Simulada] Resposta para: {prompt}"
    nome_arquivo = prompt.lower().replace(" ", "_") + ".txt"
    conteudo_arquivo = f"# Conteúdo gerado para:\n{prompt}\n\n{resposta}"
    return resposta, nome_arquivo, conteudo_arquivo

def salvar_arquivo_projeto(nome_projeto, nome_arquivo, conteudo):
    # Define caminho fixo: projetos/<nome_projeto>
    base_dir = os.path.join("projetos", nome_projeto)
    os.makedirs(base_dir, exist_ok=True)
    caminho_arquivo = os.path.join(base_dir, nome_arquivo)
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"✅ Arquivo salvo em: {caminho_arquivo}")

if __name__ == "__main__":
    nome_projeto = input("📝 Nome do projeto para salvar os arquivos gerados (dentro de 'projetos/'): ").strip()
    print("Digite seus prompts. Digite 'sair' para encerrar.\n")
    while True:
        prompt = input("🔹 Prompt: ")
        if prompt.lower() == 'sair':
            print("🚪 Encerrando sessão.")
            break
        resposta, nome_arquivo, conteudo_arquivo = executar_interacao(prompt)
        print("\n🤖 Resposta da IA:\n", resposta)
        if nome_arquivo and conteudo_arquivo:
            salvar_arquivo_projeto(nome_projeto, nome_arquivo, conteudo_arquivo)
