# routes/project_setup_routes.py
from flask import Blueprint, jsonify, request
import os
from fsm_orquestrador import fsm_instance
from ia_executor import executar_prompt_ia
from utils.file_parser import extract_text_from_file, _sanitizar_nome

setup_bp = Blueprint('setup_bp', __name__, url_prefix='/api/setup')

@setup_bp.route("/generate_project_base", methods=["POST"])
def generate_project_base():
    project_description = request.form.get('project_description', '').strip()
    project_name = request.form.get('project_name', '').strip()
    
    if not project_description or not project_name:
        return jsonify({"error": "Nome e descrição do projeto são obrigatórios."}), 400

    sanitized_project_name = _sanitizar_nome(project_name)
    context_files = request.files.getlist('files')
    context_text = []

    # Salvar arquivos de contexto localmente
    project_output_dir = os.path.join("output", sanitized_project_name)
    os.makedirs(project_output_dir, exist_ok=True)

    if context_files:
        for file in context_files:
            if file.filename:
                file_path = os.path.join(project_output_dir, file.filename)
                try:
                    file_content = file.read()
                    with open(file_path, 'wb') as f_out:
                        f_out.write(file_content)
                    
                    extracted_content = extract_text_from_file(file_path)
                    if extracted_content:
                        context_text.append(f'--- Conteúdo de {file.filename} ---\n{extracted_content}\n---')

                except Exception as e:
                    print(f"[ERRO] Falha ao salvar arquivo de contexto localmente: {e}")
                    return jsonify({"error": f"Falha ao salvar arquivo de contexto: {e}"}), 500

    full_context = "\n\n--- DOCUMENTOS DE CONTEXTO ---\n" + "\n".join(context_text) if context_text else ""

    prompt_para_gemini = f"""... (o mesmo prompt gigante para gerar a base de conhecimento) ..."""

    try:
        resposta_ia = executar_prompt_ia(prompt_para_gemini)
        arquivos_gerados = _parse_ia_response(resposta_ia)

        # Salvar arquivos gerados localmente
        for filename, content in arquivos_gerados.items():
            file_path = os.path.join(project_output_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f_out:
                f_out.write(content)
            print(f"[INFO] Arquivo de conhecimento salvo em: {file_path}")

        fsm_instance.setup_project(project_name) # Inicia o FSM
        return jsonify({"message": "Base de conhecimento gerada e salva com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro: {e}"}), 500

def _parse_ia_response(resposta_ia):
    # (Lógica para extrair arquivos da resposta da IA, como antes)
    delimitadores = {
        "---PLANO_BASE_MD_START---": "plano_base.md",
        "---ARQUITETURA_TECNICA_MD_START---": "arquitetura_tecnica.md",
        "---REGRAS_NEGOCIO_MD_START---": "regras_negocio.md",
        "---FLUXOS_USUARIO_MD_START---": "fluxos_usuario.md",
        "---BACKLOG_MVP_MD_START---": "backlog_mvp.md",
        "---AUTENTICACAO_BACKEND_MD_START---": "autenticacao_backend.md",
    }
    arquivos_gerados = {}
    for start_tag, filename in delimitadores.items():
        end_tag = start_tag.replace("_START", "_END")
        start_index = resposta_ia.find(start_tag)
        end_index = resposta_ia.find(end_tag)
        if start_index != -1 and end_index != -1:
            content = resposta_ia[start_index + len(start_tag):end_index].strip()
            arquivos_gerados[filename] = content
    return arquivos_gerados

@setup_bp.route("/validate_knowledge_base", methods=["GET"])
def validate_knowledge_base():
    # Esta rota precisa ser implementada ou adaptada.
    # Por enquanto, retorna um sucesso mockado.
    return jsonify({"all_valid": True})