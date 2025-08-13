import re
import unicodedata

def normalize_string(s):
    """Normaliza uma string removendo acentos e convertendo para minúsculas."""
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return s.lower()

def parse_prompts(file_path, system_type, stage_name):
    """
    Analisa um arquivo de markdown para extrair prompts positivos e negativos.

    Args:
        file_path (str): O caminho para o arquivo de markdown com os prompts.
        system_type (str): O tipo de sistema (ex: 'SaaS') para procurar.
        stage_name (str): O nome da etapa (ex: 'Análise de Requisitos') para procurar.

    Returns:
        tuple: Uma tupla contendo (positive_prompt, negative_prompt). 
               Retorna (None, None) se não encontrar.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"[ERRO no Parser] Arquivo de prompts não encontrado em: {file_path}")
        return None, None

    normalized_system_type = normalize_string(system_type)
    normalized_stage_name = normalize_string(stage_name)

    # Padrão para encontrar seções de tipo de sistema (ex: ### SaaS...)
    system_type_pattern = re.compile(r"""^###\s*(.*?)$""", re.IGNORECASE | re.MULTILINE)
    
    # Padrão para encontrar seções de etapa (ex: 1. Análise de Requisitos)
    stage_pattern = re.compile(r"""^\d+\.\s*(.*?)$""", re.IGNORECASE | re.MULTILINE)
    
    system_sections = system_type_pattern.split(content)
    found_system_content = ""

    # Itera sobre as seções de sistema para encontrar a correta
    for i in range(1, len(system_sections), 2):
        header = system_sections[i]
        if normalized_system_type in normalize_string(header):
            found_system_content = system_sections[i+1]
            break

    if not found_system_content:
        print(f"[AVISO no Parser] Seção para o tipo de sistema '{system_type}' não encontrada.")
        return None, None

    stage_sections = stage_pattern.split(found_system_content)
    found_stage_content = ""

    # Itera sobre as seções de etapa para encontrar a correta
    for i in range(1, len(stage_sections), 2):
        header = stage_sections[i]
        if normalized_stage_name in normalize_string(header):
            found_stage_content = stage_sections[i+1]
            break

    if not found_stage_content:
        print(f"[AVISO no Parser] Etapa '{stage_name}' não encontrada dentro do sistema '{system_type}'.")
        return None, None

    # Extrai os prompts positivo e negativo da seção da etapa encontrada
    positive_prompt_match = re.search(r"""Prompt Positivo:\s*(.*?)(?:Prompt Negativo:|$)s*""", found_stage_content, re.DOTALL | re.IGNORECASE)
    negative_prompt_match = re.search(r"""Prompt Negativo:\s*(.*?)$""", found_stage_content, re.DOTALL | re.IGNORECASE)

    positive_prompt = positive_prompt_match.group(1).strip() if positive_prompt_match else None
    negative_prompt = negative_prompt_match.group(1).strip() if negative_prompt_match else None

    if not positive_prompt or not negative_prompt:
        print(f"[AVISO no Parser] Prompts para a etapa '{stage_name}' não foram totalmente extraídos.")

    return positive_prompt, negative_prompt