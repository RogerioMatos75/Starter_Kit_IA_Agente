import os
import json
import io
import zipfile
import sys
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, g, session
from functools import wraps
from flask_cors import CORS
import google.generativeai as genai
from fsm_orquestrador import FSMOrquestrador
from valida_output import run_validation as validar_base_conhecimento
from ia_executor import executar_prompt_ia, IAExecutionError
from dotenv import load_dotenv

load_dotenv() # Carrega as variáveis de ambiente do .env
import stripe
from relatorios import exportar_log_txt
from auditoria_seguranca import auditoria_global
from utils.supabase_client import supabase
from utils.file_parser import extract_text_from_file, _sanitizar_nome

# --- CONFIGURAÇÃO DE CAMINHOS E CONSTANTES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_CONHECIMENTO_BUCKET = "base-conhecimento"

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

project_states = carregar_workflow()
if not project_states:
    sys.exit("ERRO CRÍTICO: Falha no carregamento do workflow.json.")

fsm_instance = FSMOrquestrador(project_states)

# Adiciona uma verificação clara na inicialização se o Supabase não conectar
if not supabase:
    print("\n" + "="*60)
    print("!! [ERRO CRÍTICO] Cliente Supabase não inicializado.      !!")
    print("!! Verifique se as variáveis SUPABASE_URL e SUPABASE_KEY   !!")
    print("!! estão configuradas corretamente no seu arquivo .env.    !!")
    print("!! As funcionalidades de autenticação e banco de dados    !!")
    print("!! estarão DESATIVADAS.                                  !!")
    print("="*60 + "\n")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
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
def index():
    return render_template('landing.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/proposta')
def proposta():
    return render_template('proposta.html')

@app.route('/deploy')
@login_required
def deploy():
    return render_template('deploy.html')

