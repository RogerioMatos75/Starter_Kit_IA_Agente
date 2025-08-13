
import json
import os
import re
import unicodedata

def normalize_string(s):
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return s.lower()

def parse_prompts(file_path, system_type, stage_name):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return None, None

    normalized_system_type = normalize_string(system_type)
    normalized_stage_name = normalize_string(stage_name)

    system_type_pattern = re.compile(r"""###\s*(.*?)\s*""", re.IGNORECASE)
    stage_pattern = re.compile(r"""^\d+\.\s*(.*?)$""", re.IGNORECASE | re.MULTILINE)
    
    system_sections = system_type_pattern.split(content)
    
    found_system_content = ""
    for i in range(1, len(system_sections), 2):
        header = system_sections[i]
        if normalized_system_type in normalize_string(header):
            found_system_content = system_sections[i+1]
            break

    if not found_system_content:
        return None, None

    stage_sections = stage_pattern.split(found_system_content)
    
    found_stage_content = ""
    for i in range(1, len(stage_sections), 2):
        header = stage_sections[i]
        if normalized_stage_name in normalize_string(header):
            found_stage_content = stage_sections[i+1]
            break

    if not found_stage_content:
        return None, None

    positive_prompt_match = re.search(r"""Prompt Positivo:\s*(.*?)(?:Prompt Negativo:|$)s*""", found_stage_content, re.DOTALL | re.IGNORECASE)
    negative_prompt_match = re.search(r"""Prompt Negativo:\s*(.*?)$""", found_stage_content, re.DOTALL | re.IGNORECASE)

    positive_prompt = positive_prompt_match.group(1).strip() if positive_prompt_match else None
    negative_prompt = negative_prompt_match.group(1).strip() if negative_prompt_match else None

    return positive_prompt, negative_prompt

def create_project_json(project_name, system_type, project_root_path):
    project_path = os.path.join(project_root_path, 'projetos', project_name)
    output_path = os.path.join(project_path, 'output')
    artefatos_path = os.path.join(project_path, 'artefatos')
    prompts_file_path = os.path.join(project_root_path, 'docs', 'Estrutura de Prompts.md')

    if not os.path.exists(output_path):
        print(f"Error: Directory not found at {output_path}")
        return

    output_files = sorted([f for f in os.listdir(output_path) if f.endswith('.md')])

    timeline = [
        "Análise de requisitos",
        "Prototipação",
        "Arquitetura de software",
        "Desenvolvimento backend",
        "Desenvolvimento frontend",
        "Testes e validação",
        "Deploy",
        "Monitoramento e melhoria contínua"
    ]

    project_data = {
        "projectName": project_name,
        "systemType": system_type,
        "stages": {}
    }

    for i, stage_name in enumerate(timeline):
        if i < len(output_files):
            input_file = f"output/{output_files[i]}"
            
            # Normalize stage name for artifact file
            normalized_stage_name = stage_name.lower().replace(' ', '_').replace('ç', 'c').replace('ã', 'a')
            artifact_filename = f"{str(i+1).zfill(2)}_{normalized_stage_name}.md"
            artifact_path = f"artefatos/{artifact_filename}"

            positive_prompt, negative_prompt = parse_prompts(prompts_file_path, system_type, stage_name)

            project_data["stages"][stage_name] = {
                "status": "pending",
                "input_file": input_file,
                "prompts": {
                    "positive": positive_prompt or "",
                    "negative": negative_prompt or ""
                },
                "artifact_path": artifact_path,
                "artifact_content": ""
            }

    project_json_path = os.path.join(project_path, 'projeto.json')
    with open(project_json_path, 'w', encoding='utf-8') as f:
        json.dump(project_data, f, indent=2, ensure_ascii=False)

    print(f"'projeto.json' created successfully at {project_json_path}")

if __name__ == '__main__':
    # Example usage:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    create_project_json('ncf-indicacao-seguros', 'SaaS', project_root)
