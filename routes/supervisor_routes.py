# routes/supervisor_routes.py
from flask import Blueprint, jsonify, request, Response, send_file
from fsm_orquestrador import fsm_instance
from ia_executor import executar_prompt_ia, IAExecutionError
from utils.file_parser import extract_text_from_file, _sanitizar_nome
from valida_output import run_validation as validar_base_conhecimento # Importar aqui
import json
import os
import shutil
import tempfile

supervisor_bp = Blueprint('supervisor_bp', __name__, url_prefix='/api/supervisor')

@supervisor_bp.route('/download_and_reset_project', methods=['POST'])
def download_and_reset_project():
    """
    Cria um ZIP do projeto para download, envia ao usuário e, após o envio,
    deleta a pasta original do projeto e reseta o estado da FSM.
    """
    data = request.json
    project_name = data.get('project_name')

    if not project_name:
        return jsonify({"error": "Nome do projeto é obrigatório."}), 400

    temp_dir = None
    sanitized_project_name = _sanitizar_nome(project_name)

    try:
        # Etapa 1: Criar o arquivo ZIP temporário usando a lógica centralizada na FSM
        zip_file_path, temp_dir = fsm_instance.create_temp_archive_for_download(project_name)

        def generate_and_cleanup():
            try:
                # Etapa 2: Enviar o arquivo como um stream
                with open(zip_file_path, 'rb') as f:
                    yield from f
            finally:
                # Etapa 3: Limpar o diretório temporário e resetar a FSM
                print(f"[CLEANUP] Removendo diretório temporário: {temp_dir}")
                shutil.rmtree(temp_dir)
                # Chamar o reset do PROJETO para arquivar, deletar a pasta e limpar o estado.
                print(f"[CLEANUP] Resetando projeto: {project_name}")
                fsm_instance.reset_project(project_name_to_reset=project_name)
                print("[CLEANUP] Limpeza e reset do projeto concluídos.")

        # Envia o arquivo como um stream, e a limpeza ocorre no final
        response = Response(generate_and_cleanup(), mimetype='application/zip')
        response.headers.set('Content-Disposition', 'attachment', filename=f'{sanitized_project_name}.zip')
        return response

    except Exception as e:
        print(f"[ERRO] Falha ao compactar ou enviar o projeto: {e}")
        # Limpar o diretório temporário em caso de erro
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return jsonify({"error": f"Falha ao processar o download do projeto: {e}"}), 500



@supervisor_bp.route("/status", methods=["GET"])
def get_status():
    return jsonify(fsm_instance.get_status())

@supervisor_bp.route("/action", methods=["POST"])
def perform_action():
    data = request.json
    new_status = fsm_instance.process_action(
        action=data.get('action', '').lower(),
        observation=data.get('observation', ''),
        project_name=data.get('project_name'),
        current_preview_content=data.get('current_preview_content')
    )
    return jsonify(new_status)

# Rota de reset foi integrada na 'action' e pode ser removida ou mantida por compatibilidade
@supervisor_bp.route('/reset_project', methods=['POST'])
def reset_project_legacy():
    # Idealmente, o frontend deveria usar a rota '/action' com { "action": "reset" }
    # Mas mantemos isso por enquanto para não quebrar o fluxo antigo.
    data = request.json or {}
    project_name_to_reset = data.get('project_name') # Recebe o nome do projeto explicitamente
    return jsonify(fsm_instance.reset_project(project_name_to_reset=project_name_to_reset))

@supervisor_bp.route('/define_layout', methods=['POST'])
def define_layout():
    data = request.json
    project_name = data.get('project_name')
    layout_spec = data.get('layout_spec')

    if not project_name or not layout_spec:
        return jsonify({"error": "Nome do projeto e especificação de layout são obrigatórios."}), 400

    try:
        fsm_instance.process_layout_definition(project_name, layout_spec)
        return jsonify({"message": "Especificação de layout salva com sucesso!"}), 200
    except Exception as e:
        print(f"[ERRO API] Falha ao processar a definição de layout: {e}")
        return jsonify({"error": str(e)}), 500

@supervisor_bp.route('/consult_ai', methods=['POST'])
def consult_ai():
    data = request.json
    query = data.get('query')
    context = data.get('context')

    if not query:
        return jsonify({"error": "A consulta é obrigatória."}), 400

    try:
        prompt = f"Contexto: {context}\n\nConsulta: {query}\n\nCom base no contexto fornecido, refine a informação ou responda à consulta de forma concisa e útil."
        refined_content = executar_prompt_ia(prompt)
        return jsonify({"refined_content": refined_content}), 200
    except IAExecutionError as e:
        return jsonify({"error": f"Erro ao consultar a IA: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro inesperado: {e}"}), 500

@supervisor_bp.route('/logs', methods=["GET"])
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

@supervisor_bp.route('/gerar-estimativa', methods=['POST'])
def gerar_estimativa():
    data = request.json
    description = data.get('description')

    if not description:
        return jsonify({"error": "A descrição do projeto é obrigatória."}), 400

    try:
        # --- Etapa 1: Geração de dados estruturados com RAG para custos ---
        pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs', 'Custo Desenvolvedor FullStack Brasil.pdf')
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

# --- NOVAS ROTAS ---

@supervisor_bp.route('/save_project_name', methods=['POST'])
def save_project_name():
    data = request.json
    project_name = data.get('project_name')

    if not project_name:
        return jsonify({"error": "Nome do projeto é obrigatório."}), 400

    try:
        fsm_instance.set_project_name(project_name) # Assumindo que FSMOrquestrador tem um método para isso
        return jsonify({"message": f"Nome do projeto '{project_name}' salvo com sucesso!"}), 200
    except Exception as e:
        print(f"[ERRO API] Falha ao salvar nome do projeto: {e}")
        return jsonify({"error": str(e)}), 500

@supervisor_bp.route('/validate_knowledge_base', methods=['POST'])
def validate_knowledge_base():
    data = request.json
    project_name = data.get('project_name')

    if not project_name:
        return jsonify({"error": "Nome do projeto é obrigatório para validação."}), 400

    try:
        # A função validar_base_conhecimento precisa saber onde encontrar os arquivos.
        # Assumindo que ela pode receber o nome do projeto para localizar a pasta.
        is_valid = validar_base_conhecimento(project_name) 
        if is_valid:
            return jsonify({"message": "Base de conhecimento validada com sucesso!"}), 200
        else:
            return jsonify({"error": "Falha na validação da base de conhecimento. Verifique os logs."}), 400
    except Exception as e:
        print(f"[ERRO API] Falha ao validar base de conhecimento: {e}")
        return jsonify({"error": str(e)}), 500

# Rota para listar projetos existentes para o modal de arquivamento
@supervisor_bp.route('/list_projects', methods=['GET'])
def list_projects():
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        projects_path = os.path.join(base_dir, 'projetos')
        
        if not os.path.exists(projects_path):
            return jsonify({'projects': [], 'message': 'Diretório de projetos não encontrado.'})

        project_folders = [
            name for name in os.listdir(projects_path)
            if os.path.isdir(os.path.join(projects_path, name)) and name != 'arquivados'
        ]
        return jsonify({'projects': project_folders})
    except Exception as e:
        print(f"[ERRO API] Falha ao listar projetos: {e}")
        return jsonify({'error': str(e)}), 500
