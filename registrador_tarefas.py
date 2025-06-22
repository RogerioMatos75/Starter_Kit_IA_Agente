import datetime
import os

def registrar_log(titulo, mensagem, pasta="logs"):
    data = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"{titulo}_{data}.txt"
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, nome_arquivo)

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(f"{mensagem}\n")
    print(f"📝 Log salvo em: {caminho}")
