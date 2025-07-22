"""
Módulo para gerenciar a criação e o salvamento de artefatos de projeto,
com suporte para salvamento local e upload opcional para o Supabase Storage.
"""

import os
import json
from utils.file_parser import _sanitizar_nome
from utils.supabase_client import supabase

# --- CONFIGURAÇÃO ---
BUCKET_NAME = "artefatos-projetos"
BASE_PROJECTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "projetos"))

def _carregar_config():
    """Carrega as configurações do builder.config.json."""
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "builder.config.json"))
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"SUPABASE_ENABLED": False}

CONFIG = _carregar_config()
SUPABASE_ENABLED = CONFIG.get("SUPABASE_ENABLED", False)

def _salvar_artefato_localmente(project_name, subfolder, file_name, content):
    """
    Salva um artefato em um arquivo local dentro da estrutura de pastas do projeto.
    """
    sanitized_project_name = _sanitizar_nome(project_name)
    project_dir = os.path.join(BASE_PROJECTS_DIR, sanitized_project_name, subfolder)
    
    try:
        os.makedirs(project_dir, exist_ok=True)
        file_path = os.path.join(project_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[LOCAL] Artefato salvo em: {file_path}")
        return file_path
    except OSError as e:
        print(f"[ERRO LOCAL] Falha ao salvar o artefato '{file_name}' localmente: {e}")
        return None

def gerar_readme_projeto(project_name, etapa_nome, generated_file_name):
    """Gera o conteúdo do README.md para a pasta do projeto."""
    return f"""# Projeto: {project_name}

Gerado pelo **Archon AI**.

## Etapa Atual: "{etapa_nome}"

O artefato mais recente é: **`{generated_file_name}`**.

Use este artefato como base para a próxima fase de desenvolvimento.
"""

def salvar_artefatos_projeto(project_name, etapa_atual, codigo_gerado, roteiro_gemini_md):
    """
    Salva os artefatos do projeto localmente e, se ativado, faz o upload para o Supabase.
    Retorna o caminho local do artefato principal.
    """
    sanitized_project_name = _sanitizar_nome(project_name)
    if not sanitized_project_name:
        sanitized_project_name = "projeto-sem-nome"

    etapa_nome = etapa_atual['nome']
    generated_file_name = etapa_atual.get('artefato_gerado', f"{_sanitizar_nome(etapa_nome)}.txt")
    subfolder = etapa_atual.get('subpasta', 'base_conhecimento')

    # --- 1. Salvamento Local Obrigatório ---
    caminho_local_artefato = _salvar_artefato_localmente(project_name, subfolder, generated_file_name, codigo_gerado)
    
    readme_content = gerar_readme_projeto(project_name, etapa_nome, generated_file_name)
    _salvar_artefato_localmente(project_name, "", "README.md", readme_content)

    # Usa o roteiro dinâmico recebido como argumento
    _salvar_artefato_localmente(project_name, "", "GEMINI.md", roteiro_gemini_md)

    # --- 2. Upload Condicional para o Supabase ---
    if SUPABASE_ENABLED:
        if not supabase:
            print("[AVISO] Upload para Supabase ativado, mas o cliente não está disponível. Pulando upload.")
            return caminho_local_artefato

        print("[SUPABASE] Tentando upload dos artefatos...")
        storage_path_artefato = f"{sanitized_project_name}/{subfolder}/{generated_file_name}"
        storage_path_readme = f"{sanitized_project_name}/README.md"
        storage_path_gemini = f"{sanitized_project_name}/GEMINI.md"

        try:
            supabase.storage.from_(BUCKET_NAME).upload(
                path=storage_path_artefato,
                file=codigo_gerado.encode('utf-8'),
                file_options={"content-type": "text/plain;charset=utf-8", "upsert": "true"}
            )
            supabase.storage.from_(BUCKET_NAME).upload(
                path=storage_path_readme,
                file=readme_content.encode('utf-8'),
                file_options={"content-type": "text/markdown;charset=utf-8", "upsert": "true"}
            )
            supabase.storage.from_(BUCKET_NAME).upload(
                path=storage_path_gemini,
                file=roteiro_gemini_md.encode('utf-8'),
                file_options={"content-type": "text/markdown;charset=utf-8", "upsert": "true"}
            )
            print("[SUPABASE] Todos os artefatos foram salvos com sucesso.")

        except Exception as e:
            print(f"[AVISO SUPABASE] Falha ao fazer upload do artefato para o bucket '{BUCKET_NAME}'. O processo continuará.")
            print(f"Detalhes do erro: {e}")
    else:
        print("[INFO] Upload para Supabase desativado. Artefatos salvos apenas localmente.")

    return caminho_local_artefato