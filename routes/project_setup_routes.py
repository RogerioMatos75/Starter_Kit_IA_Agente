# routes/project_setup_routes.py
from flask import Blueprint, jsonify, request, send_from_directory
import os
from fsm_orquestrador import fsm_instance
from ia_executor import executar_prompt_ia, IAExecutionError
from utils.file_parser import extract_text_from_file, _sanitizar_nome
from prompt_generator import parse_prompt_structure, save_prompts_to_json # NEW: Import prompt generator

setup_bp = Blueprint('setup_bp', __name__, url_prefix='/api/setup')

@setup_bp.route("/generate_project_base", methods=["POST"])
def generate_project_base():
    """
    Etapa 1 do fluxo: Gera o MANIFESTO da Base de Conhecimento.
    Recebe a descrição e os arquivos de contexto, chama a IA para gerar o manifesto,
    mas NÃO SALVA NADA. Apenas passa o resultado como preview para a FSM.
    """
    project_description = request.form.get('project_description', '').strip()
    project_name = request.form.get('project_name', '').strip()
    system_type = request.form.get('system_type', '').strip() # NEW: Get system_type
    
    if not project_description or not project_name or not system_type:
        return jsonify({"error": "Nome, descrição do projeto e tipo de sistema são obrigatórios."}), 400

    context_files = request.files.getlist('files')
    context_text = []

    # Extrai texto de arquivos de contexto, se houver
    if context_files:
        for file in context_files:
            if file.filename:
                try:
                    # Não precisamos salvar o arquivo, apenas ler o conteúdo para o contexto
                    extracted_content = extract_text_from_file(file)
                    if extracted_content:
                        context_text.append(f'--- Início do Documento de Contexto: {file.filename} ---\n{extracted_content}\n--- Fim do Documento de Contexto: {file.filename} ---')
                except Exception as e:
                    print(f"[ERRO] Falha ao processar arquivo de contexto: {e}")
                    return jsonify({"error": f"Falha ao ler o arquivo de contexto: {e}"}), 500

    full_context = "\n\n".join(context_text) if context_text else "Nenhum documento de contexto fornecido."

    # Prompt focado em gerar apenas o manifesto da Base de Conhecimento
    prompt_manifesto = f"""
    **Tarefa:** Você é um Arquiteto de Software Sênior. Sua missão é criar o manifesto inicial (a Base de Conhecimento) para um novo projeto de software.

    **Projeto:** {project_name}
    **Descrição Detalhada:**
    {project_description}

    **Documentos de Contexto Adicionais:**
    {full_context}

    **Instruções:**
    Com base em todas as informações fornecidas, gere um documento único e bem estruturado chamado `01_base_conhecimento.md`.
    Este documento deve conter as seções essenciais para guiar o desenvolvimento, como:
    - **Regras de Negócio (RN):** Liste as regras de negócio fundamentais.
    - **Requisitos Funcionais (RF):** Descreva as principais funcionalidades que o sistema deve ter.
    - **Requisitos Não Funcionais (RNF):** Detalhe os requisitos de performance, segurança, etc.
    - **Personas de Usuário:** Descreva os tipos de usuários que interagirão com o sistema.
    - **Fluxos de Usuário:** Esboce os principais fluxos de interação.

    **Formato de Saída:**
    Gere APENAS o conteúdo de texto em markdown para o arquivo `01_base_conhecimento.md`. Não inclua nenhuma outra explicação, tag ou delimitador.
    """

    try:
        # Executa a IA para gerar o manifesto
        manifesto_content = executar_prompt_ia(prompt_manifesto)

        # NEW: Generate and save structured prompts based on system type
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompt_structure_md_path = os.path.join(base_dir, "docs", "Estrutura de Prompts.md")
        
        with open(prompt_structure_md_path, 'r', encoding='utf-8') as f:
            prompt_structure_content = f.read()
        
        parsed_prompts = parse_prompt_structure(prompt_structure_content)
        save_prompts_to_json(project_name, system_type, parsed_prompts, base_dir)

        # Inicia a FSM com o nome do projeto, o manifesto como o primeiro preview e o tipo de sistema
        fsm_instance.setup_project(project_name, initial_preview_content=manifesto_content, system_type=system_type)
        
        print(f"[FLUXO] Manifesto gerado para '{project_name}'. Aguardando aprovação do usuário.")
        return jsonify({
            "message": "Manifesto da Base de Conhecimento gerado com sucesso! Revise o preview e aprove.",
            "preview_content": manifesto_content
        }), 200

    except IAExecutionError as e:
        print(f"[ERRO ROTA] Erro de execução da IA: {e}")
        return jsonify({"error": f"Ocorreu um erro ao contatar a IA: {e}"}), 500
    except Exception as e:
        print(f"[ERRO ROTA] Ocorreu um erro inesperado: {e}")
        return jsonify({"error": f"Ocorreu um erro inesperado: {e}"}), 500

# Blueprint para rotas de projeto e artefatos
project_bp = Blueprint('project_bp', __name__, url_prefix='/api/project')

@project_bp.route('/<project_name>/artifact/<path:artifact_path>', methods=['GET'])
def get_project_artifact(project_name, artifact_path):
    """Serve um artefato específico de um projeto."""
    try:
        sanitized_name = _sanitizar_nome(project_name)
        # Constrói o caminho absoluto para a pasta 'projetos' na raiz do app
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        projects_root = os.path.join(base_dir, 'projetos')
        project_dir = os.path.join(projects_root, sanitized_name)

        # Segurança: Garante que o caminho do artefato não saia do diretório do projeto
        safe_artifact_path = os.path.normpath(artifact_path).lstrip('./\\ ') # Corrected: \\ instead of \ 
        full_path = os.path.join(project_dir, safe_artifact_path)
        
        if not os.path.abspath(full_path).startswith(os.path.abspath(project_dir)):
            return jsonify({"error": "Acesso negado ao artefato."}), 403

        if not os.path.exists(full_path):
            return jsonify({"error": "Artefato não encontrado."}), 404

        # Envia o arquivo. send_from_directory lida com o mimetype.
        return send_from_directory(os.path.dirname(full_path), os.path.basename(full_path))

    except Exception as e:
        print(f"[ERRO API] Falha ao buscar artefato '{artifact_path}' para o projeto '{project_name}': {e}")
        return jsonify({"error": str(e)}), 500