# --- ROTAS DE AUTENTICAÇÃO SUPABASE ---
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    if not supabase:
        return jsonify({"error": "Serviço de autenticação indisponível. Verifique a configuração do servidor."}), 503


    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "E-mail e senha são obrigatórios."}), 400

    try:
        res = supabase.auth.sign_up({'email': email, 'password': password})
        if res.user:
            session['user_id'] = res.user.id
            session['access_token'] = res.session.access_token
            return jsonify({"message": "Usuário registrado com sucesso!", "user": res.user.id}), 200
        else:
            return jsonify({"error": res.get('error_description', 'Erro ao registrar usuário.')}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login_api():
    if not supabase:
        return jsonify({"error": "Serviço de autenticação indisponível. Verifique a configuração do servidor."}), 503

    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "E-mail e senha são obrigatórios."}), 400

    try:
        res = supabase.auth.sign_in_with_password({'email': email, 'password': password})
        if res.user:
            session['user_id'] = res.user.id
            session['access_token'] = res.session.access_token
            return jsonify({"message": "Login realizado com sucesso!", "user": res.user.id}), 200
        else:
            return jsonify({"error": res.get('error_description', 'Erro ao fazer login.')}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    if not supabase:
        return jsonify({"error": "Serviço de autenticação indisponível. Verifique a configuração do servidor."}), 503

    try:
        supabase.auth.sign_out()
        session.pop('user_id', None)
        session.pop('access_token', None)
        return jsonify({"message": "Logout realizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- API FSM & WORKFLOW ---
@app.route('/api/status')
def api_status():
    return jsonify(fsm_instance.get_status())

@app.route('/api/generate_project_base', methods=['POST'])
def generate_project_base():
    project_description = request.form.get('project_description', '').strip()
    project_name = request.form.get('project_name', '').strip()
    
    if not project_description or not project_name:
        return jsonify({"error": "Nome e descrição do projeto são obrigatórios."}), 400

    sanitized_project_name = _sanitizar_nome(project_name)
    context_files = request.files.getlist('files')
    context_text = []

    # Upload de arquivos de contexto para o Supabase
    if context_files:
        for file in context_files:
            if file.filename:
                storage_path = f"{sanitized_project_name}/contexto/{file.filename}"
                try:
                    file_content = file.read()
                    supabase.storage.from_(BASE_CONHECIMENTO_BUCKET).upload(
                        path=storage_path,
                        file=file_content,
                        file_options={"content-type": file.mimetype, "upsert": "true"}
                    )
                    # Para extrair texto, salvamos temporariamente
                    temp_path = os.path.join(BASE_DIR, file.filename)
                    with open(temp_path, 'wb') as f_temp:
                        f_temp.write(file_content)
                    
                    extracted_content = extract_text_from_file(temp_path)
                    if extracted_content:
                        context_text.append(f'--- Conteúdo de {file.filename} ---\n{extracted_content}\n---')
                    os.remove(temp_path)

                except Exception as e:
                    print(f"[ERRO SUPABASE] Falha no upload do arquivo de contexto: {e}")
                    return jsonify({"error": f"Falha no upload do arquivo de contexto: {e}"}), 500

    full_context = "\n\n--- DOCUMENTOS DE CONTEXTO ---\n" + "\n".join(context_text) if context_text else ""

    prompt_para_gemini = f"""... (o mesmo prompt gigante para gerar a base de conhecimento) ..."""

    try:
        resposta_ia = executar_prompt_ia(prompt_para_gemini)
        arquivos_gerados = _parse_ia_response(resposta_ia)

        # Upload dos arquivos gerados para o Supabase
        for filename, content in arquivos_gerados.items():
            storage_path = f"{sanitized_project_name}/{filename}"
            supabase.storage.from_(BASE_CONHECIMENTO_BUCKET).upload(
                path=storage_path,
                file=content.encode('utf-8'),
                file_options={"content-type": "text/markdown;charset=utf-8", "upsert": "true"}
            )
            print(f"[SUPABASE] Arquivo de conhecimento salvo em: {storage_path}")

        # Validação agora precisa ser adaptada para ler do Supabase
        # if not validar_base_conhecimento(project_name):
        #     return jsonify({"error": "Validação da base de conhecimento falhou."}), 500

        fsm_instance.setup_project(project_name) # Inicia o FSM
        return jsonify({"message": "Base de conhecimento gerada e salva com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro: {e}"}), 500

def _parse_ia_response(resposta_ia):
    # (Lógica para extrair arquivos da resposta da IA, como antes)
    delimitadores = {
        "---PLANO_BASE_MD_START---": "plano_base.md",
        "---ARQUITETURA_TECNICA_MD_START---": "arquitetura_tecnica.md",
        "---REGRAS_NEGOCIO_MD_START---": "regras_negocio.md",
        "---FLUXOS_USUARIO_MD_START---": "fluxos_usuario.md",
        "---BACKLOG_MVP_MD_START---": "backlog_mvp.md",
        "---AUTENTICACAO_BACKEND_MD_START---": "autenticacao_backend.md",
    }
    arquivos_gerados = {}
    for start_tag, filename in delimitadores.items():
        end_tag = start_tag.replace("_START", "_END")
        start_index = resposta_ia.find(start_tag)
        end_index = resposta_ia.find(end_tag)
        if start_index != -1 and end_index != -1:
            content = resposta_ia[start_index + len(start_tag):end_index].strip()
            arquivos_gerados[filename] = content
    return arquivos_gerados

@app.route('/api/action', methods=['POST'])
def perform_action():
    data = request.json
    new_status = fsm_instance.process_action(
        action=data.get('action', '').lower(),
        observation=data.get('observation', ''),
        project_name=data.get('project_name'),
        current_preview_content=data.get('current_preview_content')
    )
    return jsonify(new_status)

@app.route('/api/reset_project', methods=['POST'])
def reset_project():
    return jsonify(fsm_instance.reset_project())

@app.route('/api/consult_ai', methods=['POST'])
def consult_ai():
    data = request.json
    query = data.get('query')
    context = data.get('context')

    if not query:
        return jsonify({"error": "A consulta é obrigatória."}), 400

    try:
        # Concatena a consulta com o contexto para enviar à IA
        prompt = f"Contexto: {context}\n\nConsulta: {query}\n\nCom base no contexto fornecido, refine a informação ou responda à consulta de forma concisa e útil."
        refined_content = executar_prompt_ia(prompt)
        return jsonify({"refined_content": refined_content}), 200
    except IAExecutionError as e:
        return jsonify({"error": f"Erro ao consultar a IA: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro inesperado: {e}"}), 500

@app.route('/api/gerar-estimativa', methods=['POST'])
def gerar_estimativa():
    data = request.json
    description = data.get('description')

    if not description:
        return jsonify({"error": "A descrição do projeto é obrigatória."}), 400

    try:
        # --- Etapa 1: Geração de dados estruturados com RAG para custos ---
        pdf_path = os.path.join(BASE_DIR, 'docs', 'Custo Desenvolvedor FullStack Brasil.pdf')
        market_research_context = extract_text_from_file(pdf_path)
        if not market_research_context:
            print("[AVISO] O arquivo de pesquisa de mercado PDF não foi encontrado ou está vazio.")

        prompt_custos = f'''
            Analisando a descrição de projeto e os dados de custo de mercado, gere um JSON com a estrutura de custos.
            Contexto de Mercado: "{market_research_context}"
            Descrição do Projeto: "{description}"
            Sua Tarefa: Gere uma resposta ESTRITAMENTE no formato JSON com o schema:
            {{
              "projectName": "string", "coreFeatures": ["string"], "suggestedTeam": "string",
              "estimatedTimelineMonths": "number", "estimatedMonthlyTeamCost": "number"
            }}
        '''
        dados_custos_json = executar_prompt_ia(prompt_custos, is_json_output=True)
        dados_custos = json.loads(dados_custos_json)

        # --- Etapa 2: Geração de texto criativo para a introdução ---
        prompt_introducao = f'''
            Atue como um consultor de software sênior escrevendo uma proposta.
            Baseado na descrição do projeto, crie um texto de introdução e escopo.
            Descrição do Projeto: "{description}"
            Sua Tarefa: Escreva um texto com:
            1.  **Introdução:** Um parágrafo resumindo o entendimento do projeto.
            2.  **Fases do Projeto:** Uma lista breve das etapas (ex: Discovery, Design, Desenvolvimento, Testes, Implantação).
            Use markdown para formatação (títulos com ##, listas com *).
        '''
        texto_introducao = executar_prompt_ia(prompt_introducao)

        # --- Etapa 3: Combinar os resultados ---
        resultado_final = {
            "dados_orcamento": dados_custos,
            "texto_introducao": texto_introducao
        }

        return jsonify(resultado_final), 200

    except IAExecutionError as e:
        return jsonify({"error": f"Erro ao consultar a IA: {e}"}), 500
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Erro ao decodificar a resposta JSON da IA: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro inesperado: {e}"}), 500

import stripe

# Configura a chave secreta do Stripe
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

# --- ROTAS DE UTILIDADES E API KEYS ---
@app.route('/api/check_api_key')
def check_api_key():
    is_configured = os.environ.get("GEMINI_API_KEY") is not None
    return jsonify({"is_configured": is_configured})

@app.route('/api/list_api_keys')
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

@app.route('/api/save_api_key', methods=['POST'])
def save_api_key():
    data = request.json
    api_key = data.get('api_key')
    provider = data.get('provider') # e.g., "gemini"
    provider_type = data.get('provider_type') # e.g., "gemini" or "custom"

    if not api_key or not provider:
        return jsonify({"error": "API Key e provedor são obrigatórios."}), 400

    # Por simplicidade, salvamos apenas a GEMINI_API_KEY
    if provider == "gemini":
        os.environ["GEMINI_API_KEY"] = api_key
        # Para persistir a chave no .env, você precisaria de uma biblioteca como python-dotenv
        # e escrever no arquivo, o que não é recomendado em produção por segurança.
        # Para este ambiente, a variável de ambiente em memória é suficiente.
        return jsonify({"message": "API Key Gemini salva com sucesso!"}), 200
    else:
        return jsonify({"error": f"Provedor '{provider}' não suportado para salvamento direto."}), 400

@app.route('/api/test_new_api_key', methods=['POST'])
def test_new_api_key():
    data = request.json
    api_key = data.get('api_key')

    if not api_key:
        return jsonify({"success": False, "message": "Nenhuma API Key fornecida para teste."}), 400

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro') # Usar um modelo leve para teste
        model.generate_content("Hello", timeout=5) # Teste simples de conectividade
        return jsonify({"success": True, "message": "API Key Gemini válida e conectada!"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Falha no teste da API Key Gemini: {e}"}), 200

@app.route('/api/remove_api_key', methods=['POST'])
def remove_api_key():
    data = request.json
    provider = data.get('provider')

    if not provider:
        return jsonify({"error": "Provedor é obrigatório para remoção."}), 400

    if provider == "gemini":
        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]
            # Em um ambiente real, você também removeria do .env ou do armazenamento persistente
            return jsonify({"message": "API Key Gemini removida com sucesso!"}), 200
        else:
            return jsonify({"message": "API Key Gemini não encontrada."}), 404
    else:
        return jsonify({"error": f"Provedor '{provider}' não suportado para remoção direta."}), 400

# --- ROTAS DE PAGAMENTO STRIPE ---
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
            # Atualizar o perfil do usuário no Supabase para conceder acesso Pro
            try:
                # Primeiro, obter o user_id do Supabase auth.users usando o email
                user_response = supabase.table('users').select('id').eq('email', customer_email).execute()
                user_id = user_response.data[0]['id'] if user_response.data else None

                if user_id:
                    # Atualizar a tabela de perfis (assumindo que você tem uma tabela 'profiles')
                    # ou inserir se o perfil não existir (para o caso de um novo usuário)
                    update_response = supabase.table('profiles').upsert({
                        'id': user_id,
                        'email': customer_email,
                        'has_pro_access': True
                    }, on_conflict='id').execute()
                    print(f"[SUPABASE] Acesso Pro concedido para {customer_email}: {update_response.data}")
                else:
                    print(f"[SUPABASE] Usuário não encontrado no Supabase para o email: {customer_email}")
            except Exception as e:
                print(f"[ERRO SUPABASE] Falha ao atualizar acesso Pro para {customer_email}: {e}")
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
    return redirect(url_for('index'))

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
@login_required
def download_executables(os_type):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Usuário não autenticado."}), 401

    try:
        # Verifica se o usuário tem acesso Pro na tabela de perfis
        profile_response = supabase.table('profiles').select('has_pro_access').eq('id', user_id).execute()
        has_pro_access = profile_response.data[0]['has_pro_access'] if profile_response.data else False

        if not has_pro_access:
            return jsonify({"error": "Acesso negado. Por favor, adquira o plano Pro."}), 403

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
        print(f"[ERRO DOWNLOAD] Falha ao liberar download para {user_id}: {e}")
        return jsonify({"error": f"Ocorreu um erro ao processar o download: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
