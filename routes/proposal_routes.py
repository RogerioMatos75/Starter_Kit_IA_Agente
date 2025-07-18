from flask import Blueprint, request, jsonify
import os 
import json 
from ia_executor import executar_prompt_ia, IAExecutionError 
from utils.file_parser import extract_text_from_file 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

proposal_bp = Blueprint('proposal_bp', __name__)

@proposal_bp.route('/api/gerar-estimativa', methods=['POST'])
def gerar_estimativa():
    data = request.json
    description = data.get('description')

    if not description:
        return jsonify({"error": "A descrição do projeto é obrigatória."}), 400

    try:
        prompt_interpretacao = f"""
// PROMPT-ID: SAAS-PROPOSAL-PARAM-EXTRACTION-V1
// TASK: Extrair parâmetros estruturados de uma descrição de projeto em linguagem natural.
// CONTEXT: O usuário forneceu uma descrição livre de um projeto de software SaaS. Sua tarefa é analisar essa descrição e preencher os campos do framework de prompt.
// INPUT-DESCRIPTION: {description}
// CONSTRAINTS: Seja o mais preciso possível. Se uma informação não for explicitamente mencionada, use um valor padrão ou deixe em branco se apropriado. Não invente informações.
// OUTPUT-FORMAT: JSON com o schema: {{"targetVertical": "string", "module": "string", "persona": "string", "contextDescription": "string", "constraints": "string"}}
// PROMPT: Analise o INPUT-DESCRIPTION e extraia as informações para preencher o OUTPUT-FORMAT. Retorne ESTRITAMENTE o JSON.
"""
        parametros_extraidos_json = executar_prompt_ia(prompt_interpretacao, is_json_output=True)
        parametros_extraidos = json.loads(parametros_extraidos_json)

        target_vertical = parametros_extraidos.get('targetVertical', '')
        module = parametros_extraidos.get('module', '')
        persona = parametros_extraidos.get('persona', '')
        context_description = parametros_extraidos.get('contextDescription', description) 
        constraints = parametros_extraidos.get('constraints', '')

        pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs', 'Custo Desenvolvedor FullStack Brasil.pdf')
        market_research_context = extract_text_from_file(pdf_path)
        if not market_research_context:
            print("[AVISO] O arquivo de pesquisa de mercado PDF não foi encontrado ou está vazio.")

        prompt_custos = f"""
// PROMPT-ID: SAAS-ESTIMATE-COSTS-V1
// TARGET-VERTICAL: {target_vertical if target_vertical else 'Não especificado'}
// MODULE: {module if module else 'Não especificado'}
// PERSONA: {persona if persona else 'Não especificado'}
// TASK: Gerar uma estimativa de custos e escopo para um projeto de software SaaS.
// CONTEXT: O usuário forneceu uma descrição detalhada do projeto. Além disso, temos dados de pesquisa de mercado sobre custos de desenvolvimento no Brasil. O objetivo é fornecer uma base para um orçamento.
// CONTEXT-DESCRIPTION: {context_description}
// CONSTRAINTS: {constraints if constraints else 'Nenhum'}
// OUTPUT-FORMAT: JSON com o schema: {{"projectName": "string", "coreFeatures": ["string"], "suggestedTeam": "string", "estimatedTimelineMonths": "number", "estimatedMonthlyTeamCost": "number"}}
// PROMPT: Analise o CONTEXT-DESCRIPTION e o CONTEXT-MARKET-RESEARCH para gerar uma estimativa de custos e escopo para o projeto. Forneça a resposta ESTRITAMENTE no formato JSON, sem formatação markdown, seguindo o OUTPUT-FORMAT especificado.
"""
        dados_custos_json = executar_prompt_ia(prompt_custos, is_json_output=True)
        dados_custos = json.loads(dados_custos_json)

        prompt_introducao = f"""
// PROMPT-ID: SAAS-PROPOSAL-INTRO-V1
// TARGET-VERTICAL: {target_vertical if target_vertical else 'Não especificado'}
// MODULE: {module if module else 'Não especificado'}
// PERSONA: {persona if persona else 'Não especificado'}
// TASK: Atuar como um consultor de software sênior e escrever uma introdução e visão geral para uma proposta de projeto SaaS.
// CONTEXT: O usuário forneceu uma descrição detalhada do projeto. O objetivo é criar um texto profissional que resuma o entendimento do projeto e suas fases.
// CONTEXT-DESCRIPTION: {context_description}
// CONSTRAINTS: {constraints if constraints else 'Nenhum'}
// OUTPUT-FORMAT: Texto em Markdown.
// PROMPT: Baseado no CONTEXT-DESCRIPTION, crie um texto com: 1. **Introdução:** Um parágrafo resumindo o entendimento do projeto. 2. **Fases do Projeto:** Uma lista breve das etapas (ex: Discovery, Design, Desenvolvimento, Testes, Implantação). Use markdown para formatação (títulos com ##, listas com *).
"""
        texto_introducao = executar_prompt_ia(prompt_introducao)

        resultado_final = {
            "dados_orcamento": dados_custos,
            "texto_introducao": texto_introducao,
            "parametros_ia": parametros_extraidos 
        }

        return jsonify(resultado_final), 200

    except IAExecutionError as e:
        return jsonify({"error": str(e)}), 401
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Erro ao decodificar a resposta JSON da IA: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro inesperado: {e}"}), 500