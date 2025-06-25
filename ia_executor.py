import os
import google.generativeai as genai

def configurar_ia():
    """
    Configura a API do Gemini a partir de uma variável de ambiente.
    Levanta um erro se a chave da API não estiver definida.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "A variável de ambiente GEMINI_API_KEY não foi definida. "
            "Por favor, obtenha sua chave no Google AI Studio e configure a variável."
        )
    genai.configure(api_key=api_key)

def executar_prompt_ia(prompt: str) -> str:
    """
    Envia um prompt para a API do Gemini (modelo gemini-pro) e retorna a resposta em texto.
    """
    try:
        configurar_ia()
        # Usando um modelo mais recente e estável. 'gemini-1.5-flash' é rápido e eficiente.
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"[ERRO NA IA] Falha ao executar o prompt: {e}")
        return f"Ocorreu um erro ao contatar a IA. Verifique o console do servidor para detalhes. Erro: {e}"