import os
import google.generativeai as genai

class IAExecutionError(Exception):
    """Exceção customizada para erros durante a execução da IA."""
    pass

def executar_prompt_ia(prompt: str, api_key: str = None) -> str:
    """
    Executa um prompt usando a API do Google Gemini.
    Pode usar uma chave de API fornecida diretamente ou, como fallback,
    a chave configurada na variável de ambiente.

    Args:
        prompt: O prompt a ser enviado para a IA.
        api_key: (Opcional) A chave de API a ser usada para esta chamada específica.

    Raises:
        IAExecutionError: Se a chave da API não estiver configurada ou se ocorrer um erro na API.

    Returns:
        A resposta em texto da IA.
    """
    # Se nenhuma chave for fornecida, usa a do ambiente.
    if api_key is None:
        api_key = os.environ.get("GEMINI_API_KEY")

    # Verifica se a chave é nula, vazia ou apenas aspas vazias '""'
    if not api_key or not api_key.strip() or api_key == '""':
        raise IAExecutionError(
            "A variável de ambiente GEMINI_API_KEY não foi definida. "
            "Por favor, configure-a no painel ou no arquivo .env e reinicie o servidor."
        )

    try:
        # Remove aspas extras que podem vir do arquivo .env
        clean_api_key = api_key.strip('"')
        genai.configure(api_key=clean_api_key)
        
        # O modelo 'gemini-pro' pode estar obsoleto dependendo da versão da API.
        # Usar um modelo mais recente e estável como 'gemini-1.5-flash-latest' é recomendado.
        # Para mais detalhes: https://ai.google.dev/gemini-api/docs/models/gemini
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        
        # Verifica se a resposta foi bloqueada por segurança
        if not response.parts and response.prompt_feedback and response.prompt_feedback.block_reason:
            block_reason = response.prompt_feedback.block_reason.name
            raise IAExecutionError(f"A resposta da IA foi bloqueada por segurança. Razão: {block_reason}")

        return response.text
    except Exception as e:
        # Se já for nossa exceção customizada, apenas a relança
        if isinstance(e, IAExecutionError):
            raise e
        # Se for outra exceção, a encapsula na nossa
        raise IAExecutionError(f"Falha ao contatar a API do Gemini: {e}")
