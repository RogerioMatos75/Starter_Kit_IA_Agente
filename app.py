import os
import json
import io
import zipfile
import sys
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from flask_cors import CORS
from fsm_orquestrador import FSMOrquestrador, LOG_PATH
from valida_output import run_validation as validar_base_conhecimento
from ia_executor import executar_prompt_ia, IAExecutionError
from dotenv import load_dotenv
import stripe

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- Funções Auxiliares e Inicialização ---

def carregar_workflow(file_path="workflow.json"):
    """Carrega a definição do workflow de um arquivo JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)
        print(f"Workflow '{workflow_data.get('nome_workflow')}' carregado com sucesso.")
        return workflow_data.get("estados", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[ERRO CRÍTICO] Não foi possível carregar o workflow de '{file_path}': {e}")
        return []

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# --- Inicialização do FSM (Orquestrador) ---
project_states = carregar_workflow()
if not project_states:
    error_msg = "ERRO CRÍTICO: Falha no carregamento do workflow.json. A aplicação não pode iniciar."
    print(error_msg)
    sys.exit(1)

fsm_instance = FSMOrquestrador(project_states)
print("[INFO] Instância do FSM criada com sucesso.")


# --- ROTAS DA VITRINE (LANDING PAGE) ---

@app.route('/')
def index():
    """Serve a página de apresentação (landing.html)."""
    return render_template('landing.html')

# --- ROTAS DO PAINEL DE CONTROLE (O PRODUTO) ---

@app.route('/dashboard')
def dashboard():
    """Serve o painel de controle principal (dashboard.html)."""
    return render_template('dashboard.html')

@app.route('/api/download_templates')
def download_templates():
    """Cria um arquivo .zip com os templates e o envia para download."""
    template_dir = "documentos_base"
    if not os.path.exists(template_dir):
        return jsonify({"error": "Diretório de templates 'documentos_base' não encontrado."}), 404

    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename in os.listdir(template_dir):
            if filename.endswith(".md"):
                file_path = os.path.join(template_dir, filename)
                zf.write(file_path, arcname=filename)
    memory_file.seek(0)
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='templates_archon_ai.zip'
    )

@app.route('/api/status')
def api_status():
    """Endpoint que fornece o estado atual do projeto."""
    return jsonify(fsm_instance.get_status())

@app.route('/api/setup_project', methods=['POST'])
def setup_project():
    """Endpoint para configurar o projeto: salva arquivos e inicia o FSM."""
    project_name = request.form.get('project_name')
    if not project_name:
        return jsonify({"error": "Nome do projeto é obrigatório"}), 400

    files = request.files.getlist('files')
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    for file in files:
        if file.filename != '':
            filename_base, _ = os.path.splitext(file.filename)
            save_path = os.path.join(output_dir, f"{filename_base}.md")
            file.save(save_path)

    if not validar_base_conhecimento():
        return jsonify({
            "error": "Validação da base de conhecimento falhou. Verifique se todos os arquivos necessários (.md) foram enviados."
        }), 400

    new_status = fsm_instance.setup_project(project_name)
    return jsonify(new_status)

@app.route('/api/action', methods=['POST'])
def perform_action():
    """Endpoint que recebe as ações do supervisor."""
    data = request.json
    action = data.get('action', '').lower()
    observation = data.get('observation', '')
    project_name = data.get('project_name')
    new_status = fsm_instance.process_action(action, observation, project_name)
    return jsonify(new_status)

@app.route('/api/reset_project', methods=['POST'])
def reset_project():
    """Endpoint para resetar o projeto."""
    new_status = fsm_instance.reset_project()
    return jsonify(new_status)

@app.route('/api/logs')
def get_logs():
    """Endpoint que fornece o histórico de logs."""
    logs = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                logs = data.get('execucoes', [])
            except (json.JSONDecodeError, TypeError):
                pass
    return jsonify(logs)

@app.route('/api/consult_ai', methods=['POST'])
def consult_ai():
    """Endpoint para fazer uma consulta à IA para refinar um resultado."""
    # --- DEBUG VERCEL: Verifica a chave da API no ambiente de produção ---
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        # Imprime apenas uma parte da chave por segurança
        print(f"[DEBUG VERCEL] Chave GEMINI_API_KEY encontrada. Início: {gemini_key[:4]}, Fim: {gemini_key[-4:]}")
    else:
        print("[DEBUG VERCEL] ERRO: Variável de ambiente GEMINI_API_KEY não encontrada no servidor!")
    # --- FIM DO DEBUG ---

    data = request.json
    user_query = data.get('query', '')
    context = data.get('context', '')
    if not user_query:
        return jsonify({"error": "A consulta não pode estar vazia."}), 400

    prompt_refinamento = (
        "Atue como um assistente de engenharia de software sênior. "
        f"Analise o contexto abaixo:\n\n--- CONTEXTO ---\n{context}\n--- FIM DO CONTEXTO ---\n\n"
        f"Um supervisor humano fez a seguinte solicitação para refinar este contexto: '{user_query}'.\n\n"
        "Sua resposta:"
    )
    try:
        resposta_ia = executar_prompt_ia(prompt_refinamento)
        return jsonify({"refined_content": resposta_ia})
    except IAExecutionError as e:
        # Log do erro no servidor para facilitar a depuração
        print(f"[ERRO /api/consult_ai] IAExecutionError: {e}")
        return jsonify({"error": f"Ocorreu um erro ao consultar a IA: {e}"}), 500

# --- ROTAS DE GERENCIAMENTO DE API KEYS ---

@app.route('/api/check_api_key')
def check_api_key():
    """Verifica se a GEMINI_API_KEY está configurada no ambiente."""
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    is_configured = bool(gemini_api_key and gemini_api_key.strip() != '""')
    return jsonify({"is_configured": is_configured})

@app.route('/api/test_gemini_connection', methods=['POST'])
def test_gemini_connection():
    """Tenta fazer uma chamada simples à IA para verificar a conexão e a validade da chave."""
    try:
        # Um prompt simples para testar a conexão
        test_prompt = "Olá, você está funcionando? Responda com 'Sim, estou online!'."
        response = executar_prompt_ia(test_prompt)
        if "sim, estou online" in response.lower():
            return jsonify({"success": True, "message": "Conexão com a API Gemini bem-sucedida!"}), 200
        else:
            return jsonify({"success": False, "message": f"API Gemini respondeu, mas com conteúdo inesperado: {response[:50]}..."}), 200
    except IAExecutionError as e:
        return jsonify({"success": False, "message": f"Falha na conexão com a API Gemini: {e}"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Ocorreu um erro inesperado ao testar a conexão: {e}"}), 500

@app.route('/api/list_api_keys')
def list_api_keys():
    """Lista dinamicamente todas as API keys configuradas no ambiente."""
    configured_keys = []
    for env_var, value in os.environ.items():
        if env_var.endswith('_API_KEY') and value:
            provider_name = env_var.replace('_API_KEY', '').lower()
            configured_keys.append({
                "provider": provider_name,
                "status": "active",
                "lastCheck": "Configurada"
            })
    return jsonify({"keys": configured_keys})

@app.route('/api/save_api_key', methods=['POST'])
def save_api_key():
    """Salva uma chave de API no arquivo .env."""
    data = request.json
    api_key = data.get('api_key')
    provider_name = data.get('provider')

    if not api_key or not api_key.strip():
        return jsonify({"error": "API Key não pode ser vazia."}), 400
    if not provider_name or not provider_name.strip():
        return jsonify({"error": "Nome do provedor é obrigatório."}), 400

    env_var = f"{provider_name.upper().replace(' ', '_')}_API_KEY"

    try:
        env_vars = {}
        if os.path.exists('.env'):
            with open('.env', 'r', encoding='utf-8') as f:
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        env_vars[key.strip()] = value.strip()
        
        env_vars[env_var] = f'"{api_key}"'

        with open('.env', 'w', encoding='utf-8') as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")
        
        load_dotenv(override=True)
        
        return jsonify({"message": f"API Key para {provider_name.title()} salva! Por favor, reinicie o servidor para aplicar as alterações."}), 200
    except Exception as e:
        return jsonify({"error": f"Falha ao salvar a chave no arquivo .env: {e}"}), 500

@app.route('/api/remove_api_key', methods=['POST'])
def remove_api_key():
    """Remove uma chave de API do arquivo .env."""
    data = request.json
    provider_name = data.get('provider')

    if not provider_name or not provider_name.strip():
        return jsonify({"error": "Nome do provedor é obrigatório para remoção."}), 400

    env_var = f"{provider_name.upper().replace(' ', '_')}_API_KEY"

    try:
        env_vars = {}
        if os.path.exists('.env'):
            with open('.env', 'r', encoding='utf-8') as f:
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        env_vars[key.strip()] = value.strip()
        
        if env_var in env_vars:
            del env_vars[env_var]

        with open('.env', 'w', encoding='utf-8') as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")
        
        load_dotenv(override=True)
        
        return jsonify({"message": f"API Key para {provider_name.title()} removida com sucesso! Por favor, reinicie o servidor para aplicar as alterações."}), 200
    except Exception as e:
        return jsonify({"error": f"Falha ao remover a chave do arquivo .env: {e}"}), 500

# --- ROTAS DE PAGAMENTO (Stripe) ---

# Configura a chave secreta do Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Cria uma sessão de checkout no Stripe."""
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'E-mail é obrigatório'}), 400

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card', 'boleto'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'brl',
                        'product_data': {
                            'name': 'Archon AI - Plano Starter',
                            'images': [url_for('static', filename='assets/5logo_Archon.png', _external=True)],
                        },
                        'unit_amount': 4450,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=url_for('success', _external=True),
            cancel_url=url_for('cancel', _external=True),
            customer_email=email,
            metadata={
                'github_repo': os.getenv('GITHUB_REPO_URL')
            }
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/success')
def success():
    """Página de sucesso após o pagamento."""
    return render_template('success.html')

@app.route('/cancel')
def cancel():
    """Página de cancelamento do pagamento."""
    return render_template('cancel.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint que recebe notificações (webhooks) do Stripe."""
    event = None
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

    if not webhook_secret:
        return jsonify(error="Configuração de servidor incompleta"), 500

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        return jsonify(error=str(e)), 400
    except stripe.error.SignatureVerificationError as e:
        return jsonify(error=str(e)), 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session['customer_details']['email']
        repo_url = session['metadata'].get('github_repo', 'URL_DO_REPO_NAO_CONFIGURADA')
        print(f"[SUCESSO PAGAMENTO] Pagamento recebido de: {customer_email}")
        print(f"-> [AÇÃO] Enviando e-mail com o link do repositório: {repo_url} para {customer_email}")
        # TODO: Implementar a lógica de envio de e-mail aqui.

    return jsonify(success=True), 200

# --- Bloco de Execução Principal ---

if __name__ == '__main__':
    print("-" * 50)
    print("Iniciando Archon AI (Servidor de Desenvolvimento Completo)...")
    print("Acesse a Landing Page em http://127.0.0.1:5001")
    print("Acesse o Painel de Controle em http://127.0.0.1:5001/dashboard")
    app.run(debug=True, port=5001)
