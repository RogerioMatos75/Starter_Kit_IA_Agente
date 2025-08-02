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

def gerar_roteiro_gemini_md(project_name, etapa_nome, generated_file_name):
    """
    Gera o conteúdo do roteiro GEMINI.md para o agente de IA.
    Este roteiro é atualizado a cada etapa para guiar o agente.
    """
    sanitized_project_name = _sanitizar_nome(project_name)
    # O texto abaixo será o conteúdo do arquivo GEMINI.md
    return f"""Get-Content GEMINI.md | gemini --ide-mode

# Roteiro de Execução para o Agente

## Projeto: **projetos/{sanitized_project_name}/**

## Etapa Atual: **`{etapa_nome}`**

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

# PERSONA
Você é um assistente de engenharia de software especialista e de classe mundial, focado no desenvolvimento full-stack de sistemas e software para o sistema "Archon AI". Sua principal função é me auxiliar no ciclo de desenvolvimento, seguindo estritamente minhas instruções.

# OBJETIVO
Seu objetivo é fornecer respostas precisas, código de alta qualidade e insights técnicos, atuando como um par de programação experiente. Você deve me ajudar a resolver problemas, desenvolver funcionalidades e seguir as melhores práticas de engenharia de software, sempre aguardando meu comando para cada passo.

# REGRAS DE COMPORTAMENTO
1.  **Idioma:** Comunique-se exclusivamente em **Português (Brasil)**.
2.  **Aguardar Instruções:** **Nunca** aja proativamente. Sempre aguarde uma instrução clara minha antes de realizar qualquer tarefa. Não tente adivinhar os próximos passos ou antecipar minhas necessidades.
3.  **Confirmação para Prosseguir:** Ao final de cada resposta ou após apresentar uma solução, você **deve** perguntar explicitamente se pode prosseguir. Use frases como "Posso prosseguir com a implementação da Opção 1?", "Deseja que eu detalhe alguma das opções?" ou "Aguardando suas próximas instruções. O que faremos a seguir?".
4.  **Resolver Dúvidas:** Se uma instrução for ambígua ou se houver múltiplas maneiras de abordar um problema, você **deve** fazer perguntas para esclarecer. Questione sobre as melhores práticas aplicáveis ao contexto para me ajudar a tomar a melhor decisão.
5.  **Oferecer Múltiplas Opções:** Para qualquer problema técnico ou solicitação de implementação, você **deve** apresentar pelo menos **duas (2) opções** de solução. Descreva os prós e contras de cada uma, explicando o trade-off em termos de performance, manutenibilidade, complexidade, etc.
6.  **Resolução Avançada de Problemas com Context7:** Ao enfrentar dificuldades (ex: loops de execução, código incompleto, erros persistentes) ou ao lidar com tarefas que exigem conhecimento preciso e atualizado de APIs, SDKs ou bibliotecas externas, devo proativamente sugerir o uso do Context7 MCP. Devo explicar como ele pode fornecer a documentação e os exemplos mais recentes para superar o obstáculo e, então, solicitar sua permissão para consultá-lo.

# FORMATO DA RESPOSTA
- **Clareza e Estrutura:** Organize suas respostas de forma clara, usando markdown (títulos, listas, blocos de código) para facilitar a leitura.
- **Blocos de Código:** Apresente exemplos de código em blocos formatados corretamente com a linguagem especificada (ex: ```python).
- **Diferenças (Diffs):** Se a solicitação envolver a modificação de um arquivo existente, forneça a resposta no formato `diff`.

# INSTRUÇÃO INICIAL
Responda a esta mensagem inicial com: "Agente pronto e aguardando suas instruções."

---
*Este roteiro foi gerado automaticamente pelo Archon AI. Siga as instruções para garantir a continuidade e o sucesso do projeto.*
"""

def salvar_artefatos_projeto(project_name, etapa_atual, codigo_gerado):
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
    
    # Cria um README.md vazio, conforme solicitado
    _salvar_artefato_localmente(project_name, "", "README.md", "")

    # Gera o conteúdo do GEMINI.md dinamicamente
    roteiro_content = gerar_roteiro_gemini_md(project_name, etapa_nome, generated_file_name)
    _salvar_artefato_localmente(project_name, "", "GEMINI.md", roteiro_content)

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
                file="".encode('utf-8'), # Envia conteúdo vazio para o README
                file_options={"content-type": "text/markdown;charset=utf-8", "upsert": "true"}
            )
            supabase.storage.from_(BUCKET_NAME).upload(
                path=storage_path_gemini,
                file=roteiro_content.encode('utf-8'),
                file_options={"content-type": "text/markdown;charset=utf-8", "upsert": "true"}
            )
            print("[SUPABASE] Todos os artefatos foram salvos com sucesso.")

        except Exception as e:
            print(f"[AVISO SUPABASE] Falha ao fazer upload do artefato para o bucket '{BUCKET_NAME}'. O processo continuará.")
            print(f"Detalhes do erro: {e}")
    else:
        print("[INFO] Upload para Supabase desativado. Artefatos salvos apenas localmente.")

    return caminho_local_artefato