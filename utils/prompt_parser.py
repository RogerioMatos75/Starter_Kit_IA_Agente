import re

def parse_prompts_for_system_stage(system_type, stage_name, markdown_content):
    """
    Analisa o conteúdo de um arquivo Markdown para extrair os prompts positivo e negativo
    para um tipo de sistema e uma etapa de desenvolvimento específicos.

    Args:
        system_type (str): O tipo de sistema (ex: 'SaaS', 'MicroSaaS').
        stage_name (str): O nome da etapa (ex: 'Análise de Requisitos').
        markdown_content (str): O conteúdo completo do arquivo Markdown.

    Returns:
        dict: Um dicionário contendo 'positivo' e 'negativo' prompts, ou None se não encontrado.
    """
    try:
        # Regex para encontrar a seção do sistema (ex: ### SaaS - Software as a Service)
        system_header_pattern = re.compile(
            r"^###\s*{}\s*–.*$\n".format(re.escape(system_type)),
            re.IGNORECASE | re.MULTILINE
        )
        system_match = system_header_pattern.search(markdown_content)

        if not system_match:
            print(f"[Parser] Seção para o sistema '{system_type}' não encontrada.")
            return None

        # Limita a busca ao conteúdo após o cabeçalho do sistema encontrado
        content_after_system = markdown_content[system_match.end():]

        # Regex para encontrar a próxima seção de sistema ou o final do arquivo
        next_system_header_pattern = re.compile(r"^###\s+\w+\s*–", re.MULTILINE)
        next_system_match = next_system_header_pattern.search(content_after_system)

        # Isola o bloco de texto pertencente apenas ao sistema atual
        if next_system_match:
            system_block = content_after_system[:next_system_match.start()]
        else:
            system_block = content_after_system

        # Regex para encontrar a seção da etapa dentro do bloco do sistema (ex: 1. Análise de Requisitos)
        stage_header_pattern = re.compile(
            r"^\d+\.\s*{}\s*$\n".format(re.escape(stage_name)),
            re.IGNORECASE | re.MULTILINE
        )
        stage_match = stage_header_pattern.search(system_block)

        if not stage_match:
            print(f"[Parser] Etapa '{stage_name}' não encontrada para o sistema '{system_type}'.")
            return None

        # Limita a busca ao conteúdo após o cabeçalho da etapa
        content_after_stage = system_block[stage_match.end():]

        # Isola o bloco de texto da etapa até a próxima etapa
        next_stage_header_pattern = re.compile(r"^\d+\.\s+\w+\s*$\n", re.MULTILINE)
        next_stage_match = next_stage_header_pattern.search(content_after_stage)

        if next_stage_match:
            stage_block = content_after_stage[:next_stage_match.start()]
        else:
            stage_block = content_after_stage

        # Regex para extrair os prompts positivo e negativo
        prompt_positivo_pattern = re.search(r"Prompt Positivo:\s*\n"(.*?)"\s*\n", stage_block, re.DOTALL)
        prompt_negativo_pattern = re.search(r"Prompt Negativo:\s*\n"(.*?)"\s*\n", stage_block, re.DOTALL)

        prompt_positivo = prompt_positivo_pattern.group(1).strip() if prompt_positivo_pattern else ""
        prompt_negativo = prompt_negativo_pattern.group(1).strip() if prompt_negativo_pattern else ""

        if not prompt_positivo and not prompt_negativo:
            print(f"[Parser] Nenhum prompt encontrado para '{stage_name}' em '{system_type}'.")
            return None

        return {"positivo": prompt_positivo, "negativo": prompt_negativo}

    except Exception as e:
        print(f"[ERRO no Parser] Ocorreu um erro ao analisar os prompts: {e}")
        return None
