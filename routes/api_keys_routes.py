# routes/api_keys_routes.py
from flask import Blueprint, jsonify, request
import os
import google.generativeai as genai
from dotenv import set_key, unset_key

api_keys_bp = Blueprint('api_keys_bp', __name__, url_prefix='/api/keys')

# Caminho para o arquivo .env na raiz do projeto
DOTENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")

api_keys_bp = Blueprint('api_keys_bp', __name__, url_prefix='/api/keys')

@api_keys_bp.route('/status')
def get_api_key_status():
    # Esta rota espelha a lógica de 'check' para o novo frontend.
    has_key = os.environ.get("GEMINI_API_KEY") is not None
    return jsonify({"has_key": has_key})

@api_keys_bp.route('/check')
def check_api_key():
    is_configured = os.environ.get("GEMINI_API_KEY") is not None
    return jsonify({"is_configured": is_configured})

@api_keys_bp.route('/list')
def list_api_keys():
    # Por simplicidade, apenas listamos a chave Gemini se configurada
    keys = []
    if os.environ.get("GEMINI_API_KEY"):
        keys.append({
            "provider": "gemini",
            "status": "active", # Assumimos ativo se configurado
            "lastCheck": "N/A" # Poderíamos adicionar lógica para registrar a última verificação
        })
    return jsonify({"keys": keys})

@api_keys_bp.route('/save', methods=['POST'])
def save_api_key():
    data = request.json
    api_key = data.get('api_key')
    provider = data.get('provider') # e.g., "gemini"

    if not api_key or not provider:
        return jsonify({"error": "API Key e provedor são obrigatórios."}), 400

    # Salva a chave no arquivo .env e atualiza a variável de ambiente
    if provider == "gemini":
        os.environ["GEMINI_API_KEY"] = api_key
        set_key(DOTENV_PATH, "GEMINI_API_KEY", api_key)
        return jsonify({"message": "API Key Gemini salva com sucesso! Reinicie o servidor para aplicar."})
    else:
        return jsonify({"error": f"Provedor '{provider}' não suportado para salvamento direto."}), 400

@api_keys_bp.route('/test', methods=['POST'])
def test_new_api_key():
    data = request.json
    api_key = data.get('api_key')

    if not api_key:
        return jsonify({"success": False, "message": "Nenhuma API Key fornecida para teste."}), 400

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash') # Usar um modelo leve e recente para teste
        model.generate_content("Hello") # Teste simples de conectividade
        return jsonify({"success": True, "message": "API Key Gemini válida e conectada!"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Falha no teste da API Key Gemini: {e}"}), 200

@api_keys_bp.route('/remove', methods=['POST'])
def remove_api_key():
    data = request.json
    provider = data.get('provider')

    if not provider:
        return jsonify({"error": "Provedor é obrigatório para remoção."}), 400

    if provider == "gemini":
        key_name = "GEMINI_API_KEY"
        key_existed_in_env = unset_key(DOTENV_PATH, key_name)
        
        key_existed_in_session = False
        if key_name in os.environ:
            del os.environ[key_name]
            key_existed_in_session = True

        if key_existed_in_env or key_existed_in_session:
            return jsonify({"message": "API Key Gemini removida com sucesso!"}), 200
        else:
            return jsonify({"message": "API Key Gemini não encontrada para remoção."}), 200
    else:
        return jsonify({"error": f"Provedor '{provider}' não suportado para remoção direta."}), 400
