"""
Módulo para gerenciar a criação e o salvamento de artefatos de projeto,
integrado com o Supabase Storage para persistência na nuvem.
"""

import os
from datetime import datetime
from utils.supabase_client import supabase  # Importa o cliente Supabase inicializado

BUCKET_NAME = "artefatos-projetos"  # Nome do bucket que você criou no Supabase

def _sanitizar_nome(nome):
    """Remove caracteres inválidos e espaços para criar um caminho seguro."""
    # Substitui espaços e outros separadores por hífens
    nome_limpo = re.sub(r'[\s/\\:*?"<>|]', '-', nome)
    # Remove quaisquer caracteres que não sejam alfanuméricos, hífens ou underscores
    return "".join(c for c in nome_limpo if c.isalnum() or c in ("-", "_")).lower()

def gerar_readme_projeto(project_name, etapa_nome, generated_file_name):
    """Gera o conteúdo do README.md para a pasta do projeto."""
    return f"""# Projeto: {project_name}

Gerado pelo **Archon AI**.

## Etapa Atual: "{etapa_nome}"

O artefato mais recente é: **`{generated_file_name}`**.

Use este artefato como base para a próxima fase de desenvolvimento.
"""

def gerar_gemini_md(project_name, etapa_nome, generated_file_name):
    """Gera o conteúdo do Gemini.md para guiar o agente de IA."""
    return f"""# Roteiro para o Agente Gemini

## Projeto: {project_name}
## Etapa: {etapa_nome}

**Analise o artefato `{generated_file_name}` e execute as ações necessárias para avançar o projeto.**
"""

def salvar_artefatos_projeto(project_name, etapa_atual, codigo_gerado):
    """
    Faz o upload do artefato principal, do README.md e do Gemini.md para o Supabase Storage.
    Retorna o caminho do objeto do artefato principal no bucket.
    """
    if not supabase:
        print("[ERRO CRÍTICO] Cliente Supabase não está disponível. O salvamento de artefatos falhou.")
        raise ConnectionError("Não foi possível conectar ao Supabase. Verifique as credenciais e a conexão.")

    sanitized_project_name = _sanitizar_nome(project_name)
    if not sanitized_project_name:
        sanitized_project_name = "projeto-sem-nome"

    # Define o nome do artefato a ser gerado
    generated_file_name = etapa_atual.get('artefato_gerado')
    if not generated_file_name:
        generated_file_name = f"{_sanitizar_nome(etapa_atual['nome'])}.txt"

    # --- Caminhos dos objetos no Supabase Storage ---
    # A estrutura será: nome-do-projeto/nome-do-arquivo.ext
    storage_path_artefato = f"{sanitized_project_name}/{generated_file_name}"
    storage_path_readme = f"{sanitized_project_name}/README.md"
    storage_path_gemini = f"{sanitized_project_name}/Gemini.md"

    try:
        # 1. Upload do artefato principal
        # O conteúdo precisa ser em bytes
        supabase.storage.from_(BUCKET_NAME).upload(
            path=storage_path_artefato,
            file=codigo_gerado.encode('utf-8'),
            file_options={"content-type": "text/plain;charset=utf-8", "upsert": "true"}
        )
        print(f"[SUPABASE] Artefato salvo em: {BUCKET_NAME}/{storage_path_artefato}")

        # 2. Geração e Upload do README.md
        readme_content = gerar_readme_projeto(project_name, etapa_atual['nome'], generated_file_name)
        supabase.storage.from_(BUCKET_NAME).upload(
            path=storage_path_readme,
            file=readme_content.encode('utf-8'),
            file_options={"content-type": "text/markdown;charset=utf-8", "upsert": "true"}
        )
        print(f"[SUPABASE] README.md salvo em: {BUCKET_NAME}/{storage_path_readme}")

        # 3. Geração e Upload do Gemini.md
        gemini_content = gerar_gemini_md(project_name, etapa_atual['nome'], generated_file_name)
        supabase.storage.from_(BUCKET_NAME).upload(
            path=storage_path_gemini,
            file=gemini_content.encode('utf-8'),
            file_options={"content-type": "text/markdown;charset=utf-8", "upsert": "true"}
        )
        print(f"[SUPABASE] Gemini.md salvo em: {BUCKET_NAME}/{storage_path_gemini}")

        # Retorna o caminho do artefato principal no storage para referência
        return storage_path_artefato

    except Exception as e:
        print(f"[ERRO SUPABASE] Falha ao fazer upload do artefato para o bucket '{BUCKET_NAME}'.")
        print(f"Detalhes do erro: {e}")
        # Lança a exceção para que o FSM possa tratá-la adequadamente
        raise