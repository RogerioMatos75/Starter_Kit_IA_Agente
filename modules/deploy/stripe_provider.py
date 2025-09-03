import stripe
import os

def validate_credentials(secret_key, public_key=None):
    """Valida as credenciais do Stripe."""
    if not secret_key:
        return {"success": False, "error": "A Chave Secreta do Stripe é obrigatória."}
    
    try:
        stripe.api_key = secret_key
        # Faz uma chamada de API leve para verificar se a chave é válida
        stripe.balance.retrieve()
        return {"success": True, "message": "Credenciais do Stripe são válidas."}
    except stripe.error.AuthenticationError:
        return {"success": False, "error": "Chave Secreta do Stripe inválida ou incorreta."}
    except Exception as e:
        return {"success": False, "error": f"Erro ao validar credenciais do Stripe: {str(e)}"}

