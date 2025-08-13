# /routes/agent_routes.py

from flask import Blueprint, request, jsonify
import sys
import os

# Adiciona o diretório raiz ao sys.path para permitir importações de outros módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.agentes.structuring_agent import structure_idea
from modules.agentes.refactoring_agent import refactor_manifest_file # Importa a nova função
from modules.agentes.archon_agent import ArchonAgent

agent_bp = Blueprint('agent_bp', __name__)

@agent_bp.route('/structure-idea', methods=['POST'])
def handle_structure_idea():
    """
    Endpoint da API para receber uma ideia de projeto bruta e retorná-la estruturada.
    """
    data = request.get_json()
    if not data or 'task_description' not in data:
        return jsonify({'error': 'A descrição da tarefa é obrigatória.'}), 400

    raw_idea = data['task_description']
    
    try:
        structured_text = structure_idea(raw_idea)
        return jsonify({'structured_text': structured_text})
    except Exception as e:
        print(f"[API Error] Erro no endpoint /structure-idea: {e}")
        return jsonify({'error': f'Ocorreu um erro interno: {e}'}), 500

@agent_bp.route('/refactor-manifest', methods=['POST'])
def handle_refactor_manifest():
    """
    Endpoint para acionar o agente de refatoração para um arquivo de manifesto específico.
    """
    data = request.get_json()
    project_name = data.get('project_name')
    file_name = data.get('file_name')
    error_reason = data.get('error_reason')

    if not all([project_name, file_name, error_reason]):
        return jsonify({'error': 'project_name, file_name e error_reason são obrigatórios.'}), 400

    try:
        result = refactor_manifest_file(project_name, file_name, error_reason)
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    except Exception as e:
        print(f"[API Error] Erro no endpoint /refactor-manifest: {e}")
        return jsonify({'error': f'Ocorreu um erro interno: {e}'}), 500

@agent_bp.route('/consult-supervisor', methods=['POST'])
def handle_consult_supervisor():
    """
    Endpoint para o supervisor consultar o Archon AI para refinar um artefato.
    """
    data = request.get_json()
    query = data.get('query')
    context = data.get('context')

    if not query or not context:
        return jsonify({'error': 'Query e context são obrigatórios.'}), 400

    try:
        # Obtém a API key a partir da variável de ambiente, seguindo o padrão do projeto
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return jsonify({'error': 'A variável de ambiente GEMINI_API_KEY não está configurada.'}), 500

        # Instancia e usa o agente
        agent = ArchonAgent(api_key=api_key)
        refined_content = agent.consult_supervisor(query, context)
        
        return jsonify({'refined_content': refined_content})

    except Exception as e:
        print(f"[API Error] Erro no endpoint /consult-supervisor: {e}")
        return jsonify({'error': f'Ocorreu um erro interno ao consultar o agente: {str(e)}'}), 500
