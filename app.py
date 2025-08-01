import os
import json
import io
import zipfile
import sys
import datetime
import subprocess
import time
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, g, session
from flask_socketio import SocketIO, emit
from functools import wraps
from flask_cors import CORS
import google.generativeai as genai
from fsm_orquestrador import FSMOrquestrador
from valida_output import run_validation as validar_base_conhecimento
from ia_executor import executar_prompt_ia, IAExecutionError
from dotenv import load_dotenv
from prompt_generator import parse_prompt_structure, save_prompts_to_json # NEW: Import prompt generator

load_dotenv() # Carrega as variáveis de ambiente do .env
import stripe
from relatorios import exportar_log_txt
from modules.deploy.routes import deploy_bp
from routes.api_keys_routes import api_keys_bp
from routes.supervisor_routes import supervisor_bp
from routes.proposal_routes import proposal_bp
from routes.project_setup_routes import setup_bp, project_bp # Importa o novo blueprint
from routes.template_routes import template_bp
from routes.agent_routes import agent_bp
from auditoria_seguranca import auditoria_global
# from utils.supabase_client import supabase # Comentado para desabilitar Supabase
from utils.file_parser import extract_text_from_file, _sanitizar_nome

# --- CONFIGURAÇÃO DE CAMINHOS E CONSTANTES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# BASE_CONHECIMENTO_BUCKET = "base-conhecimento" # Comentado para desabilitar Supabase

def carregar_workflow(file_path=None):
    if file_path is None:
        file_path = os.path.join(BASE_DIR, "workflow.json")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)
        print(f"Workflow '{workflow_data.get('nome_workflow')}' carregado com sucesso.")
        return workflow_data.get("estados", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[ERRO CRÍTICO] Não foi possível carregar o workflow de '{file_path}': {e}")
        return []

app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, 'static'),
            template_folder=os.path.join(BASE_DIR, 'templates'))
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey") # Usar variável de ambiente ou fallback
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

project_states = carregar_workflow()
if not project_states:
    sys.exit("ERRO CRÍTICO: Falha no carregamento do workflow.json.")

fsm_instance = FSMOrquestrador(project_states)

app.register_blueprint(deploy_bp, url_prefix='/deployment')
app.register_blueprint(api_keys_bp)
app.register_blueprint(supervisor_bp)
app.register_blueprint(proposal_bp)
app.register_blueprint(setup_bp)
app.register_blueprint(project_bp) # Registra o novo blueprint
app.register_blueprint(template_bp)
app.register_blueprint(agent_bp)

# Adiciona uma verificação clara na inicialização se o Supabase não conectar
# if not supabase: # Comentado para desabilitar Supabase
#     print("\n" + "="*60)
#     print("!! [ERRO CRÍTICO] Cliente Supabase não inicializado.      !!")
#     print("!! Verifique se as variáveis SUPABASE_URL e SUPABASE_KEY   !!")
#     print("!! estão configuradas corretamente no seu arquivo .env.    !!")
#     print("!! As funcionalidades de autenticação e banco de dados    !!")
#     print("!! estarão DESATIVADAS.                                  !!")
#     print("="*60 + "\n")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # if 'user_id' not in session: # Comentado para desabilitar Supabase
        #     return redirect(url_for('login')) # Comentado para desabilitar Supabase
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def after_request(response):
    try:
        auditoria_global.log_http_request(status_code=response.status_code)
    except Exception as e:
        print(f"[ERRO AUDITORIA] Falha ao registrar requisição: {e}")
    return response

# --- ROTAS PRINCIPAIS ---
@app.route('/')
def initial_loading():
    return render_template('initial_loading.html')

# @app.route('/login') # Comentado para desabilitar Supabase
# def login(): # Comentado para desabilitar Supabase
#     return render_template('login.html') # Comentado para desabilitar Supabase

