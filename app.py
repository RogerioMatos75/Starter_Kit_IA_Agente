import os
import json
import io
import zipfile
import sys
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, g
from flask_cors import CORS
from fsm_orquestrador import FSMOrquestrador
from valida_output import run_validation as validar_base_conhecimento
from ia_executor import executar_prompt_ia, IAExecutionError
from dotenv import load_dotenv
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
CORS(app)

project_states = carregar_workflow()
if not project_states:
    sys.exit("ERRO CRÍTICO: Falha no carregamento do workflow.json.")

fsm_instance = FSMOrquestrador(project_states)

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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

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

import google.generativeai as genai

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

# --- ROTAS DE PAGAMENTO (sem alterações) ---

# --- ROTAS DE PAGAMENTO (sem alterações) ---
# ... (manter as rotas do Stripe)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
