# routes/proposal_routes.py

from flask import Blueprint, request, jsonify

# Cria um Blueprint para as rotas de proposta. 
# Blueprints ajudam a organizar as rotas em módulos.
proposal_bp = Blueprint('proposal_bp', __name__)

@proposal_bp.route('/api/gerar-estimativa', methods=['POST'])
def gerar_estimativa():
    """
    Endpoint para gerar uma estimativa de proposta com base em uma descrição.
    Atualmente, retorna dados de exemplo (mock) para desenvolvimento do frontend.
    """
    try:
        # No futuro, aqui entraria a lógica de chamada para a IA
        # data = request.get_json()
        # description = data.get('description')
        # if not description:
        #     return jsonify({"error": "Descrição do projeto é necessária."}), 400
        
        # --- DADOS DE EXEMPLO (MOCK) ---
        mock_data = {
            "dados_orcamento": {
                "projectName": "Plataforma SaaS para Academias",
                "suggestedTeam": "1 Tech Lead, 2 Desenvolvedores Plenos, 1 Designer UX/UI",
                "estimatedTimelineMonths": 4,
                "estimatedMonthlyTeamCost": 45000,
                "coreFeatures": [
                    "Controle de Alunos (Cadastro, Planos, Pagamentos)",
                    "Agendamento de Aulas e Equipamentos",
                    "Faturamento Recorrente (Mensalidades)",
                    "Dashboard Administrativo com Relatórios",
                    "Área do Aluno (Login, Treinos, Horários)"
                ]
            },
            "texto_introducao": "Esta proposta detalha o desenvolvimento de uma plataforma de gestão para academias, projetada para otimizar a administração e melhorar a experiência do cliente.",
            "parametros_ia": {
                "targetVertical": "Fitness e Bem-estar",
                "module": "Gestão Operacional",
                "persona": "Gerentes de Academia",
                "contextDescription": "Desenvolvimento de um sistema de gestão completo para academias de pequeno e médio porte.",
                "constraints": "O sistema deve ser responsivo e funcionar em navegadores modernos."
            }
        }
        
        return jsonify(mock_data)

    except Exception as e:
        print(f"Erro no endpoint /api/gerar-estimativa: {e}")
        return jsonify({"error": "Ocorreu um erro interno no servidor."}), 500
