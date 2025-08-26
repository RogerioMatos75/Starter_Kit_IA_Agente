import os
import json
from flask import Blueprint, jsonify, send_from_directory, request
import unicodedata
import re

template_bp = Blueprint('template_bp', __name__)

# Diretório base onde os templates e previews estão localizados
TEMPLATES_DIR = os.path.join(os.getcwd(), 'templates', 'sites-profissionais')

def normalize_filename(name):
    # Convert to lowercase
    name = name.lower()
    # Normalize unicode characters (e.g., remove accents)
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')
    # Replace spaces, parentheses, and " by " with hyphens
    name = re.sub(r'[\s()]+|\s+by\s+', '-', name)
    # Remove any remaining non-alphanumeric characters (except hyphens)
    name = re.sub(r'[^a-z0-9-]', '', name)
    # Remove duplicate hyphens
    name = re.sub(r'-+', '-', name)
    # Remove leading/trailing hyphens
    name = name.strip('-')
    return name

@template_bp.route('/listar_templates', methods=['GET'])
def listar_templates():
    """Lista os templates JSON e suas imagens de preview correspondentes."""
    try:
        if not os.path.isdir(TEMPLATES_DIR):
            return jsonify({'status': 'erro', 'mensagem': 'Diretório de templates não encontrado.'}), 404

        templates = []
        all_files = os.listdir(TEMPLATES_DIR)
        json_files = [f for f in all_files if f.endswith('.json')]

        # Create a mapping of normalized image filenames to their original filenames
        image_files_map = {}
        for f in all_files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                normalized_image_name = normalize_filename(os.path.splitext(f)[0])
                image_files_map[normalized_image_name] = f

        for filename in json_files:
            base_name = os.path.splitext(filename)[0]
            json_path = os.path.join(TEMPLATES_DIR, filename).replace('\\', '/')
            
            # Normalize the base_name of the JSON file to match the image file naming convention
            normalized_base_name = normalize_filename(base_name)
            
            # Search for the image using the normalized name
            preview_image_filename = image_files_map.get(normalized_base_name)
            
            if preview_image_filename:
                # Se a imagem existe, cria a URL para servi-la através da rota de preview
                preview_image_url = f'/templates/sites-profissionais/{preview_image_filename}'
            else:
                # Se não houver imagem, usa um placeholder
                preview_image_url = '/static/assets/1logo_Archon.png' # Usando um logo existente como placeholder

            templates.append({
                'name': base_name,
                'json_file': json_path,
                'preview_image': preview_image_url
            })
        
        return jsonify({'status': 'sucesso', 'templates': templates})

    except Exception as e:
        # Log do erro no servidor para depuração
        print(f"[ERRO] em /listar_templates: {e}")
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500

@template_bp.route('/templates/sites-profissionais/<filename>')
def serve_template_preview_image(filename):
    """Serve as imagens de preview diretamente do diretório de templates."""
    return send_from_directory(TEMPLATES_DIR, filename)

@template_bp.route('/gerar_artefato_frontend', methods=['POST'])
def gerar_artefato_frontend():
    """
    Cria um artefato de layout de frontend e enriquece o GEMINI.md com uma
    tarefa de design prioritária, sem alterar a etapa principal.
    """
    try:
        data = request.get_json()
        prompt_usuario = data.get('prompt')

        if not prompt_usuario:
            return jsonify({'status': 'erro', 'mensagem': 'Prompt não fornecido.'}), 400

        # --- 1. Cria o artefato de design ---
        base_dir = os.getcwd()
        artefato_path = os.path.join(base_dir, 'projetos', 'ncf-indicacao-seguros', 'artefatos', 'Frontend_Layout.md')
        
        conteudo_artefato = f"""# Tarefa: Geração de Frontend UI

## Prompt do Usuário
{prompt_usuario}

---
**DIRETRIZ OBRIGATÓRIA:** Para a execução desta tarefa, siga estritamente todas as regras, padrões e workflows definidos no arquivo mestre `.regrasdesign` localizado na raiz do projeto.
"""
        
        with open(artefato_path, 'w', encoding='utf-8') as f:
            f.write(conteudo_artefato)

        # --- 2. Enriquece o GEMINI.md com a nova tarefa ---
        gemini_md_path = os.path.join(base_dir, 'projetos', 'ncf-indicacao-seguros', 'GEMINI.md')
        
        bloco_tarefa = """
---
### 🚨 TAREFA PRIORITÁRIA DE DESIGN 🚨
*   **Analise o Artefato de Design:** `artefatos/Frontend_Layout.md`
*   **Sua Missão:** Execute a tarefa de design descrita no artefato acima. Siga estritamente todas as regras do arquivo `.regrasdesign`. Ao concluir, reporte o resultado e aguarde a aprovação antes de remover este bloco de tarefa.
---
"""

        with open(gemini_md_path, 'r', encoding='utf-8') as f:
            linhas = f.readlines()

        # Encontra o ponto de inserção e adiciona o bloco da tarefa
        ponto_insercao = -1
        target_line_start = "*   Ao concluir, descreva as ações que você tomou e aguarde a próxima instrução."
        for i, linha in enumerate(linhas):
            if linha.strip() == target_line_start:
                ponto_insercao = i + 1
                break
        
        if ponto_insercao != -1:
            linhas.insert(ponto_insercao, bloco_tarefa)
        else:
            # Fallback: if the specific line is not found, insert after "### Instruções Imediatas:"
            for i, linha in enumerate(linhas):
                if linha.strip() == "### Instruções Imediatas:":
                    ponto_insercao = i + 1
                    break
            if ponto_insercao != -1:
                linhas.insert(ponto_insercao, bloco_tarefa)
            else:
                # Final fallback: add at the beginning if no marker is found
                linhas.insert(0, bloco_tarefa)

        with open(gemini_md_path, 'w', encoding='utf-8') as f:
            f.writelines(linhas)

        return jsonify({'status': 'sucesso', 'mensagem': 'Artefato de design gerado e GEMINI.md atualizado com a tarefa prioritária!'})

    except Exception as e:
        print(f"[ERRO] em /gerar_artefato_frontend: {e}")
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500