# @app.route('/register') # Comentado para desabilitar Supabase
# def register(): # Comentado para desabilitar Supabase
#     return render_template('register.html') # Comentado para desabilitar Supabase

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard-simple')
def dashboard_simple():
    """Dashboard simplificado para teste"""
    return render_template('dashboard_simple.html')

@app.route('/test-dashboard')
def test_dashboard():
    """Rota de teste para verificar se o problema é no template dashboard.html"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Teste Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-900 text-white p-8">
        <h1 class="text-3xl font-bold mb-4">🧪 TESTE DASHBOARD</h1>
        <p class="mb-4">Se você consegue ver esta página, o Flask está funcionando!</p>

        <div class="bg-red-600 p-4 rounded-lg mb-4">
            <h2 class="text-xl font-bold">Etapa 8 - Deploy Teste</h2>
            <button onclick="alert('Funcionou!')" class="bg-green-600 px-4 py-2 rounded mt-2">
                🚀 TESTE
            </button>
        </div>

        <div class="bg-blue-600 p-4 rounded-lg">
            <h3 class="font-bold">Debug Info:</h3>
            <ul>
                <li>URL atual: <span id="current-url"></span></li>
                <li>Servidor Flask: Funcionando ✅</li>
                <li>Template: Simples (não dashboard.html)</li>
            </ul>
        </div>

        <script>
            document.getElementById('current-url').textContent = window.location.href;
            console.log('Teste dashboard carregado com sucesso!');
        </script>
    </body>
    </html>
    """

@app.route('/proposta')
def proposta():
    return render_template('proposta.html')

@app.route('/proposal_generator')
def proposal_generator():
    return render_template('proposal_generator.html')


import stripe
try:
    from deploy_service import deploy_project
    from modules.deploy.supabase_provider import validate_credentials as validate_supabase, deploy as deploy_supabase
    from modules.deploy.vercel_provider import deploy as deploy_vercel
except ImportError as e:
    print(f"[AVISO] Erro ao importar módulos de deploy: {e}")
    # Funções fallback
    def deploy_project(*args, **kwargs):
        return {"success": False, "error": "Módulo de deploy não disponível"}
    def validate_supabase(*args, **kwargs):
        return {"success": False, "error": "Provider Supabase não disponível"}
    def deploy_supabase(*args, **kwargs):
        return {"success": False, "error": "Provider Supabase não disponível"}
    def deploy_vercel(*args, **kwargs):
        return {"success": False, "error": "Provider Vercel não disponível"}

# Configura a chave secreta do Stripe
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")


# --- ROTAS DE PAGAMENTO STRIPE ---
@app.route('/api/get_step_template/<int:step_number>')
def get_step_template(step_number):
    """Serve o template HTML para uma etapa específica."""
    try:
        # Obter o nome do projeto da instância da FSM
        # Assumindo que fsm_instance tem um método para obter o nome do projeto atual
        current_project_name = fsm_instance.get_current_project_name()
        return render_template(f'steps/step_{step_number}.html', project_name=current_project_name)
    except Exception as e:
        print(f"Erro ao carregar template para etapa {step_number}: {e}")
        return f"<p>Erro ao carregar o conteúdo da etapa {step_number}.</p>", 404

@app.route('/api/stripe-public-key')
def stripe_public_key():
    stripe_public_key = os.environ.get("STRIPE_PUBLIC_KEY")
    if not stripe_public_key:
        return jsonify({"error": "Chave pública do Stripe não configurada."}), 500
    return jsonify({"publicKey": stripe_public_key})

