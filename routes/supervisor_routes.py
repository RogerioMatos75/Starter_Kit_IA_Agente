# routes/supervisor_routes.py
from flask import Blueprint, jsonify, request, Response, send_file, send_from_directory
from fsm_orquestrador import fsm_instance
from ia_executor import executar_prompt_ia, IAExecutionError
from utils.file_parser import extract_text_from_file, _sanitizar_nome
from valida_output import run_validation as validar_base_conhecimento # Importar aqui
import json
import os
import shutil
import tempfile

supervisor_bp = Blueprint('supervisor_bp', __name__, url_prefix='/api/supervisor')

@supervisor_bp.route('/get_project_path', methods=['POST'])
def get_project_path():
    """Retorna o caminho completo do sistema para o diretório do projeto."""
    data = request.json
    project_name = data.get('project_name')

    if not project_name:
        return jsonify({"error": "Nome do projeto é obrigatório"}), 400

    try:
        # Define o caminho absoluto do projeto
        project_dir = os.path.abspath(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "projetos",
            _sanitizar_nome(project_name)
        ))
        
        return jsonify({"project_path": project_dir})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@supervisor_bp.route('/verify_taskmaster', methods=['POST'])
def verify_taskmaster():
    """Verifica se o Taskmaster está inicializado no diretório do projeto."""
    data = request.json
    project_name = data.get('project_name')

    if not project_name:
        return jsonify({"success": False, "error": "Nome do projeto é obrigatório"}), 400

    try:
        # Define o caminho do projeto
        project_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                 "projetos", _sanitizar_nome(project_name))
        
        # Verifica se a pasta do projeto existe
        if not os.path.exists(project_dir):
            return jsonify({
                "success": False,
                "error": "Diretório do projeto não encontrado"
            }), 404

        # Verifica se o diretório .taskmaster existe
        taskmaster_dir = os.path.join(project_dir, '.taskmaster')
        if os.path.exists(taskmaster_dir):
            return jsonify({"success": True, "message": "Ambiente Taskmaster verificado com sucesso"})
        else:
            return jsonify({
                "success": False,
                "error": "Taskmaster não inicializado. Execute 'task-master init' no diretório do projeto"
            })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro ao verificar ambiente Taskmaster: {str(e)}"
        }), 500

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
        system_type=data.get('system_type'),  # <-- A CORREÇÃO ESTÁ AQUI
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
        # Lista de arquivos de manifesto esperados
        manifest_files = [
            "01_base_conhecimento.md",
            "02_arquitetura_tecnica.md",
            "03_regras_negocio.md",
            "04_fluxos_usuario.md",
            "05_backlog_mvp.md",
            "06_autenticacao_backend.md"
        ]

        project_output_path = os.path.join('projetos', _sanitizar_nome(project_name), 'output')
        
        if not os.path.isdir(project_output_path):
            return jsonify({
                "error": "Diretório 'output' do projeto não encontrado.",
                "path_checked": project_output_path
            }), 404

        validation_results = {
            "overall_status": "success",
            "files": []
        }

        all_files_found = True
        for filename in manifest_files:
            file_path = os.path.join(project_output_path, filename)
            if os.path.exists(file_path):
                validation_results["files"].append({
                    "file_name": filename,
                    "status": "found",
                    "message": "Arquivo encontrado."
                })
            else:
                all_files_found = False
                validation_results["files"].append({
                    "file_name": filename,
                    "status": "missing",
                    "message": "Arquivo não encontrado."
                })
        
        if not all_files_found:
            validation_results["overall_status"] = "error"

        return jsonify(validation_results), 200

    except Exception as e:
        print(f"[ERRO API] Falha ao validar a existência dos arquivos de conhecimento: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Ocorreu um erro interno no servidor ao verificar os arquivos.", "details": str(e)}), 500

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


@supervisor_bp.route('/get_step_template/<int:step_number>', methods=['GET'])
def get_step_template(step_number):
    """
    Retorna o template HTML para uma etapa específica.
    """
    # Mapeia o número da etapa para o nome do arquivo de template
    template_map = {
        1: 'step_1.html',
        2: 'step_2.html',
        3: 'step_3.html',
        4: 'step_4.html',
        5: 'step_5.html',
        6: 'step_6.html',
        7: 'step_7.html',
        8: 'step_8.html',
    }
    
    template_name = template_map.get(step_number)
    
    if not template_name:
        return "Template não encontrado para esta etapa.", 404
        
    # Constrói o caminho para a pasta de templates
    template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates', 'steps')
    
    return send_from_directory(template_folder, template_name)

@supervisor_bp.route('/generate_ui_artifact', methods=['POST'])
def generate_ui_artifact():
    """
    Recebe o prompt de UI gerado, salva como um novo artefato
    e atualiza o GEMINI.md para a próxima etapa.
    """
    data = request.json
    project_name = data.get('project_name')
    ui_prompt = data.get('ui_prompt')

    if not project_name or not ui_prompt:
        return jsonify({"error": "Nome do projeto e prompt de UI são obrigatórios."}), 400

    try:
        sanitized_project_name = _sanitizar_nome(project_name)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Caminho para o novo artefato de UI
        artifacts_path = os.path.join(base_dir, 'projetos', sanitized_project_name, 'artefatos')
        os.makedirs(artifacts_path, exist_ok=True)
        ui_artifact_path = os.path.join(artifacts_path, '00_ui_definition_prompt.md')

        with open(ui_artifact_path, 'w', encoding='utf-8') as f:
            f.write(ui_prompt)
        
        print(f"[FLUXO] Artefato de UI salvo em: {ui_artifact_path}")

        # Atualizar o GEMINI.md
        gemini_md_path = os.path.join(base_dir, 'projetos', sanitized_project_name, 'GEMINI.md')
        
        gemini_content = fsm_instance._generate_gemini_md('00_ui_definition_prompt.md')

        with open(gemini_md_path, 'w', encoding='utf-8') as f:
            f.write(gemini_content)

        print(f"[FLUXO] GEMINI.md atualizado para a etapa de UI.")

        return jsonify({"message": "Artefato de UI gerado e roteiro atualizado com sucesso!"}), 200

    except Exception as e:
        print(f"[ERRO ROTA] Falha ao gerar artefato de UI: {e}")
        return jsonify({"error": str(e)}), 500