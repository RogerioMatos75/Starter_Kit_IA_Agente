# /routes/agent_routes.py

from flask import Blueprint, request, jsonify
import sys
import os

# Adiciona o diretório raiz ao sys.path para permitir importações de outros módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.agentes.structuring_agent import structure_idea

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
