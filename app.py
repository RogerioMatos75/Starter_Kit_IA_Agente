import os
import json
import io
import zipfile
import sys
import datetime
import subprocess
import time
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

project_states = carregar_workflow()
if not project_states:
    sys.exit("ERRO CRÍTICO: Falha no carregamento do workflow.json.")

fsm_instance = FSMOrquestrador(project_states)

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
    return render_template('dashboard_new.html')

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

@app.route('/deploy')
# @login_required # Comentado para desabilitar Supabase
def deploy():
    # Redireciona para o dashboard na Etapa 7 (Deploy integrado)
    return redirect(url_for('dashboard') + '#step-7')

# --- ROTAS DE AUTENTICAÇÃO SUPABASE --- # Comentado para desabilitar Supabase
# @app.route('/api/auth/signup', methods=['POST']) # Comentado para desabilitar Supabase
# def signup(): # Comentado para desabilitar Supabase
#     if not supabase: # Comentado para desabilitar Supabase
#         return jsonify({"error": "Serviço de autenticação indisponível. Verifique a configuração do servidor."}), 503


#     data = request.json # Comentado para desabilitar Supabase
#     email = data.get('email') # Comentado para desabilitar Supabase
#     password = data.get('password') # Comentado para desabilitar Supabase

#     if not email or not password: # Comentado para desabilitar Supabase
#         return jsonify({"error": "E-mail e senha são obrigatórios."}), 400 # Comentado para desabilitar Supabase

#     try: # Comentado para desabilitar Supabase
#         res = supabase.auth.sign_up({'email': email, 'password': password}) # Comentado para desabilitar Supabase
#         if res.user: # Comentado para desabilitar Supabase
#             session['user_id'] = res.user.id # Comentado para desabilitar Supabase
#             session['access_token'] = res.session.access_token # Comentado para desabilitar Supabase
#             return jsonify({"message": "Usuário registrado com sucesso!", "user": res.user.id}), 200 # Comentado para desabilitar Supabase
#         else: # Comentado para desabilitar Supabase
#             return jsonify({"error": res.get('error_description', 'Erro ao registrar usuário.')}), 400 # Comentado para desabilitar Supabase
#     except Exception as e: # Comentado para desabilitar Supabase
#         return jsonify({"error": str(e)}), 500 # Comentado para desabilitar Supabase

# @app.route('/api/auth/login', methods=['POST']) # Comentado para desabilitar Supabase
# def login_api(): # Comentado para desabilitar Supabase
#     if not supabase: # Comentado para desabilitar Supabase
#         return jsonify({"error": "Serviço de autenticação indisponível. Verifique a configuração do servidor."}), 503 # Comentado para desabilitar Supabase

#     data = request.json # Comentado para desabilitar Supabase
#     email = data.get('email') # Comentado para desabilitar Supabase
#     password = data.get('password') # Comentado para desabilitar Supabase

#     if not email or not password: # Comentado para desabilitar Supabase
#         return jsonify({"error": "E-mail e senha são obrigatórios."}), 400 # Comentado para desabilitar Supabase

#     try: # Comentado para desabilitar Supabase
#         res = supabase.auth.sign_in_with_password({'email': email, 'password': password}) # Comentado para desabilitar Supabase
#         if res.user: # Comentado para desabilitar Supabase
#             session['user_id'] = res.user.id # Comentado para desabilitar Supabase
#             session['access_token'] = res.session.access_token # Comentado para desabilitar Supabase
#             return jsonify({"message": "Login realizado com sucesso!", "user": res.user.id}), 200 # Comentado para desabilitar Supabase
#         else: # Comentado para desabilitar Supabase
#             return jsonify({"error": res.get('error_description', 'Erro ao fazer login.')}), 400 # Comentado para desabilitar Supabase
#     except Exception as e: # Comentado para desabilitar Supabase
#         return jsonify({"error": str(e)}), 500 # Comentado para desabilitar Supabase

