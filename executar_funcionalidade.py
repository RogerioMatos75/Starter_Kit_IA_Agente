from memoria_conceitual import carregar_memoria
from prompts import prompts_comuns

def executar_prompt(tipo="estudo_dominio"):
    prompt = prompts_comuns.get(tipo)
    if not prompt:
        return "Prompt não encontrado."

    dominio = input("Qual o tipo de projeto? ")
    print("\nPrompt gerado:")
    print(prompt.format(tipo_projeto=dominio))

if __name__ == "__main__":
    executar_prompt()
