from flask import Blueprint, jsonify, request, render_template
import os
from dotenv import dotenv_values, set_key
from . import vercel_provider, supabase_provider, stripe_provider

deploy_bp = Blueprint('deploy', __name__)

# --- Funções Auxiliares ---

def _get_project_dotenv_path(project_name):
    """Retorna o caminho para o arquivo .env de um projeto específico."""
    if not project_name or not isinstance(project_name, str) or '/' in project_name or '\\' in project_name:
        return None, "Nome de projeto inválido."
    
    # O diretório base é o diretório raiz da aplicação Flask
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    project_path = os.path.join(base_dir, 'projetos', project_name)
    
    if not os.path.exists(project_path):
        os.makedirs(project_path)
        
    return os.path.join(project_path, '.env'), None

def _load_project_env(project_name):
    """Carrega as variáveis de ambiente de um projeto específico."""
    dotenv_path, error = _get_project_dotenv_path(project_name)
    if error:
        return None, error
    
    if not os.path.exists(dotenv_path):
        return {}, None # Retorna um dict vazio se o .env não existe
        
    return dotenv_values(dotenv_path), None

# --- Rotas Refatoradas ---

@deploy_bp.route('/api/deploy/get_credentials_status', methods=['POST'])
def get_credentials_status():
    project_name = request.json.get('project_name')
    if not project_name:
        return jsonify({"error": "O nome do projeto é obrigatório."}), 400

    config, error = _load_project_env(project_name)
    if error:
        return jsonify({"error": error}), 400

    status = {
        'vercel': {'configured': 'VERCEL_TOKEN' in config},
        'supabase': {'configured': 'SUPABASE_URL' in config and 'SUPABASE_SERVICE_ROLE_KEY' in config},
        'stripe': {'configured': 'STRIPE_SECRET_KEY' in config}
    }
    return jsonify(status)

@deploy_bp.route('/api/deploy/save_credentials', methods=['POST'])
def save_credentials():
    data = request.json
    project_name = data.get('project_name')
    if not project_name:
        return jsonify({"error": "O nome do projeto é obrigatório."}), 400

    dotenv_path, error = _get_project_dotenv_path(project_name)
    if error:
        return jsonify({"error": error}), 400

    key_mapping = {
        'vercel_token': 'VERCEL_TOKEN',
        'supabase_url': 'SUPABASE_URL',
        'supabase_key': 'SUPABASE_SERVICE_ROLE_KEY',
        'stripe_secret': 'STRIPE_SECRET_KEY',
        'stripe_public': 'STRIPE_PUBLIC_KEY'
    }

    try:
        for frontend_key, env_key in key_mapping.items():
            if data.get(frontend_key):
                set_key(dotenv_path, env_key, data[frontend_key])
        return jsonify({"message": f"Credenciais salvas com sucesso para o projeto '{project_name}'."})
    except Exception as e:
        return jsonify({"error": f"Falha ao salvar o arquivo .env: {e}"}), 500

@deploy_bp.route('/api/deploy/validate_credentials', methods=['POST'])
def validate_all_credentials():
    project_name = request.json.get('project_name')
    if not project_name:
        return jsonify({"error": "O nome do projeto é obrigatório."}), 400
        
    config, error = _load_project_env(project_name)
    if error:
        return jsonify({"error": error}), 400

    results = {}
    vercel_token = config.get('VERCEL_TOKEN')
    results['vercel'] = vercel_provider.validate_credentials(vercel_token) if vercel_token else {'success': False, 'error': 'Credencial não configurada.'}

    supabase_url = config.get('SUPABASE_URL')
    supabase_key = config.get('SUPABASE_SERVICE_ROLE_KEY')
    if supabase_url and supabase_key:
        project_ref = supabase_url.replace('https://', '').split('.')[0]
        results['supabase'] = supabase_provider.validate_credentials(supabase_key, project_ref)
    else:
        results['supabase'] = {'success': False, 'error': 'Credenciais não configuradas.'}

    stripe_secret = config.get('STRIPE_SECRET_KEY')
    results['stripe'] = stripe_provider.validate_credentials(stripe_secret) if stripe_secret else {'success': False, 'error': 'Credencial não configurada.'}
        
    return jsonify(results)

@deploy_bp.route('/api/deploy/provision_database', methods=['POST'])
def provision_database():
    project_name = request.json.get('project_name')
    if not project_name:
        return jsonify({"error": "O nome do projeto é obrigatório."}), 400

    config, error = _load_project_env(project_name)
    if error:
        return jsonify({"error": error}), 400

    supabase_url = config.get('SUPABASE_URL')
    supabase_key = config.get('SUPABASE_SERVICE_ROLE_KEY')

    if not supabase_url or not supabase_key:
        return jsonify({"error": "As credenciais do Supabase não estão configuradas para este projeto."}, 400)

    try:
        project_ref = supabase_url.replace('https://', '').split('.')[0]
        result = supabase_provider.deploy(supabase_key, project_ref)
        if not result.get("success"):
            raise Exception(result.get("error", "Erro desconhecido"))
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Falha ao provisionar o banco de dados: {e}"}), 500

@deploy_bp.route('/api/deploy/deploy_frontend', methods=['POST'])
def deploy_frontend():
    project_name = request.json.get('project_name')
    if not project_name:
        return jsonify({"error": "O nome do projeto é obrigatório."}), 400

    config, error = _load_project_env(project_name)
    if error:
        return jsonify({"error": error}), 400
        
    vercel_token = config.get('VERCEL_TOKEN')
    if not vercel_token:
        return jsonify({"error": "O token da Vercel não está configurado para este projeto."}, 400)

    try:
        result = vercel_provider.deploy(vercel_token)
        if not result.get("success"):
            raise Exception(result.get("error", "Erro desconhecido"))
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Falha no deploy do frontend: {e}"}), 500

@deploy_bp.route('/api/deploy/complete_deploy', methods=['POST'])
def complete_deploy():
    project_name = request.json.get('project_name')
    if not project_name:
        return jsonify({"error": "O nome do projeto é obrigatório."}), 400

    # Reutiliza as funções de endpoint, passando o nome do projeto
    # É necessário reconstruir a request para as funções internas ou refatorar
    # Para simplicidade, vamos chamar a lógica diretamente.

    full_output = []
    config, error = _load_project_env(project_name)
    if error:
        return jsonify({"error": error}), 500

    # Etapa 1: Provisionar Banco de Dados
    supabase_url = config.get('SUPABASE_URL')
    supabase_key = config.get('SUPABASE_SERVICE_ROLE_KEY')
    if not supabase_url or not supabase_key:
        return jsonify({"error": "Credenciais do Supabase ausentes."}, 400)
    try:
        project_ref = supabase_url.replace('https://', '').split('.')[0]
        db_result = supabase_provider.deploy(supabase_key, project_ref)
        if not db_result.get("success"):
            raise Exception(f"Falha na etapa do Supabase: {db_result.get('error', 'Erro desconhecido')}")
        full_output.append({"provider": "Supabase", "output": db_result.get("output")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Etapa 2: Deploy do Frontend
    vercel_token = config.get('VERCEL_TOKEN')
    if not vercel_token:
        return jsonify({"error": "Token da Vercel ausente."}, 400)
    try:
        frontend_result = vercel_provider.deploy(vercel_token)
        if not frontend_result.get("success"):
            raise Exception(f"Falha na etapa da Vercel: {frontend_result.get('error', 'Erro desconhecido')}")
        full_output.append({"provider": "Vercel", "output": frontend_result.get("output")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
    return jsonify({"success": True, "message": "Deploy completo finalizado com sucesso.", "details": full_output})