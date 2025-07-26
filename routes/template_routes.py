import os
import json
from flask import Blueprint, jsonify, send_from_directory

template_bp = Blueprint('template_bp', __name__)

# Diretório base onde os templates e previews estão localizados
TEMPLATES_DIR = os.path.join('templates', 'sites-profissionais')

@template_bp.route('/listar_templates', methods=['GET'])
def listar_templates():
    """Lista os templates JSON e suas imagens de preview correspondentes."""
    try:
        if not os.path.isdir(TEMPLATES_DIR):
            return jsonify({'status': 'erro', 'mensagem': 'Diretório de templates não encontrado.'}), 404

        templates = []
        # Lista todos os arquivos no diretório para evitar múltiplas chamadas ao sistema de arquivos
        all_files = os.listdir(TEMPLATES_DIR)
        json_files = [f for f in all_files if f.endswith('.json')]
        image_files = {os.path.splitext(f)[0].lower(): f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))}

        for filename in json_files:
            base_name = os.path.splitext(filename)[0]
            json_path = os.path.join(TEMPLATES_DIR, filename).replace('\\', '/')
            
            # Busca a imagem correspondente (case-insensitive)
            preview_image_filename = image_files.get(base_name.lower())
            
            if preview_image_filename:
                # Se a imagem existe, cria a URL para servi-la através da rota de preview
                preview_image_url = f'/templates/sites-profissionais/{preview_image_filename}'
            else:
                # Se não houver imagem, usa um placeholder ou retorna null
                # O frontend deve ser capaz de lidar com a ausência da imagem
                preview_image_url = None # Ou um caminho para uma imagem placeholder, ex: '/static/assets/placeholder.png'

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