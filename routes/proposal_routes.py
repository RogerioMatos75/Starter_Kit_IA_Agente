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
// PROMPT-ID: SAAS-PROPOSAL-PARAM-EXTRACTION-V2
// TASK: Extrair e estruturar os componentes fundamentais de uma descrição de projeto de software, focando em entidades, personas e casos de uso.
// CONTEXT: O usuário forneceu uma descrição em linguagem natural de um projeto de software. A sua tarefa é decompor essa descrição nos elementos-chave que definirão a arquitetura e a funcionalidade do sistema.
// INPUT-DESCRIPTION: {description}
// CONSTRAINTS: Analise o texto para identificar os principais 'atores' (userPersonas), os 'objetos' ou 'conceitos' centrais (coreEntities), e as 'ações' ou 'funcionalidades' principais (mainUseCases). Seja conciso e preciso. Se uma informação não for clara, deduza com base no contexto.
// OUTPUT-FORMAT: JSON com o schema: {{"projectName": "string", "mainObjective": "string", "userPersonas": [{{"personaName": "string", "description": "string"}}], "coreEntities": [{{"entityName": "string", "description": "string"}}], "mainUseCases": [{{"useCase": "string", "description": "string"}}], "technicalConstraints": ["string"], "integrations": ["string"]}}
// PROMPT: Analise o INPUT-DESCRIPTION e extraia as informações para preencher o OUTPUT-FORMAT. Retorne ESTRITAMENTE o JSON.
"""
        parametros_extraidos_json = executar_prompt_ia(prompt_interpretacao, is_json_output=True)
        print(f"DEBUG: Raw AI response for param extraction: {parametros_extraidos_json}")
        parametros_extraidos = json.loads(parametros_extraidos_json)
        print(f"DEBUG: Parsed AI response for param extraction: {parametros_extraidos}")

        # Extrai os novos parâmetros estruturados
        project_name = parametros_extraidos.get('projectName', 'Nome não definido')
        main_objective = parametros_extraidos.get('mainObjective', '')
        user_personas = parametros_extraidos.get('userPersonas', [])
        core_entities = parametros_extraidos.get('coreEntities', [])
        main_use_cases = parametros_extraidos.get('mainUseCases', [])
        technical_constraints = parametros_extraidos.get('technicalConstraints', [])

        # Constrói uma descrição de contexto rica para os próximos prompts
        context_description = f"""
O projeto '{project_name}' tem como objetivo principal: {main_objective}.
Ele será utilizado por: {', '.join([p['personaName'] for p in user_personas])}.
As entidades centrais do sistema são: {', '.join([e['entityName'] for e in core_entities])}.
Os principais casos de uso incluem: {', '.join([u['useCase'] for u in main_use_cases])}.
Restrições técnicas a serem consideradas: {', '.join(technical_constraints)}.
"""

        pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs', 'Custo Desenvolvedor FullStack Brasil.pdf')
        market_research_context = extract_text_from_file(pdf_path)
        if not market_research_context:
            print("[AVISO] O arquivo de pesquisa de mercado PDF não foi encontrado ou está vazio.")

        prompt_custos = f"""
// PROMPT-ID: SAAS-ESTIMATE-COSTS-V2
// TASK: Gerar uma estimativa de custos e escopo para um projeto de software SaaS com base em uma análise estruturada.
// CONTEXT: A IA já analisou a descrição inicial e extraiu os componentes-chave do projeto. Agora, com base nesses dados estruturados e em informações de mercado sobre custos de desenvolvimento, sua tarefa é criar uma estimativa de equipe, prazo e custo.
// CONTEXT-DESCRIPTION: {context_description}
// CONSTRAINTS: Baseie a complexidade (e, portanto, o custo e o tempo) no número e na natureza das personas, entidades e casos de uso. Proponha uma equipe realista para o escopo.
// OUTPUT-FORMAT: JSON com o schema: {{"projectName": "string", "coreFeatures": ["string"], "suggestedTeam": "string", "estimatedTimelineMonths": "number", "estimatedMonthlyTeamCost": "number"}}
// PROMPT: Analise o CONTEXT-DESCRIPTION e o CONTEXT-MARKET-RESEARCH para gerar uma estimativa de custos e escopo para o projeto. O campo 'coreFeatures' deve ser uma lista dos 'mainUseCases' extraídos. O 'projectName' deve ser o mesmo extraído anteriormente. Forneça a resposta ESTRITAMENTE no formato JSON.
"""
        dados_custos_json = executar_prompt_ia(prompt_custos, is_json_output=True)
        dados_custos = json.loads(dados_custos_json)

        prompt_introducao = f"""
// PROMPT-ID: SAAS-PROPOSAL-INTRO-V2
// TASK: Atuar como um consultor de software sênior e escrever uma introdução e visão geral para uma proposta de projeto SaaS, utilizando os dados estruturados extraídos pela IA.
// CONTEXT: A IA já processou a ideia inicial e a transformou em uma estrutura clara com objetivo, personas, entidades e casos de uso. Sua tarefa é usar essa estrutura para redigir um texto de abertura de proposta que seja profissional, claro e convincente.
// CONTEXT-DESCRIPTION: {context_description}
// CONSTRAINTS: Use os dados do CONTEXT-DESCRIPTION para criar um texto coeso. Não invente novas funcionalidades.
// OUTPUT-FORMAT: Texto em Markdown.
// PROMPT: Baseado no CONTEXT-DESCRIPTION, crie um texto com: 1. **Introdução:** Um parágrafo resumindo o entendimento do projeto ({project_name}). 2. **Visão Geral da Solução:** Um parágrafo descrevendo como a solução atenderá aos objetivos, mencionando as personas e entidades. 3. **Fases do Projeto:** Uma lista breve das etapas (ex: Discovery, Design, Desenvolvimento, Testes, Implantação). Use markdown para formatação.
"""
        texto_introducao = executar_prompt_ia(prompt_introducao)

        resultado_final = {
            "dados_orcamento": dados_custos,
            "texto_introducao": texto_introducao,
            "parametros_ia": parametros_extraidos,
            "prompt_param_extraction": prompt_interpretacao # NOVO: Adiciona o texto do prompt
        }

        return jsonify(resultado_final), 200

    except IAExecutionError as e:
        return jsonify({"error": str(e)}), 401
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Erro ao decodificar a resposta JSON da IA: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro inesperado: {e}"}), 500