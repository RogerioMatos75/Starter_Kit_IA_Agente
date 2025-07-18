from flask import Blueprint, jsonify, render_template, request
import time
from fsm_orquestrador import registrar_log
from .supabase_provider import deploy as deploy_supabase, validate_credentials as validate_supabase
from .vercel_provider import deploy as deploy_vercel


deploy_bp = Blueprint('deploy', __name__, template_folder='templates')

@deploy_bp.route('/deploy')
def deploy_page():
    return render_template('deploy_page.html')

@deploy_bp.route('/api/deploy/start', methods=['POST'])
def start_deploy_task():
    task_id = "some_new_task_id"
    return jsonify({"status": "deploy queued", "task_id": task_id})

@deploy_bp.route('/api/execute_deploy', methods=['POST'])
def execute_deploy():
    data = request.json
    provider = data.get('provider')
    project_name = data.get('project_name')
    api_token = data.get('api_token') # Token genérico para qualquer provedor
    project_ref = data.get('project_ref') # Para Supabase

    if not provider or not project_name:
        return jsonify({"error": "Provedor e nome do projeto são obrigatórios."}), 400

    try:
        deploy_output = ""
        if provider == 'vercel':
            if not api_token:
                return jsonify({"error": "Token da Vercel é obrigatório para o deploy."}), 400
            print(f"[DEPLOY] Recebido token da Vercel: ...{api_token[-4:]}")
            result = deploy_vercel(api_token)
            if not result["success"]:
                raise Exception(result["error"])
            deploy_output = result["output"]
        elif provider == 'supabase':
            if not api_token or not project_ref:
                return jsonify({"error": "API Token e Project Ref do Supabase são obrigatórios."}), 400
            print(f"[DEPLOY] Recebido token do Supabase: ...{api_token[-4:]}")
            result = deploy_supabase(api_token, project_ref)
            if not result["success"]:
                raise Exception(result["error"])
            deploy_output = result["output"]
        else:
            return jsonify({"error": f"Provedor de deploy '{provider}' não é suportado."}), 400
        
        registrar_log(
            etapa="Deploy",
            status="concluída",
            decisao=f"Deploy em {provider} iniciado pelo usuário.",
            resposta_agente=deploy_output,
            tarefa=f"Deploy {provider}: {project_name}"
        )
        
        return jsonify({"output": deploy_output}), 200
    except Exception as e:
        print(f"[DEPLOY ERROR] Falha no deploy: {e}")
        return jsonify({"error": f"Falha no deploy: {e}"}), 500

# --- NOVA ROTA PARA O DASHBOARD ---
@deploy_bp.route('/deploy', methods=['POST'])
def dashboard_deploy_initiate():
    data = request.json
    project_name = data.get('project_name')

    if not project_name:
        return jsonify({"error": "Nome do projeto é obrigatório para iniciar o deploy."}), 400
    
    try:
        # Aqui você pode adicionar a lógica para iniciar o processo de deploy real
        # Por exemplo, enfileirar uma tarefa assíncrona ou chamar uma função de deploy simplificada.
        registrar_log(
            etapa="Deploy",
            status="iniciado",
            decisao=f"Processo de deploy para o projeto '{project_name}' iniciado pelo dashboard.",
            resposta_agente="Aguardando seleção de provedor e credenciais.",
            tarefa=f"Iniciar Deploy: {project_name}"
        )
        return jsonify({"message": f"Processo de deploy para '{project_name}' iniciado com sucesso. Prossiga com as configurações."}), 200
    except Exception as e:
        print(f"[ERRO API] Falha ao iniciar deploy pelo dashboard: {e}")
        return jsonify({"error": str(e)}), 500