# @app.route('/api/auth/logout', methods=['POST']) # Comentado para desabilitar Supabase
# def logout(): # Comentado para desabilitar Supabase
#     if not supabase: # Comentado para desabilitar Supabase
#         return jsonify({"error": "Serviço de autenticação indisponível. Verifique a configuração do servidor."}), 503 # Comentado para desabilitar Supabase

#     try: # Comentado para desabilitar Supabase
#         supabase.auth.sign_out() # Comentado para desabilitar Supabase
#         session.pop('user_id', None) # Comentado para desabilitar Supabase
#         session.pop('access_token', None) # Comentado para desabilitar Supabase
#         return jsonify({"message": "Logout realizado com sucesso!"}), 200 # Comentado para desabilitar Supabase
#     except Exception as e: # Comentado para desabilitar Supabase
#         return jsonify({"error": str(e)}), 500 # Comentado para desabilitar Supabase

# --- API FSM & WORKFLOW ---
@app.route('/api/status')
def api_status():
    return jsonify(fsm_instance.get_status())

@app.route('/api/logs')
def api_logs():
    """Retorna os logs de execução do sistema"""
    try:
        from fsm_orquestrador import carregar_logs
        logs = carregar_logs()

        # Formata os logs para o frontend
        formatted_logs = []
        for log in logs:
            formatted_logs.append({
                'id': hash(log.get('data_hora', '') + log.get('etapa', '')),
                'timestamp': log.get('data_hora', ''),
                'stage': log.get('etapa', 'Desconhecido'),
                'status': log.get('status', 'unknown'),
                'decision': log.get('decisao', ''),
                'task': log.get('tarefa', ''),
                'response': log.get('resposta_agente', ''),
                'observation': log.get('observacao', '')
            })

        return jsonify({'logs': formatted_logs})
    except Exception as e:
        print(f"[ERRO] Falha ao carregar logs: {e}")
        return jsonify({'logs': [], 'error': str(e)})

