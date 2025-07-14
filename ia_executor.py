import os
import google.generativeai as genai

class IAExecutionError(Exception):
    """Exceção customizada para erros durante a execução da IA."""
    pass

def executar_prompt_ia(prompt: str, api_key: str = None, is_json_output: bool = False) -> str:
    """
    Executa um prompt usando a API do Google Gemini.
    Pode solicitar uma saída em formato JSON.

    Args:
        prompt: O prompt a ser enviado para a IA.
        api_key: (Opcional) A chave de API a ser usada.
        is_json_output: (Opcional) Se True, configura a API para retornar JSON.

    Raises:
        IAExecutionError: Se a chave da API não estiver configurada ou se ocorrer um erro na API.

    Returns:
        A resposta da IA (string de texto ou string JSON).
    """
    if api_key is None:
        api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key or not api_key.strip() or api_key == '""':
        raise IAExecutionError(
            "A variável de ambiente GEMINI_API_KEY não foi definida. "
            "Por favor, configure-a no painel ou no arquivo .env e reinicie o servidor."
        )

    try:
        clean_api_key = api_key.strip('"')
        genai.configure(api_key=clean_api_key)
        
        model = genai.GenerativeModel('gemini-1.5-flash')

        generation_config = None
        if is_json_output:
            generation_config = genai.types.GenerationConfig(
                response_mime_type="application/json"
            )

        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        if not response.parts and response.prompt_feedback and response.prompt_feedback.block_reason:
            block_reason = response.prompt_feedback.block_reason.name
            raise IAExecutionError(f"A resposta da IA foi bloqueada por segurança. Razão: {block_reason}")

        return response.text
    except Exception as e:
        if isinstance(e, IAExecutionError):
            raise e
        raise IAExecutionError(f"Falha ao contatar a API do Gemini: {e}")
