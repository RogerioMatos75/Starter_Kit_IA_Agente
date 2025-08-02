# routes/project_setup_routes.py
from flask import Blueprint, jsonify, request, send_from_directory, send_file
import os
import shutil
from fsm_orquestrador import fsm_instance
from ia_executor import executar_prompt_ia, IAExecutionError
from utils.file_parser import extract_text_from_file, _sanitizar_nome

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
    
    if not project_description or not project_name:
        return jsonify({"error": "Nome e descrição do projeto são obrigatórios."}), 400

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

    # Define os documentos a serem gerados e seus prompts específicos
    documents_to_generate = {
        "01_base_conhecimento.md": {
            "prompt": f"""
            **Tarefa:** Você é um Arquiteto de Software Sênior. Sua missão é criar o manifesto inicial (a Base de Conhecimento) para um novo projeto de software.

            **Projeto:** {project_name}
            **Descrição Detalhada:**
            {project_description}

            **Documentos de Contexto Adicionais:**
            {full_context}

            **Instruções:**
            Com base em todas as informações fornecidas, gere APENAS o conteúdo de texto em markdown para o arquivo `01_base_conhecimento.md`.
            O documento deve conter as seguintes seções, utilizando os cabeçalhos Markdown exatos:

            ## Regras de Negócio
            Liste as regras de negócio fundamentais do projeto.

            ## Requisitos Funcionais
            Descreva as principais funcionalidades que o sistema deve ter.

            ## Requisitos Não Funcionais
            Detalhe os requisitos de performance, segurança, usabilidade, etc.

            ## Personas de Usuário
            Descreva os tipos de usuários que interagirão com o sistema.

            ## Fluxos de Usuário
            Esboce os principais fluxos de interação do usuário com o sistema.

            Não inclua nenhuma outra explicação, tag ou delimitador além do conteúdo do documento.
            """
        },
        "02_arquitetura_tecnica.md": {
            "prompt": f"""
            **Tarefa:** Você é um Arquiteto de Software Sênior. Sua missão é criar a arquitetura técnica para o projeto.

            **Projeto:** {project_name}
            **Descrição Detalhada:**
            {project_description}

            **Documentos de Contexto Adicionais:**
            {full_context}

            **Instruções:**
            Com base em todas as informações fornecidas, gere APENAS o conteúdo de texto em markdown para o arquivo `02_arquitetura_tecnica.md`.
            O documento deve conter as seguintes seções, utilizando os cabeçalhos Markdown exatos:

            ## Arquitetura
            Descreva a arquitetura geral (ex: microsserviços, monolito).

            ## Tecnologias
            Liste as tecnologias recomendadas para frontend, backend, banco de dados, etc.

            ## Integrações
            Detalhe as integrações com serviços de terceiros.

            ## Fluxos Principais
            Esboce os fluxos técnicos mais importantes.

            Não inclua nenhuma outra explicação, tag ou delimitador além do conteúdo do documento.
            """
        },
        "03_regras_negocio.md": {
            "prompt": f"""
            **Tarefa:** Você é um Analista de Negócios Sênior. Sua missão é detalhar as regras de negócio para o projeto.

            **Projeto:** {project_name}
            **Descrição Detalhada:**
            {project_description}

            **Documentos de Contexto Adicionais:**
            {full_context}

            **Instruções:**
            Com base em todas as informações fornecidas, gere um documento único e bem estruturado chamado `03_regras_negocio.md`.
            Este documento deve conter as seguintes seções, utilizando os cabeçalhos Markdown exatos:

            ## Regras de Negócio
            Liste as regras de negócio fundamentais.

            ## Restrições
            Detalhe quaisquer restrições conhecidas.

            ## Exceções
            Descreva as exceções e como elas devem ser tratadas.

            ## Decisões
            Registre as decisões importantes tomadas.

            **Formato de Saída:**
            Gere APENAS o conteúdo de texto em markdown para o arquivo `03_regras_negocio.md`. Não inclua nenhuma outra explicação, tag ou delimitador.
            """
        },
        "04_fluxos_usuario.md": {
            "prompt": f"""
            **Tarefa:** Você é um UX Designer Sênior. Sua missão é mapear os fluxos de usuário para o projeto.

            **Projeto:** {project_name}
            **Descrição Detalhada:**
            {project_description}

            **Documentos de Contexto Adicionais:**
            {full_context}

            **Instruções:**
            Com base em todas as informações fornecidas, gere um documento único e bem estruturado chamado `04_fluxos_usuario.md`.
            Este documento deve conter as seguintes seções, utilizando os cabeçalhos Markdown exatos:

            ## Fluxos de Usuário
            Descreva a jornada do usuário em processos chave.

            ## Navegação
            Detalhe a sequência de telas e interações.

            ## Interações
            Especifique as ações do usuário e as respostas do sistema.

            **Formato de Saída:**
            Gere APENAS o conteúdo de texto em markdown para o arquivo `04_fluxos_usuario.md`. Não inclua nenhuma outra explicação, tag ou delimitador.
            """
        },
        "05_backlog_mvp.md": {
            "prompt": f"""
            **Tarefa:** Você é um Product Owner Sênior. Sua missão é criar o backlog inicial do MVP para o projeto.

            **Projeto:** {project_name}
            **Descrição Detalhada:**
            {project_description}

            **Documentos de Contexto Adicionais:**
            {full_context}

            **Instruções:**
            Com base em todas as informações fornecidas, gere um documento único e bem estruturado chamado `05_backlog_mvp.md`.
            Este documento deve conter as seguintes seções, utilizando os cabeçalhos Markdown exatos:

            ## Funcionalidades (Épicos e User Stories)
            Liste as funcionalidades principais.

            ## Critérios de Aceitação
            Defina os critérios de aceitação para as user stories.

            ## Priorização (MoSCoW)
            Priorize as funcionalidades usando o método MoSCoW (Must-Have, Should-Have, Could-Have, Won't-Have).

            **Formato de Saída:**
            Gere APENAS o conteúdo de texto em markdown para o arquivo `05_backlog_mvp.md`. Não inclua nenhuma outra explicação, tag ou delimitador.
            """
        },
        "06_autenticacao_backend.md": {
            "prompt": f"""
            **Tarefa:** Você é um Especialista em Segurança. Sua missão é sugerir um modelo de autenticação backend para o projeto.

            **Projeto:** {project_name}
            **Descrição Detalhada:**
            {project_description}

            **Documentos de Contexto Adicionais:**
            {full_context}

            **Instruções:**
            Com base em todas as informações fornecidas, gere um documento único e bem estruturado chamado `06_autenticacao_backend.md`.
            Este documento deve conter as seguintes seções, utilizando os cabeçalhos Markdown exatos:

            ### Fluxo de Autenticação
            Descreva os passos envolvidos no fluxo de autenticação (ex: login, registro, recuperação de senha).

            ### Tecnologias/Bibliotecas
            Sugira tecnologias e bibliotecas específicas (ex: JWT, OAuth2, Passport.js, etc.).

            ### Considerações de Segurança
            Liste as melhores práticas de segurança a serem consideradas (ex: hashing de senhas, proteção contra CSRF).

            **Formato de Saída:**
            Gere APENAS o conteúdo de texto em markdown para o arquivo `06_autenticacao_backend.md`. Não inclua nenhuma outra explicação, tag ou delimitador.
            """
        }
    }

    generated_files_summary = []
    sanitized_project_name = _sanitizar_nome(project_name)
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "projetos", sanitized_project_name, "output")
    os.makedirs(output_dir, exist_ok=True)

    print(f"[DEBUG] generate_project_base chamada para projeto: {project_name}")
    for filename, doc_info in documents_to_generate.items():
        try:
            print(f"[FLUXO] Gerando {filename}...")
            file_content = executar_prompt_ia(doc_info["prompt"])
            
            if not file_content or file_content.strip() == "":
                print(f"[AVISO] IA retornou conteúdo vazio ou nulo para {filename}.")
                generated_files_summary.append(f"- {filename} (AVISO: Conteúdo vazio da IA)")
                continue # Pula para o próximo arquivo se o conteúdo for vazio

            file_path = os.path.join(output_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            generated_files_summary.append(f"- {filename} (Gerado com sucesso)")
            print(f"[FLUXO] {filename} salvo em: {file_path}")
            print(f"[DEBUG] Conteúdo de {filename} (primeiros 200 chars):\n{file_content[:200]}...")
        except IAExecutionError as e:
            generated_files_summary.append(f"- {filename} (ERRO: {e})")
            print(f"[ERRO ROTA] Erro ao gerar {filename}: {e}")
        except Exception as e:
            generated_files_summary.append(f"- {filename} (ERRO: {e})")
            print(f"[ERRO ROTA] Erro inesperado ao salvar {filename}: {e}")

    final_preview_content = "# Documentos da Base de Conhecimento Gerados:\n\n" + "\n".join(generated_files_summary)

    try:
        # Inicia a FSM com o nome do projeto e o resumo dos arquivos gerados como preview
        fsm_instance.setup_project(project_name, initial_preview_content=final_preview_content)
        
        print(f"[FLUXO] Documentos da Base de Conhecimento gerados para '{project_name}'. Aguardando validação do usuário.")
        return jsonify({
            "message": "Documentos da Base de Conhecimento gerados com sucesso! Revise o preview e aprove.",
            "preview_content": final_preview_content
        }), 200

    except Exception as e:
        print(f"[ERRO ROTA] Ocorreu um erro inesperado ao configurar o projeto na FSM: {e}")
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
        safe_artifact_path = os.path.normpath(artifact_path) 
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

@project_bp.route('/<project_name>/download_zip', methods=['GET'])
def download_project_zip(project_name):
    """Cria um arquivo ZIP do projeto e o envia para download."""
    try:
        sanitized_name = _sanitizar_nome(project_name)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_path = os.path.join(base_dir, 'projetos', sanitized_name)

        if not os.path.exists(project_path):
            return jsonify({"error": "Projeto não encontrado para download."}), 404

        # Cria um arquivo ZIP temporário
        temp_zip_path = os.path.join(base_dir, 'temp', f'{sanitized_name}.zip')
        os.makedirs(os.path.dirname(temp_zip_path), exist_ok=True)
        shutil.make_archive(os.path.splitext(temp_zip_path)[0], 'zip', project_path)

        # Envia o arquivo para download
        return send_file(temp_zip_path, as_attachment=True, download_name=f'{sanitized_name}.zip')

    except Exception as e:
        print(f"[ERRO API] Falha ao gerar ZIP para download do projeto '{project_name}': {e}")
        return jsonify({"error": str(e)}), 500