@app.route('/api/generate_project_base', methods=['POST'])
def generate_project_base():
    project_description = request.form.get('project_description', '').strip()
    project_name = request.form.get('project_name', '').strip()
    
    if not project_description or not project_name:
        return jsonify({"error": "Nome e descrição do projeto são obrigatórios."}), 400

    sanitized_project_name = _sanitizar_nome(project_name)
    context_files = request.files.getlist('files')
    context_text = []

    # Salvar arquivos de contexto localmente
    project_output_dir = os.path.join(BASE_DIR, "output", sanitized_project_name)
    os.makedirs(project_output_dir, exist_ok=True)

    if context_files:
        for file in context_files:
            if file.filename:
                file_path = os.path.join(project_output_dir, file.filename)
                try:
                    file_content = file.read()
                    with open(file_path, 'wb') as f_out:
                        f_out.write(file_content)
                    
                    extracted_content = extract_text_from_file(file_path)
                    if extracted_content:
                        context_text.append(f'--- Conteúdo de {file.filename} ---\n{extracted_content}\n---')

                except Exception as e:
                    print(f"[ERRO] Falha ao salvar arquivo de contexto localmente: {e}")
                    return jsonify({"error": f"Falha ao salvar arquivo de contexto: {e}"}), 500

    full_context = "\n\n--- DOCUMENTOS DE CONTEXTO ---\n" + "\n".join(context_text) if context_text else ""

    prompt_para_gemini = f"""... (o mesmo prompt gigante para gerar a base de conhecimento) ..."""

    try:
        resposta_ia = executar_prompt_ia(prompt_para_gemini)
        arquivos_gerados = _parse_ia_response(resposta_ia)

        # Salvar arquivos gerados localmente
        for filename, content in arquivos_gerados.items():
            file_path = os.path.join(project_output_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f_out:
                f_out.write(content)
            print(f"[INFO] Arquivo de conhecimento salvo em: {file_path}")

        # Validação agora precisa ser adaptada para ler do diretório local
        # if not validar_base_conhecimento(project_name): # Manter esta linha se a validação for adaptada
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


@app.route('/api/define_layout', methods=['POST'])
def define_layout():
    data = request.json
    project_name = data.get('project_name')
    layout_spec = data.get('layout_spec')

    if not project_name or not layout_spec:
        return jsonify({"error": "Nome do projeto e especificação de layout são obrigatórios."}), 400

    try:
        # Aqui, em vez de chamar uma função complexa, passamos os dados para o orquestrador
        # O orquestrador será responsável por salvar o artefato.
        fsm_instance.process_layout_definition(project_name, layout_spec)
        return jsonify({"message": "Especificação de layout salva com sucesso!"}), 200
    except Exception as e:
        print(f"[ERRO API] Falha ao processar a definição de layout: {e}")
        return jsonify({"error": str(e)}), 500

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

def _simulate_deploy(provider, project_name):
    """Simula um processo de deploy e retorna o output."""
    output = []
    output.append(f"[{provider.upper()}] Iniciando deploy para o projeto: {project_name}...")
    time.sleep(1)
    output.append(f"[{provider.upper()}] Conectando ao repositório...")
    time.sleep(2)
    output.append(f"[{provider.upper()}] Instalando dependências...")
    time.sleep(3)
    output.append(f"[{provider.upper()}] Realizando o build do projeto...")
    time.sleep(4)
    output.append(f"[{provider.upper()}] Build concluído com sucesso.")
    time.sleep(1)
    output.append(f"[{provider.upper()}] Publicando a nova versão...")
    time.sleep(2)
    project_url = f"https://{project_name.lower().replace('_', '-')}.vercel.app"
    output.append(f"[{provider.upper()}] Deploy finalizado! URL: {project_url}")
    return "\n".join(output)

@app.route('/api/execute_deploy', methods=['POST'])
def execute_deploy():
    data = request.json
    provider = data.get('provider')
    project_name = data.get('project_name')
    vercel_token = data.get('vercel_token')

    if not provider or not project_name:
        return jsonify({"error": "Provedor e nome do projeto são obrigatórios."}), 400

    if provider == 'vercel':
        if not vercel_token:
            return jsonify({"error": "Token da Vercel é obrigatório para o deploy."}), 400
        
        print(f"[DEPLOY] Recebido token da Vercel: ...{vercel_token[-4:]}")

        try:
            deploy_output = _simulate_deploy('vercel', project_name)
            
            from fsm_orquestrador import registrar_log
            registrar_log(
                etapa="Deploy",
                status="concluída",
                decisao=f"Deploy na Vercel iniciado pelo usuário.",
                resposta_agente=deploy_output,
                tarefa=f"Deploy Vercel: {project_name}"
            )
            
            return jsonify({"output": deploy_output}), 200
        except Exception as e:
            return jsonify({"error": f"Falha na simulação do deploy: {e}"}), 500
    else:
        return jsonify({"error": f"Provedor de deploy '{provider}' não é suportado."}), 400

import stripe
try:
    from deploy_service import deploy_project
    from providers.supabase_provider import validate_credentials as validate_supabase, deploy as deploy_supabase
    from providers.vercel_provider import deploy as deploy_vercel
except ImportError as e:
    print(f"[AVISO] Erro ao importar módulos de deploy: {e}")
    # Funções fallback
    def deploy_project(*args, **kwargs):
        return {"success": False, "error": "Módulo de deploy não disponível"}
    def validate_supabase(*args, **kwargs):
        return {"success": False, "error": "Provider Supabase não disponível"}
    def deploy_supabase(*args, **kwargs):
        return {"success": False, "error": "Provider Supabase n��o disponível"}
    def deploy_vercel(*args, **kwargs):
        return {"success": False, "error": "Provider Vercel não disponível"}

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

# --- ROTAS DE DEPLOY E PROVISIONAMENTO ---
@app.route('/api/deploy/save_credentials', methods=['POST'])
def save_deploy_credentials():
    """Salva as credenciais dos providers de deploy"""
    data = request.json

    vercel_token = data.get('vercel_token', '').strip()
    supabase_url = data.get('supabase_url', '').strip()
    supabase_key = data.get('supabase_key', '').strip()
    stripe_secret = data.get('stripe_secret', '').strip()
    stripe_public = data.get('stripe_public', '').strip()

    try:
        # Salva as credenciais nas variáveis de ambiente
        if vercel_token:
            os.environ["VERCEL_TOKEN"] = vercel_token
        if supabase_url:
            os.environ["SUPABASE_URL"] = supabase_url
        if supabase_key:
            os.environ["SUPABASE_SERVICE_ROLE_KEY"] = supabase_key
        if stripe_secret:
            os.environ["STRIPE_SECRET_KEY"] = stripe_secret
            stripe.api_key = stripe_secret  # Atualiza a configuração do Stripe
        if stripe_public:
            os.environ["STRIPE_PUBLIC_KEY"] = stripe_public

        return jsonify({"message": "Credenciais salvas com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao salvar credenciais: {str(e)}"}), 500

@app.route('/api/deploy/validate_credentials', methods=['POST'])
def validate_deploy_credentials():
    """Valida as credenciais dos providers"""
    results = {}

    # Validar Vercel
    vercel_token = os.environ.get("VERCEL_TOKEN")
    if vercel_token:
        try:
            # Teste simples: tentar listar projetos
            result = subprocess.run(
                ["vercel", "ls", "--token", vercel_token],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                results["vercel"] = {"status": "valid", "message": "Token Vercel válido"}
            else:
                results["vercel"] = {"status": "invalid", "message": "Token Vercel inválido"}
        except Exception as e:
            results["vercel"] = {"status": "error", "message": f"Erro ao validar Vercel: {str(e)}"}
    else:
        results["vercel"] = {"status": "missing", "message": "Token Vercel não configurado"}

    # Validar Supabase
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if supabase_url and supabase_key:
        try:
            # Extrair project_ref da URL
            project_ref = supabase_url.split("//")[1].split(".")[0] if "//" in supabase_url else ""
            validation_result = validate_supabase(supabase_key, project_ref)
            if validation_result.get("success"):
                results["supabase"] = {"status": "valid", "message": "Credenciais Supabase válidas"}
            else:
                results["supabase"] = {"status": "invalid", "message": validation_result.get("error", "Credenciais inválidas")}
        except Exception as e:
            results["supabase"] = {"status": "error", "message": f"Erro ao validar Supabase: {str(e)}"}
    else:
        results["supabase"] = {"status": "missing", "message": "Credenciais Supabase não configuradas"}

    # Validar Stripe
    stripe_secret = os.environ.get("STRIPE_SECRET_KEY")
    if stripe_secret:
        try:
            stripe.api_key = stripe_secret
            # Teste simples: listar algumas transações
            stripe.Account.retrieve()
            results["stripe"] = {"status": "valid", "message": "Chave Stripe válida"}
        except Exception as e:
            results["stripe"] = {"status": "invalid", "message": f"Chave Stripe inválida: {str(e)}"}
    else:
        results["stripe"] = {"status": "missing", "message": "Chave Stripe não configurada"}

    return jsonify({"results": results}), 200

@app.route('/api/deploy/provision_database', methods=['POST'])
def provision_database():
    """Provisiona o banco de dados no Supabase"""
    data = request.json
    project_name = data.get('project_name', 'default-project')

    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not supabase_key:
        return jsonify({"error": "Credenciais Supabase não configuradas"}), 400

    try:
        # Extrair project_ref da URL
        project_ref = supabase_url.split("//")[1].split(".")[0] if "//" in supabase_url else ""
        result = deploy_supabase(supabase_key, project_ref)

        if result.get("success"):
            return jsonify({
                "message": "Banco de dados provisionado com sucesso!",
                "output": result.get("output", {})
            }), 200
        else:
            return jsonify({"error": result.get("error", "Erro desconhecido")}), 500
    except Exception as e:
        return jsonify({"error": f"Erro ao provisionar banco: {str(e)}"}), 500

@app.route('/api/deploy/deploy_frontend', methods=['POST'])
def deploy_frontend():
    """Faz o deploy do frontend na Vercel"""
    data = request.json
    project_name = data.get('project_name', 'default-project')

    vercel_token = os.environ.get("VERCEL_TOKEN")

    if not vercel_token:
        return jsonify({"error": "Token Vercel não configurado"}), 400

    try:
        result = deploy_vercel(vercel_token)

        if result.get("success"):
            return jsonify({
                "message": "Deploy do frontend realizado com sucesso!",
                "output": result.get("output", "")
            }), 200
        else:
            return jsonify({"error": result.get("error", "Erro desconhecido")}), 500
    except Exception as e:
        return jsonify({"error": f"Erro ao fazer deploy: {str(e)}"}), 500

@app.route('/api/deploy/setup_payments', methods=['POST'])
def setup_payments():
    """Configura o sistema de pagamentos Stripe"""
    data = request.json
    project_name = data.get('project_name', 'default-project')

    stripe_secret = os.environ.get("STRIPE_SECRET_KEY")
    stripe_public = os.environ.get("STRIPE_PUBLIC_KEY")

    if not stripe_secret:
        return jsonify({"error": "Chave secreta Stripe não configurada"}), 400

    try:
        # Configurar webhook endpoints se necessário
        # Criar produtos padrão se necessário
        stripe.api_key = stripe_secret

        # Verificar se a conta está ativa
        account = stripe.Account.retrieve()

        output = [
            f"✅ Conta Stripe verificada: {account.get('email', 'N/A')}",
            f"✅ Moeda padrão: {account.get('default_currency', 'N/A').upper()}",
            f"✅ Pagamentos habilitados: {'Sim' if account.get('charges_enabled') else 'Não'}",
        ]

        if stripe_public:
            output.append(f"✅ Chave pública configurada: {stripe_public[:12]}...")

        return jsonify({
            "message": "Sistema de pagamentos configurado com sucesso!",
            "output": "\n".join(output)
        }), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao configurar pagamentos: {str(e)}"}), 500

@app.route('/api/deploy/complete_deploy', methods=['POST'])
def complete_deploy():
    """Executa o deploy completo (todos os providers)"""
    data = request.json
    project_name = data.get('project_name', 'default-project')

    results = {}

    try:
        # 1. Provisionar banco (Supabase)
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

        if supabase_url and supabase_key:
            project_ref = supabase_url.split("//")[1].split(".")[0] if "//" in supabase_url else ""
            supabase_result = deploy_supabase(supabase_key, project_ref)
            results["database"] = supabase_result

        # 2. Deploy frontend (Vercel)
        vercel_token = os.environ.get("VERCEL_TOKEN")
        if vercel_token:
            vercel_result = deploy_vercel(vercel_token)
            results["frontend"] = vercel_result

        # 3. Configurar pagamentos (Stripe)
        stripe_secret = os.environ.get("STRIPE_SECRET_KEY")
        if stripe_secret:
            stripe.api_key = stripe_secret
            account = stripe.Account.retrieve()
            results["payments"] = {
                "success": True,
                "output": f"Stripe configurado para {account.get('email', 'conta verificada')}"
            }

        # Verificar se pelo menos um deploy foi bem-sucedido
        successful = any(result.get("success", False) for result in results.values())

        if successful:
            return jsonify({
                "message": "Deploy completo finalizado!",
                "results": results
            }), 200
        else:
            return jsonify({
                "error": "Nenhum deploy foi bem-sucedido",
                "results": results
            }), 500

    except Exception as e:
        return jsonify({"error": f"Erro no deploy completo: {str(e)}"}), 500

@app.route('/api/deploy/get_credentials_status', methods=['GET'])
def get_credentials_status():
    """Retorna o status das credenciais configuradas"""
    status = {}

    # Vercel
    if os.environ.get("VERCEL_TOKEN"):
        status["vercel"] = "configured"
    else:
        status["vercel"] = "not_configured"

    # Supabase
    if os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_SERVICE_ROLE_KEY"):
        status["supabase"] = "configured"
    else:
        status["supabase"] = "not_configured"

    # Stripe
    if os.environ.get("STRIPE_SECRET_KEY"):
        status["stripe"] = "configured"
    else:
        status["stripe"] = "not_configured"

    return jsonify({"status": status}), 200

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
        print(f"[ERRO DOWNLOAD] Falha ao liberar download para {user_id}: {e}")
        return jsonify({"error": f"Ocorreu um erro ao processar o download: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
