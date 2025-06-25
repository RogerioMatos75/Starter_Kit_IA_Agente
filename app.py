from flask import Flask, jsonify, render_template, request
import json
import os
from flask_cors import CORS
# Importar o orquestrador e os dados necessários para definir os estados
from fsm_orquestrador import FSMOrquestrador, LOG_PATH
from guia_projeto import OUTPUT_FILES
from ia_executor import executar_prompt_ia
from valida_output import run_validation as validar_base_conhecimento
 
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
    """Serve a nova página de apresentação (landing.html)."""
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    """Serve o painel de controle principal (dashboard.html)."""
    # Futuramente, esta rota será protegida pelo Clerk.
    # Se o usuário não estiver logado, será redirecionado para a página de login do Clerk.
    return render_template('dashboard.html')
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
                logs = data['execucoes'] if isinstance(data, dict) and 'execucoes' in data else data
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