@app.route('/api/create-checkout-session-pro', methods=['POST'])
def create_checkout_session_pro():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'brl',
                        'product_data': {
                            'name': 'Archon AI Pro Executables',
                        },
                        'unit_amount': 8900, # R$89.00 em centavos
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=url_for('payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('payment_cancel', _external=True),
        )
        return jsonify({'checkout_url': checkout_session.url})
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/api/create-checkout-session-starter', methods=['POST'])
def create_checkout_session_starter():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify(error={'message': 'O e-mail é obrigatório.'}), 400

    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=email,
            line_items=[
                {
                    'price_data': {
                        'currency': 'brl',
                        'product_data': {
                            'name': 'Archon AI Starter Kit (Código Fonte)',
                        },
                        'unit_amount': 4450, # R$ 44,50 em centavos
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=url_for('payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('payment_cancel', _external=True),
        )
        return jsonify({'checkout_url': checkout_session.url})
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.environ.get("STRIPE_WEBHOOK_SECRET")
        )
    except ValueError as e:
        # Invalid payload
        return str(e), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return str(e), 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session_data = event['data']['object']
        customer_email = session_data.get('customer_details', {}).get('email')
        
        if customer_email:
            print(f"[STRIPE WEBHOOK] Pagamento bem-sucedido para: {customer_email}")
            # Ação pós-pagamento para o executável:
            # Aqui você pode adicionar lógica para enviar um e-mail com o link de download do executável.
            # Ex: enviar_email_com_link_download(customer_email, "link_para_download_do_executavel")
        else:
            print("[STRIPE WEBHOOK] Pagamento bem-sucedido, mas e-mail do cliente não encontrado.")

    return jsonify({'status': 'success'}), 200

@app.route('/payment-success')
def payment_success():
    session_id = request.args.get('session_id')
    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            # Aqui você pode verificar o status da sessão e liberar o download
            # para o usuário logado, se aplicável.
            return render_template('success.html', session=session)
        except Exception as e:
            return render_template('cancel.html', message=str(e))
    return redirect(url_for('initial_loading'))

@app.route('/payment-cancel')
def payment_cancel():
    return render_template('cancel.html')

# --- ROTAS DE DOWNLOAD DE EXECUTÁVEIS ---
EXECUTABLES_DIR = os.path.join(BASE_DIR, "executables")

# Cria o diretório de executáveis se não existir e adiciona arquivos de exemplo
if not os.path.exists(EXECUTABLES_DIR):
    os.makedirs(EXECUTABLES_DIR)
    with open(os.path.join(EXECUTABLES_DIR, "archon-ai-windows.exe"), "w") as f:
        f.write("Conteúdo do executável Windows")
    with open(os.path.join(EXECUTABLES_DIR, "archon-ai-linux"), "w") as f:
        f.write("Conteúdo do executável Linux")
    with open(os.path.join(EXECUTABLES_DIR, "archon-ai-macos"), "w") as f:
        f.write("Conteúdo do executável macOS")

@app.route('/api/download-executables/<os_type>')
# @login_required # Comentado para desabilitar Supabase
def download_executables(os_type):
    # user_id = session.get('user_id') # Comentado para desabilitar Supabase
    # if not user_id: # Comentado para desabilitar Supabase
    #     return jsonify({"error": "Usuário não autenticado."}), 401 # Comentado para desabilitar Supabase

    try:
        # Verifica se o usuário tem acesso Pro na tabela de perfis
        # has_pro_access = True # Temporariamente True para testes sem Supabase
        # if not has_pro_access: # Comentado para desabilitar Supabase
        #     return jsonify({"error": "Acesso negado. Por favor, adquira o plano Pro."}), 403 # Comentado para desabilitar Supabase

        # Mapeia o tipo de OS para o nome do arquivo
        file_map = {
            'windows': 'archon-ai-windows.exe',
            'linux': 'archon-ai-linux',
            'macos': 'archon-ai-macos',
        }
        filename = file_map.get(os_type.lower())

        if not filename:
            return jsonify({"error": "Tipo de sistema operacional inválido."}), 400

        file_path = os.path.join(EXECUTABLES_DIR, filename)

        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            return jsonify({"error": "Arquivo não encontrado."}), 404

    except Exception as e:
        print(f"[ERRO DOWNLOAD] Falha ao liberar download: {e}")
        return jsonify({"error": f"Ocorreu um erro ao processar o download: {e}"}), 500

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
