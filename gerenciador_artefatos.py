import os
from datetime import datetime

def _sanitizar_nome(nome):
    """Remove caracteres inválidos para nomes de arquivo/diretório."""
    return "".join(c for c in nome if c.isalnum() or c in (" ", "_", "-")).rstrip()

def gerar_readme_projeto(project_name, etapa_nome, generated_file_name):
    """
    Gera o conteúdo do README.md para a pasta do projeto,
    com base na etapa atual e no conteúdo gerado pela IA.
    """
    readme_content = f"""# Projeto: {project_name}

Bem-vindo ao seu projeto, gerado pelo **Archon AI**!

Este diretório (`projetos/{project_name}/`) contém os artefatos gerados pela IA.

## Status Atual: Etapa "{etapa_nome}"

O artefato mais recente gerado para esta etapa é: **`{generated_file_name}`**.

## Próximos Passos (para o Desenvolvedor):

### 1. Revisar os Artefatos Gerados:
*   **`{generated_file_name}`**: Analise o conteúdo gerado pela IA. Este é o ponto de partida para a sua implementação ou para a sua compreensão do projeto.
*   **Documentos Conceituais**: Consulte os arquivos `.md` na pasta `output/` (na raiz do Starter Kit) para entender o contexto completo do projeto (plano de base, arquitetura, regras de negócio, etc.).

### 2. Implementação e Refinamento:
*   Use os artefatos gerados como base para desenvolver o código real, refinar a lógica ou planejar a próxima fase.
"""
    return readme_content

def gerar_gemini_md(project_name, etapa_nome, generated_file_name, previous_artifact_name=None):
    """
    Gera o conteúdo do Gemini.md para guiar o agente de IA.
    """
    revision_note = ""
    if previous_artifact_name:
        revision_note = f"""
### ⚠️ ATENÇÃO: ARTEFATO REVISADO

O artefato original para esta etapa era `{previous_artifact_name}`. Ele foi revisado e substituído pelo novo artefato abaixo. **Desconsidere o artefato anterior e use o novo como base.**
"""

    gemini_content = f"""# Roteiro de Execução para o Agente Gemini

## Projeto: {project_name}
## Etapa Atual: {etapa_nome}
{revision_note}

### Missão do Agente

Sua missão é continuar o desenvolvimento deste projeto com base nos artefatos gerados pelo Archon AI.

### Instruções Imediatas:

1.  **Analise o Artefato Principal:**
    *   O artefato gerado para esta etapa é: **`{generated_file_name}`**.
    *   Leia e compreenda completamente o conteúdo deste arquivo. Ele contém a especificação ou o código que você deve usar como base.

2.  **Execute as Ações Necessárias:**
    *   Com base na análise, crie ou modifique os arquivos do projeto.
    *   Se for um arquivo de requisitos, comece a estruturar o código.
    *   Se for um código, integre-o ao projeto existente.
    *   Se for um documento de arquitetura, crie os diretórios e arquivos iniciais.

3.  **Verificação e Validação:**
    *   Certifique-se de que o código está limpo e segue as boas práticas.
    *   Se aplicável, execute testes para validar a implementação.

4.  **Reporte o Progresso:**
    *   Ao concluir, descreva as ações que você tomou.
    *   Aguarde a próxima instrução ou a aprovação para avançar para a próxima etapa.

---
*Este roteiro foi gerado automaticamente pelo Archon AI. Siga as instruções para garantir a continuidade e o sucesso do projeto.*
"""
    return gemini_content

def salvar_artefatos_projeto(project_name, etapa_atual, codigo_gerado):
    """
    Salva o artefato principal, o README.md e o Gemini.md na pasta do projeto.
    Retorna o caminho do arquivo principal gerado.
    """
    sanitized_project_name = _sanitizar_nome(project_name)
    if not sanitized_project_name:
        sanitized_project_name = "projeto_sem_nome"

    projetos_dir = os.path.join("projetos", sanitized_project_name)
    os.makedirs(projetos_dir, exist_ok=True)

    generated_file_name = etapa_atual.get('artefato_gerado')
    if not generated_file_name:
        generated_file_name = f"{etapa_atual['nome'].replace(' ', '_').lower()}.txt"

    arquivo_gerado_path = os.path.join(projetos_dir, generated_file_name)

    with open(arquivo_gerado_path, "w", encoding="utf-8") as f:
        f.write(codigo_gerado)
    print(f"[INFO] Artefato salvo em: {arquivo_gerado_path}")

    readme_path = os.path.join(projetos_dir, "README.md")
    readme_content = gerar_readme_projeto(project_name, etapa_atual['nome'], generated_file_name)
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"[INFO] README.md atualizado em: {readme_path}")

    gemini_path = os.path.join(projetos_dir, "Gemini.md")
    gemini_content = gerar_gemini_md(project_name, etapa_atual['nome'], generated_file_name)
    with open(gemini_path, "w", encoding="utf-8") as f:
        f.write(gemini_content)
    print(f"[INFO] Gemini.md atualizado em: {gemini_path}")

    return arquivo_gerado_path
