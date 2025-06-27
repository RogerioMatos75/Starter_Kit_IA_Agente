import os
import json
import io
import zipfile
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from flask_cors import CORS
from fsm_orquestrador import FSMOrquestrador, LOG_PATH
from valida_output import run_validation as validar_base_conhecimento
from ia_executor import executar_prompt_ia
from guia_projeto import OUTPUT_FILES
from dotenv import load_dotenv
load_dotenv()
 
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
CORS(app) # Adiciona suporte a CORS para todas as rotas

fsm_instance = None # Será inicializado após carregar o workflow

@app.route('/')
def index():
    """Serve a página de apresentação (landing.html)."""
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    """Serve o painel de controle principal (dashboard.html)."""
    return render_template('dashboard.html')
    
@app.route('/api/download_templates')
def download_templates():
    """Cria um arquivo .zip com os templates da pasta output e o envia para download."""
    template_dir = "documentos_base"
    if not os.path.exists(template_dir):
        return jsonify({"error": "Diretório de templates 'documentos_base' não encontrado."}), 404

    # Cria um arquivo zip em memória
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename in os.listdir(template_dir):
            if filename.endswith(".md"):
                file_path = os.path.join(template_dir, filename)
                zf.write(file_path, arcname=filename) # arcname garante que não haja estrutura de pastas no zip

    memory_file.seek(0) # Volta ao início do arquivo em memória para a leitura

    print(f"[INFO] Gerando pacote de templates para download.")

    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='templates_archon_ai.zip'
    )


@app.route('/api/status')
def status():
    """Endpoint que fornece o estado atual do projeto."""
    # A primeira execução da etapa agora é acionada pela primeira ação de 'aprovar'.
    return jsonify(fsm_instance.get_status())

@app.route('/api/setup_project', methods=['POST'])
def setup_project():
    """Endpoint para configurar o projeto: salva arquivos conceituais e inicia o FSM."""
    project_name = request.form.get('project_name')
    if not project_name:
        return jsonify({"error": "Nome do projeto é obrigatório"}), 400

    files = request.files.getlist('files')
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    for file in files:
        if file.filename != '':
            # Garante que a extensão seja .md
            filename_base, _ = os.path.splitext(file.filename)
            save_path = os.path.join(output_dir, f"{filename_base}.md")
            file.save(save_path)
            print(f"Arquivo conceitual salvo em: {save_path}")

    # Valida a base de conhecimento APÓS salvar os novos arquivos
    if not validar_base_conhecimento():
        return jsonify({
            "error": "Validação da base de conhecimento falhou. Verifique se todos os arquivos necessários (.md) foram enviados e estão corretos."
        }), 400

    # Configura e inicia o FSM
    new_status = fsm_instance.setup_project(project_name)
    return jsonify(new_status)

@app.route('/api/action', methods=['POST'])
def perform_action():
    """Endpoint que recebe as ações do supervisor (Aprovar, Repetir, etc.)."""
    data = request.json
    action = data.get('action', '').lower()
    observation = data.get('observation', '')
    project_name = data.get('project_name')
    print(f"Ação recebida: {action} para o projeto: {project_name}")
    if observation:
        print(f"Observação: {observation}")
    # Processa a ação e retorna o novo estado do projeto
    new_status = fsm_instance.process_action(action, observation, project_name)
    return jsonify(new_status)

@app.route('/api/check_api_key')
def check_api_key():
    """Verifica se a chave da API do Gemini já está configurada no ambiente."""
    api_key = os.environ.get("GEMINI_API_KEY")
    is_configured = bool(api_key and api_key.strip())
    return jsonify({"is_configured": is_configured})

@app.route('/api/save_api_key', methods=['POST'])
def save_api_key():
    """Salva a chave da API do Gemini no arquivo .env."""
    data = request.json
    api_key = data.get('api_key')

    if not api_key or not api_key.strip():
        return jsonify({"error": "API Key não pode ser vazia."}), 400

    try:
        env_vars = {}
        if os.path.exists('.env'):
            with open('.env', 'r', encoding='utf-8') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        env_vars[key] = value

        env_vars['GEMINI_API_KEY'] = f'"{api_key}"'

        with open('.env', 'w', encoding='utf-8') as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")

        print("[INFO] Chave da API do Gemini salva com sucesso no arquivo .env.")
        return jsonify({"message": "API Key salva com sucesso! Por favor, reinicie o servidor para aplicar as alterações."}), 200
    except Exception as e:
        print(f"[ERRO] Falha ao salvar a API Key: {e}")
        return jsonify({"error": f"Falha ao salvar a chave no arquivo .env: {e}"}), 500

@app.route('/api/consult_ai', methods=['POST'])
def consult_ai():
    """Endpoint para fazer uma consulta à IA para refinar um resultado."""
    data = request.json
    user_query = data.get('query', '')
    context = data.get('context', '')

    if not user_query:
        return jsonify({"error": "A consulta não pode estar vazia."}), 400

    # Monta um prompt mais elaborado para a IA
    prompt_refinamento = (
        "Atue como um assistente de engenharia de software sênior. "
        "Analise o contexto abaixo, que é um resultado gerado por uma IA em uma etapa de um projeto.\n\n"
        "--- CONTEXTO ATUAL ---\n"
        f"{context}\n"
        "--- FIM DO CONTEXTO ---\n\n"
        "Um supervisor humano fez a seguinte solicitação ou pergunta para refinar ou esclarecer este contexto. "
        "Forneça uma resposta útil, que pode ser uma versão melhorada do código, uma explicação ou uma alternativa.\n\n"
        "--- SOLICITAÇÃO DO SUPERVISOR ---\n"
        f"{user_query}\n"
        "--- FIM DA SOLICITAÇÃO ---\n\n"
        "Sua resposta:"
    )
    print(f"[CONSULTA IA] Recebida consulta para refinamento: '{user_query}'")
    resposta_ia = executar_prompt_ia(prompt_refinamento)
    return jsonify({"refined_content": resposta_ia})

@app.route('/api/reset_project', methods=['POST'])
def reset_project():
    """Endpoint para resetar o projeto, limpando logs e arquivos gerados."""
    new_status = fsm_instance.reset_project()
    return jsonify(new_status)

@app.route('/api/logs')
def get_logs():
    """Endpoint que fornece o histórico de logs em formato JSON."""
    logs = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                # Acessa a lista 'execucoes' dentro do dicionário padrão
                logs = data.get('execucoes', [])
            except (json.JSONDecodeError, TypeError):
                pass # Retorna lista vazia se o arquivo estiver malformado ou vazio
    return jsonify(logs)

if __name__ == '__main__':
    # Carrega o workflow do arquivo JSON
    project_states = carregar_workflow()
    if not project_states:
        print("Encerrando a aplicação devido a falha no carregamento do workflow.")
    else:
        fsm_instance = FSMOrquestrador(project_states)

    # ETAPA 0: Validação da Base de Conhecimento antes de iniciar o servidor
    print("-" * 50)
    print("Iniciando servidor web...")
    print("Acesse http://127.0.0.1:5001 no seu navegador.")
    app.run(debug=True, port=5001)
