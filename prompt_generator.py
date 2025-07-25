import os
import re
import json

def _sanitizar_nome(nome):
    """Sanitiza o nome para uso em caminhos de arquivo."""
    return re.sub(r'[^a-zA-Z0-9_.-]', '', nome.replace(' ', '_'))

def parse_prompt_structure(markdown_content):
    """
    Parses the markdown content to extract prompt structures for each system type and stage.
    """
    parsed_data = {}
    current_system_type = None
    current_stage = None
    prompt_type = None # 'positivo' or 'negativo'
    
    lines = markdown_content.split('\n')
    
    for line in lines:
        line = line.strip()

        # Identify System Type
        system_match = re.match(r'### (.*?) – (.*)', line)
        if system_match:
            current_system_type = system_match.group(1).strip()
            parsed_data[current_system_type] = {}
            current_stage = None
            prompt_type = None
            continue

        if current_system_type:
            # Identify Stage
            stage_match = re.match(r'^\d+\. (.*)', line)
            if stage_match:
                current_stage = stage_match.group(1).strip()
                parsed_data[current_system_type][current_stage] = {"positivo": "", "negativo": ""}
                prompt_type = None
                continue

            if current_stage:
                # Identify Prompt Type (Positivo/Negativo)
                if line.startswith('Prompt Positivo:'):
                    prompt_type = 'positivo'
                    # Clear any previous content for this prompt type
                    parsed_data[current_system_type][current_stage][prompt_type] = ""
                    continue
                elif line.startswith('Prompt Negativo:'):
                    prompt_type = 'negativo'
                    # Clear any previous content for this prompt type
                    parsed_data[current_system_type][current_stage][prompt_type] = ""
                    continue
                
                # Append content to the current prompt type
                if prompt_type and line and not line.startswith(('+', '-')):
                    if parsed_data[current_system_type][current_stage][prompt_type]:
                        parsed_data[current_system_type][current_stage][prompt_type] += " " + line
                    else:
                        parsed_data[current_system_type][current_stage][prompt_type] = line
    
    return parsed_data

def save_prompts_to_json(project_name, system_type, parsed_prompts, base_dir):
    """
    Saves the parsed prompts into structured JSON files.
    """
    sanitized_project_name = _sanitizar_nome(project_name)
    sanitized_system_type = _sanitizar_nome(system_type)

    output_dir = os.path.join(base_dir, "projetos", sanitized_project_name, "output", "prompts", sanitized_system_type)
    os.makedirs(output_dir, exist_ok=True)

    if system_type not in parsed_prompts:
        print(f"[ERRO] Tipo de sistema '{system_type}' não encontrado nos prompts parseados.")
        return False

    for stage_name, prompts in parsed_prompts[system_type].items():
        sanitized_stage_name = _sanitizar_nome(stage_name)
        file_path = os.path.join(output_dir, f"{sanitized_stage_name}.json")
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(prompts, f, indent=2, ensure_ascii=False)
            print(f"Prompts para '{stage_name}' ({system_type}) salvos em: {file_path}")
        except IOError as e:
            print(f"[ERRO] Falha ao salvar o arquivo JSON para '{stage_name}': {e}")
            return False
    return True
