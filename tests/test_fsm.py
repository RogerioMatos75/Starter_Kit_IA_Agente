import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
# Isso garante que o 'fsm_orquestrador' possa ser importado pelos testes.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
from fsm_orquestrador import FSMOrquestrador

# Mock do workflow para os testes
MOCK_WORKFLOW_STATES = [
    {"nome": "Etapa 1", "artefato_gerado": "etapa1.txt"},
    {"nome": "Etapa 2", "artefato_gerado": "etapa2.txt"},
]

# Fixture para criar uma instância limpa do FSM para cada teste
@pytest.fixture
def fsm_instance():
    # Garante que o ambiente de teste esteja limpo
    log_path = "logs/diario_execucao.json"
    if os.path.exists(log_path):
        os.remove(log_path)
    
    instance = FSMOrquestrador(MOCK_WORKFLOW_STATES)
    return instance

def test_initial_state(fsm_instance):
    """Testa se o FSM inicia no estado correto."""
    status = fsm_instance.get_status()
    assert fsm_instance.current_step_index == 0
    assert not fsm_instance.is_finished
    assert status['current_step']['name'] == "Projeto Finalizado" # Porque o projeto não foi iniciado
    # Verifica se a nova mensagem de boas-vindas, mais detalhada, está presente.
    assert "Para começar, preciso de algumas informações essenciais" in status['current_step']['preview_content']
    assert status['project_name'] is None

def test_setup_project(fsm_instance):
    """Testa a configuração inicial do projeto."""
    # Mock da função que chama a IA para não precisar de API key
    # A assinatura do mock inclui 'use_cache' para ser consistente com a função real.
    fsm_instance._run_current_step = lambda use_cache=True: setattr(fsm_instance, 'last_preview_content', 'Preview da Etapa 1')

    fsm_instance.setup_project("Projeto Teste")
    status = fsm_instance.get_status()

    assert fsm_instance.project_name == "Projeto Teste"
    assert status['project_name'] == "Projeto Teste"
    assert status['current_step']['name'] == "Etapa 1"
    assert status['current_step']['preview_content'] == "Preview da Etapa 1"
    assert status['timeline'][0]['status'] == 'in-progress'
    assert status['timeline'][1]['status'] == 'pending'

def test_action_approve(fsm_instance):
    """Testa a ação de aprovar uma etapa."""
    # Mock para não chamar a IA
    # A assinatura do mock inclui 'use_cache' para ser consistente com a função real.
    fsm_instance._run_current_step = lambda use_cache=True: setattr(fsm_instance, 'last_preview_content', f"Preview da Etapa {fsm_instance.current_step_index + 1}")

    fsm_instance.setup_project("Projeto Teste")
    
    # Aprova a primeira etapa
    fsm_instance.process_action("approve", project_name="Projeto Teste")
    status = fsm_instance.get_status()

    assert fsm_instance.current_step_index == 1
    assert status['current_step']['name'] == "Etapa 2"
    assert "Preview da Etapa 2" in status['current_step']['preview_content']
    assert status['timeline'][0]['status'] == 'completed'
    assert status['timeline'][1]['status'] == 'in-progress'

def test_action_back(fsm_instance):
    """Testa a ação de voltar para a etapa anterior."""
    # Mock para não chamar a IA
    # A assinatura do mock inclui 'use_cache' para ser consistente com a função real.
    fsm_instance._run_current_step = lambda use_cache=True: setattr(fsm_instance, 'last_preview_content', f"Preview da Etapa {fsm_instance.current_step_index + 1}")

    fsm_instance.setup_project("Projeto Teste")
    
    # Avança para a Etapa 2
    fsm_instance.process_action("approve", project_name="Projeto Teste")
    status_after_approve = fsm_instance.get_status()
    assert status_after_approve['current_step']['name'] == "Etapa 2"
    assert status_after_approve['timeline'][0]['status'] == 'completed'
    assert status_after_approve['timeline'][1]['status'] == 'in-progress'

    # Volta para a Etapa 1
    fsm_instance.process_action("back", project_name="Projeto Teste")
    status_after_back = fsm_instance.get_status()

    assert fsm_instance.current_step_index == 0
    assert status_after_back['current_step']['name'] == "Etapa 1"
    assert "Preview da Etapa 1" in status_after_back['current_step']['preview_content']
    assert status_after_back['timeline'][0]['status'] == 'in-progress' 
    assert status_after_back['timeline'][1]['status'] == 'pending'

def test_action_repeat(fsm_instance):
    """Testa a ação de repetir a etapa atual."""
    # Mock que simula uma nova execução da IA com um resultado diferente
    run_count = 0
    # A assinatura do mock deve corresponder à função real, incluindo o argumento 'use_cache'
    def mock_run(use_cache=True):
        nonlocal run_count
        run_count += 1
        setattr(fsm_instance, 'last_preview_content', f'Preview da Etapa 1 (Execução {run_count})')

    fsm_instance._run_current_step = mock_run
    fsm_instance.setup_project("Projeto Teste")
    status_after_setup = fsm_instance.get_status()
    assert "Execução 1" in status_after_setup['current_step']['preview_content']

    fsm_instance.process_action("repeat", project_name="Projeto Teste")
    status_after_repeat = fsm_instance.get_status()
    assert fsm_instance.current_step_index == 0 # Continua na mesma etapa
    assert "Execução 2" in status_after_repeat['current_step']['preview_content'] # Conteúdo foi atualizado

def test_reset_project(fsm_instance):
    """Testa se a função de reset limpa o ambiente e o estado do FSM."""
    # 1. Simular um ambiente de projeto existente
    project_name = "ProjetoParaDeletar"
    project_dir = os.path.join("projetos", project_name)
    os.makedirs(project_dir, exist_ok=True)
    with open(os.path.join(project_dir, "artefato.txt"), "w", encoding="utf-8") as f:
        f.write("lixo")

    log_path = "logs/diario_execucao.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump({"execucoes": [{"etapa": "Etapa 1", "status": "concluída"}]}, f)

    fsm_instance.project_name = project_name
    fsm_instance.current_step_index = 1

    # 2. Executar a função de reset
    fsm_instance.reset_project()

    # 3. Verificar se o ambiente foi limpo (a pasta 'projetos' é recriada vazia)
    assert not os.path.exists(project_dir)
    assert not os.path.exists(log_path)

    # 4. Verificar se o estado do FSM foi resetado
    status = fsm_instance.get_status()
    assert status['project_name'] is None
    assert fsm_instance.current_step_index == 0
    assert not fsm_instance.is_finished
    # Verifica se a mensagem de boas-vindas foi resetada para o novo padrão.
    assert "Para começar, preciso de algumas informações essenciais" in status['current_step']['preview_content']
