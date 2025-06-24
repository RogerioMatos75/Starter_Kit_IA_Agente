from flask import Flask, jsonify, render_template, request
import json
import os
# Importar o orquestrador e os dados necessários para definir os estados
from fsm_orquestrador import FSMOrquestrador
from guia_projeto import OUTPUT_FILES
from valida_output import run_validation as validar_base_conhecimento

# Definir os estados do projeto que o orquestrador irá seguir
PROJECT_STATES = [
    {"nome": "Coleta de requisitos", "guia": OUTPUT_FILES[0]},
    {"nome": "Definição de arquitetura", "guia": OUTPUT_FILES[1]},
    {"nome": "Regras de negócio", "guia": OUTPUT_FILES[2]},
    {"nome": "Fluxos de usuário", "guia": OUTPUT_FILES[3]},
    {"nome": "Backlog MVP", "guia": OUTPUT_FILES[4]},
    {"nome": "Implementação do sistema", "guia": None} # A última etapa pode não ter um guia
]

app = Flask(__name__, static_folder='static', template_folder='templates')

# Instância global do orquestrador para manter o estado durante a execução do servidor
fsm_instance = FSMOrquestrador(PROJECT_STATES)

@app.route('/')
def index():
    """Serve a página principal (index.html)."""
    return render_template('index.html')

@app.route('/api/status')
def status():
    """Endpoint que fornece o estado atual do projeto."""
    # Na primeira vez que a UI pede o status, executamos a primeira etapa.
    if fsm_instance.last_preview_content.startswith("O projeto ainda não foi iniciado"):
        fsm_instance._run_current_step()
    return jsonify(fsm_instance.get_status())

@app.route('/api/action', methods=['POST'])
def perform_action():
    """Endpoint que recebe as ações do supervisor (Aprovar, Repetir, etc.)."""
    data = request.json
    action = data.get('action', '').lower()
    observation = data.get('observation', '')
    print(f"Ação recebida: {action}")
    if observation:
        print(f"Observação: {observation}")
    # Processa a ação e retorna o novo estado do projeto
    new_status = fsm_instance.process_action(action, observation)
    return jsonify(new_status)

@app.route('/api/shutdown', methods=['POST'])
def shutdown():
    """Endpoint para encerrar o servidor de desenvolvimento."""
    print("Recebida solicitação para encerrar o servidor...")
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Não está rodando com o servidor de desenvolvimento Werkzeug')
    shutdown_func()
    return 'Servidor encerrando...'

if __name__ == '__main__':
    # ETAPA 0: Validação da Base de Conhecimento antes de iniciar o servidor
    print("--- Iniciando validação da Base de Conhecimento ---")
    if not validar_base_conhecimento():
        print("\n[FALHA] A execução foi interrompida. Corrija os arquivos na pasta 'output/'.")
    else:
        print("-" * 50)
        print("Validação concluída. Iniciando servidor web...")
        print("Acesse http://127.0.0.1:5001 no seu navegador.")
        app.run(debug=True, port=5001)