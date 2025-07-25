import sys
import os
import shutil
from unittest.mock import patch

# Adiciona o diretório raiz do projeto ao sys.path
# Isso garante que o 'fsm_orquestrador' possa ser importado pelos testes.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
from fsm_orquestrador import FSMOrquestrador, _sanitizar_nome, BASE_DIR

# Mock workflow states (updated to reflect new stages)
MOCK_WORKFLOW_STATES = [
    {"nome": "Análise de requisitos", "artefato_gerado": "analise_requisitos.md"},
    {"nome": "Prototipação", "artefato_gerado": "prototipacao.md"},
    {"nome": "Arquitetura de software", "artefato_gerado": "arquitetura_software.md"},
    {"nome": "Desenvolvimento backend", "artefato_gerado": "backend_code.py"},
    {"nome": "Desenvolvimento frontend", "artefato_gerado": "frontend_code.js"},
    {"nome": "Testes e validação", "artefato_gerado": "test_report.md"},
    {"nome": "Deploy", "artefato_gerado": "deploy_script.sh"},
    {"nome": "Monitoramento e melhoria contínua", "artefato_gerado": "monitoring_plan.md"},
]

# Mock content for the generated prompt JSON files
MOCK_GENERATED_PROMPTS = {
    "SaaS": {
        "Análise de requisitos": {
            "positivo": "Analise os requisitos pensando em multiusuários, escalabilidade horizontal, cobrança recorrente e acesso via browser. Priorize recursos comuns a vários perfis de usuários, com foco em experiência contínua e modularidade.",
            "negativo": "Não assuma uso offline, nem arquitetura monolítica ou instalação local. Evite pensar em personalizações profundas por cliente logo de início."
        },
        "Prototipação": {
            "positivo": "Desenhe telas intuitivas, responsivas e voltadas para autosserviço. Considere fluxo de cadastro, dashboard de controle e configurações do plano.",
            "negativo": "Evite designs complexos, dependentes de treinamento intensivo ou com muitos passos manuais."
        },
        "Arquitetura de software": {
            "positivo": "Use arquitetura baseada em microsserviços ou monolitos desacoplados com APIs REST/GraphQL. Pense em autenticação OAuth2, billing e controle de acesso por tenant.",
            "negativo": "Não use banco de dados local, nem acoplamento direto entre UI e lógica de negócio. Evite autenticação hardcoded."
        },
        "Desenvolvimento backend": {
            "positivo": "Implemente APIs bem definidas, com controle de versão, e prepare endpoints para billing, login, gerenciamento de usuário e uso de recursos.",
            "negativo": "Evite lógica de negócio embarcada no frontend, hardcoding de planos e ausência de logs estruturados."
        },
        "Desenvolvimento frontend": {
            "positivo": "Crie interfaces SPA (Single Page Application) com autenticação segura, design responsivo e integração com APIs assíncronas.",
            "negativo": "Não dependa de renderização server-side exclusiva, nem bloqueie interação por causa de recarga de página."
        },
        "Testes e validação": {
            "positivo": "Automatize testes unitários, integração e testes de carga simulando múltiplos usuários simultâneos.",
            "negativo": "Evite testes manuais únicos ou sem considerar escalabilidade."
        },
        "Deploy": {
            "positivo": "Use CI/CD com containers e deploy em nuvem escalável (ex: AWS, GCP, Azure).",
            "negativo": "Não faça deploy manual ou diretamente em produção sem versionamento."
        },
        "Monitoramento e melhoria contínua": {
            "positivo": "Implemente observabilidade com métricas, tracing e alertas. Escute feedback dos usuários com analytics e feature flags.",
            "negativo": "Não deixe a aplicação sem logs, sem painel de métricas ou sem planos de rollback."
        }
    },
    "MicroSaaS": {
        "Análise de requisitos": {
            "positivo": "Mapeie um problema altamente específico de um nicho. Valide a dor com poucos usuários e foque em funcionalidades essenciais que entreguem valor imediato.",
            "negativo": "Evite pensar grande demais ou tentar cobrir várias personas. Nada de funcionalidades genéricas sem validação."
        },
        "Prototipação": {
            "positivo": "Desenhe um MVP enxuto, com interface mínima viável. Priorize o fluxo principal que resolve o problema central do nicho.",
            "negativo": "Não adicione dashboards completos, perfis avançados ou painéis de admin complexos nesta fase."
        },
        "Arquitetura de software": {
            "positivo": "Implemente uma estrutura monolítica leve com possibilidade de escalar componentes. Use frameworks simples, com backend direto ao ponto.",
            "negativo": "Não use microsserviços desnecessários nem infraestrutura robusta que exija DevOps complexo."
        },
        "Desenvolvimento backend": {
            "positivo": "Foque em entregar uma única feature central com endpoints RESTful, banco simples e lógica clara.",
            "negativo": "Evite estruturação de múltiplos módulos ou lógica genérica para várias soluções."
        },
        "Desenvolvimento frontend": {
            "positivo": "Interface simples, com foco no CTA principal. Priorize acessibilidade e carregamento rápido.",
            "negativo": "Não use bibliotecas visuais pesadas nem múltiplas páginas ou navegação complexa."
        },
        "Testes e validação": {
            "positivo": "Teste manual com usuários reais do nicho. Colete feedback qualitativo e refine iterativamente.",
            "negativo": "Não perca tempo com testes automatizados massivos antes da validação do modelo."
        },
        "Deploy": {
            "positivo": "Use plataformas low-code/no-code ou deploy via serviços como Vercel/Netlify para agilidade.",
            "negativo": "Evite provisionamento de servidores dedicados ou setups pesados como Kubernetes."
        },
        "Monitoramento e melhoria contínua": {
            "positivo": "Acompanhe o uso com ferramentas simples como Google Analytics e Hotjar. Faça melhorias pontuais baseadas em feedback direto.",
            "negativo": "Não implemente pipelines complexas ou planos de versionamento sofisticado nessa fase."
        }
    },
    "PWA": {
        "Análise de requisitos": {
            "positivo": "Identifique funcionalidades offline, sincronização em background e uso em dispositivos móveis com baixa conectividade.",
            "negativo": "Não assuma conectividade constante ou foco exclusivo em desktop."
        },
        "Prototipação": {
            "positivo": "Desenhe interface mobile-first, com ícone instalável, transições suaves e interação sem fricção.",
            "negativo": "Evite páginas pesadas, barras de menu grandes ou navegação que dependa de mouse."
        },
        "Arquitetura de software": {
            "positivo": "Inclua service workers, cache inteligente (Cache API) e fallback offline. Estrutura modular JS/CSS.",
            "negativo": "Não dependa de backend para cada ação. Nada de reloads full-page."
        },
        "Desenvolvimento backend": {
            "positivo": "Forneça APIs REST/GraphQL com suporte para sync incremental e cache controlado.",
            "negativo": "Evite lógica que quebre em uso offline. Não use autenticação que invalide tokens em uso offline."
        },
        "Desenvolvimento frontend": {
            "positivo": "Implemente Service Worker, Manifest JSON, notificações push e experiência fluida mesmo offline.",
            "negativo": "Não dependa de frameworks server-side. Evite excessos de bibliotecas JS."
        },
        "Testes e validação": {
            "positivo": "Simule perda de conexão, testes mobile-first e instalação via browser.",
            "negativo": "Não teste apenas em desktop ou com rede estável."
        },
        "Deploy": {
            "positivo": "Hospede em HTTPS com controle de cache adequado. Prefira CDNs e build otimizado.",
            "negativo": "Não use HTTP puro nem hosting sem suporte a arquivos estáticos modernos."
        },
        "Monitoramento e melhoria contínua": {
            "positivo": "Avalie tempo de carregamento, comportamento offline e eventos de instalação.",
            "negativo": "Evite usar apenas métricas tradicionais de página web."
        }
    },
    "MVP": {
        "Análise de requisitos": {
            "positivo": "Descubra a hipótese principal a ser validada. Reduza o escopo ao mínimo necessário para testar aceitação.",
            "negativo": "Não tente antecipar todas as features. Não busque perfeição agora."
        },
        "Prototipação": {
            "positivo": "Crie fluxos diretos, mockups que validem a funcionalidade base, com clareza e rapidez.",
            "negativo": "Não perca tempo refinando UI ou ajustando componentes estéticos."
        },
        "Arquitetura de software": {
            "positivo": "Use arquitetura flexível, monolítica se necessário. Permita mudanças rápidas.",
            "negativo": "Não gaste tempo em soluções escaláveis demais ou arquitetura para o futuro."
        },
        "Desenvolvimento backend": {
            "positivo": "Foque em endpoints que entreguem valor direto ao usuário. Lógica simples, rápida de ajustar.",
            "negativo": "Evite overengineering ou antecipar necessidades complexas."
        },
        "Desenvolvimento frontend": {
            "positivo": "Interfaces rápidas, que validem o comportamento do usuário com simplicidade.",
            "negativo": "Não priorize pixel-perfection ou responsividade total nesse estágio."
        },
        "Testes e validação": {
            "positivo": "Teste com usuários reais. Colete dados qualitativos e ajuste com base nisso.",
            "negativo": "Não priorize testes automatizados ou cobertura completa de código."
        },
        "Deploy": {
            "positivo": "Use hosting rápido e gratuito, GitHub Pages ou Heroku. CI/CD mínimo viável.",
            "negativo": "Não gaste tempo com infraestrutura robusta ou deploys controlados."
        },
        "Monitoramento e melhoria contínua": {
            "positivo": "Observe uso real, colete feedback e itere. Validação é mais importante que performance.",
            "negativo": "Não confie apenas em métricas. Não ignore feedback direto do usuário."
        }
    },
    "ERP": {
        "Análise de requisitos": {
            "positivo": "Mapeie todos os departamentos, fluxos e integrações necessárias. Envolva usuários-chave desde o início.",
            "negativo": "Não limite o levantamento a uma área só. Evite visão superficial."
        },
        "Prototipação": {
            "positivo": "Modele módulos separados com fluxos bem definidos. Simule interações entre setores.",
            "negativo": "Não crie wireframes genéricos sem considerar a complexidade dos processos internos."
        },
        "Arquitetura de software": {
            "positivo": "Use arquitetura modular ou SOA. Preveja escalabilidade, controle de permissões e auditabilidade.",
            "negativo": "Evite sistemas acoplados, banco único sem particionamento ou ausência de versionamento."
        },
        "Desenvolvimento backend": {
            "positivo": "Estruture os serviços por módulo (financeiro, RH, estoque), com integração via API ou filas de eventos.",
            "negativo": "Não centralize tudo em um único serviço gigante. Evite acoplamento de lógica."
        },
        "Desenvolvimento frontend": {
            "positivo": "Dashboards por setor, com menus hierárquicos, filtros e permissões visuais claras.",
            "negativo": "Não torne a UI genérica, sem diferenciação de perfil de acesso."
        },
        "Testes e validação": {
            "positivo": "Testes por módulo, casos de uso interdepartamentais e carga pesada de dados.",
            "negativo": "Não valide só um setor por vez. Não subestime integrações entre áreas."
        },
        "Deploy": {
            "positivo": "Deploy por fases, com migração controlada. Homologação antes de produção.",
            "negativo": "Não faça big bang deploy nem subestime curva de adoção."
        },
        "Monitoramento e melhoria contínua": {
            "positivo": "Auditoria ativa, logs por módulo, integração com BI e painéis de controle.",
            "negativo": "Não ignore falhas silenciosas ou inconsistências entre módulos."
        }
    }
}

@pytest.fixture
def fsm_instance(tmp_path, mocker):
    # Redirect BASE_DIR to tmp_path for isolated testing
    mocker.patch('fsm_orquestrador.BASE_DIR', str(tmp_path))
    mocker.patch('fsm_orquestrador.LOG_PATH', str(tmp_path / "logs" / "diario_execucao.json"))
    mocker.patch('fsm_orquestrador.CHECKPOINT_PATH', str(tmp_path / "logs" / "proximo_estado.json"))
    mocker.patch('fsm_orquestrador.PROJECT_CONTEXT_PATH', str(tmp_path / "logs" / "project_context.json"))
    mocker.patch('fsm_orquestrador.PROMPT_TEMPLATES_PATH', str(tmp_path / "prompt_templates.json")) # Mock this too if it's loaded

    # Ensure logs directory exists for the FSM to write to
    (tmp_path / "logs").mkdir(exist_ok=True)

    # Mock os.path.exists to simulate existence of generated prompt files
    original_os_path_exists = os.path.exists
    def mock_exists(path):
        if "output" in path and "prompts" in path and path.endswith(".json"):
            # Check if the path corresponds to a mocked prompt
            parts = path.split(os.sep)
            try:
                # Find the index of 'output' and 'prompts'
                output_idx = -1
                prompts_idx = -1
                for i, part in enumerate(parts):
                    if part == "output":
                        output_idx = i
                    if part == "prompts":
                        prompts_idx = i
                
                if output_idx != -1 and prompts_idx != -1 and prompts_idx == output_idx + 1:
                    system_type_idx = prompts_idx + 1
                    stage_name_idx = system_type_idx + 1
                    
                    mock_system_type = parts[system_type_idx]
                    mock_stage_name = parts[stage_name_idx].replace(".json", "")
                    
                    if mock_system_type in MOCK_GENERATED_PROMPTS and \
                       mock_stage_name in MOCK_GENERATED_PROMPTS[mock_system_type]:
                        return True
            except (ValueError, IndexError): # Catch if parts are not as expected
                pass 
        return original_os_path_exists(path)

    mocker.patch('fsm_orquestrador.os.path.exists', side_effect=mock_exists)

    # Mock json.load to return the content of the mocked prompt files
    original_json_load = json.load
    def mock_load(fp):
        if isinstance(fp, str) and "output" in fp and "prompts" in fp and fp.endswith(".json"):
            parts = fp.split(os.sep)
            try:
                output_idx = -1
                prompts_idx = -1
                for i, part in enumerate(parts):
                    if part == "output":
                        output_idx = i
                    if part == "prompts":
                        prompts_idx = i

                if output_idx != -1 and prompts_idx != -1 and prompts_idx == output_idx + 1:
                    system_type_idx = prompts_idx + 1
                    stage_name_idx = system_type_idx + 1
                    mock_system_type = parts[system_type_idx]
                    mock_stage_name = parts[stage_name_idx].replace(".json", "")
                    return MOCK_GENERATED_PROMPTS[mock_system_type][mock_stage_name]
            except (ValueError, IndexError, KeyError): # Catch if parts are not as expected
                pass # Fallback to original if not a mocked prompt path
        # For other JSON loads (like workflow.json or prompt_templates.json if not mocked elsewhere)
        return original_json_load(fp)

    mocker.patch('fsm_orquestrador.json.load', side_effect=mock_load)

    # Mock the IA executor to return predictable results
    mocker.patch('fsm_orquestrador.executar_prompt_ia', return_value="Mocked AI response for the step.")

    # Mock the artifact manager to prevent actual file writes during tests
    mocker.patch('fsm_orquestrador.salvar_artefatos_projeto')

    instance = FSMOrquestrador(MOCK_WORKFLOW_STATES)
    yield instance

    # Cleanup after test (tmp_path handles most of it, but explicit is good)
    shutil.rmtree(tmp_path / "projetos", ignore_errors=True)

def test_initial_state(fsm_instance):
    status = fsm_instance.get_status()
    assert fsm_instance.current_step_index == 0
    assert not fsm_instance.is_finished
    assert status['current_step']['name'] == "Projeto Finalizado" # Initial state before setup_project
    assert "Para começar, preciso de algumas informações essenciais" in status['current_step']['preview_content']
    assert status['project_name'] is None
    assert fsm_instance.system_type is None

def test_setup_project_with_system_type(fsm_instance):
    """Testa a configuração inicial do projeto com o tipo de sistema."""
    project_name = "MeuProjetoTeste"
    system_type = "SaaS"
    initial_preview = "Conteúdo inicial do manifesto."

    fsm_instance.setup_project(project_name, initial_preview_content=initial_preview, system_type=system_type)
    status = fsm_instance.get_status()

    assert fsm_instance.project_name == project_name
    assert fsm_instance.system_type == system_type
    assert status['project_name'] == project_name
    assert status['current_step']['name'] == MOCK_WORKFLOW_STATES[0]['nome'] # First step of the new workflow
    assert status['current_step']['preview_content'] == initial_preview
    assert status['timeline'][0]['status'] == 'in-progress'
    assert status['timeline'][1]['status'] == 'pending'

def test_action_approve_first_step(fsm_instance, mocker):
    """Testa a ação de aprovar a primeira etapa (Gerar Base de Conhecimento)."""
    project_name = "MeuProjetoTeste"
    system_type = "SaaS"
    initial_preview = "Conteúdo inicial do manifesto."

    fsm_instance.setup_project(project_name, initial_preview_content=initial_preview, system_type=system_type)

    # Mock the file write for the manifesto
    mocker.patch('builtins.open', mocker.mock_open())
    mocker.patch('fsm_orquestrador.os.makedirs')

    # Approve the first step
    fsm_instance.process_action("approve", project_name=project_name)
    status = fsm_instance.get_status()

    assert fsm_instance.current_step_index == 1 # Should move to the next step
    assert status['current_step']['name'] == MOCK_WORKFLOW_STATES[1]['nome'] # Should be "Prototipação"
    assert "Manifesto salvo. Agora, valide os itens na Etapa 2." in status['current_step']['preview_content']
    assert status['timeline'][0]['status'] == 'completed'
    assert status['timeline'][1]['status'] == 'in-progress'

    # Verify that the manifesto was "saved" (mocked)
    mock_open().assert_called_once_with(
        os.path.join(str(fsm_instance.BASE_DIR), "projetos", _sanitizar_nome(project_name), "base_conhecimento", "01_base_conhecimento.md"),
        'w', encoding='utf-8'
    )
    mock_open().return_value.write.assert_called_once_with(initial_preview)

def test_action_approve_subsequent_step(fsm_instance, mocker):
    """Testa a ação de aprovar uma etapa subsequente."""
    project_name = "MeuProjetoTeste"
    system_type = "SaaS"
    initial_preview = "Conteúdo inicial do manifesto."

    fsm_instance.setup_project(project_name, initial_preview_content=initial_preview, system_type=system_type)
    
    # Simulate approving the first step to move to the second
    mocker.patch('builtins.open', mocker.mock_open())
    mocker.patch('fsm_orquestrador.os.makedirs')
    fsm_instance.process_action("approve", project_name=project_name) # Moves to "Prototipação"

    # Now, approve the second step ("Prototipação")
    # The _run_current_step mock will provide the AI response
    fsm_instance.process_action("approve", project_name=project_name)
    status = fsm_instance.get_status()

    assert fsm_instance.current_step_index == 2 # Should move to "Arquitetura de software"
    assert status['current_step']['name'] == MOCK_WORKFLOW_STATES[2]['nome']
    assert "Mocked AI response for the step." in status['current_step']['preview_content']
    assert status['timeline'][1]['status'] == 'completed'
    assert status['timeline'][2]['status'] == 'in-progress'

    # Verify that salvar_artefatos_projeto was called
    fsm_orquestrador.salvar_artefatos_projeto.assert_called_once()

def test_action_back(fsm_instance, mocker):
    """Testa a ação de voltar para a etapa anterior."""
    project_name = "MeuProjetoTeste"
    system_type = "SaaS"
    initial_preview = "Conteúdo inicial do manifesto."

    fsm_instance.setup_project(project_name, initial_preview_content=initial_preview, system_type=system_type)
    
    # Advance to step 2 ("Prototipação")
    mocker.patch('builtins.open', mocker.mock_open())
    mocker.patch('fsm_orquestrador.os.makedirs')
    fsm_instance.process_action("approve", project_name=project_name)

    # Advance to step 3 ("Arquitetura de software")
    fsm_instance.process_action("approve", project_name=project_name)

    # Now, go back
    fsm_instance.process_action("back", project_name=project_name)
    status = fsm_instance.get_status()

    assert fsm_instance.current_step_index == 1 # Should be back at "Prototipação"
    assert status['current_step']['name'] == MOCK_WORKFLOW_STATES[1]['nome']
    assert "Mocked AI response for the step." in status['current_step']['preview_content'] # Should re-run the step
    assert status['timeline'][1]['status'] == 'in-progress'
    assert status['timeline'][2]['status'] == 'pending' # Log for step 3 should be invalidated

def test_action_repeat(fsm_instance, mocker):
    """Testa a ação de repetir a etapa atual."""
    project_name = "MeuProjetoTeste"
    system_type = "SaaS"
    initial_preview = "Conteúdo inicial do manifesto."

    fsm_instance.setup_project(project_name, initial_preview_content=initial_preview, system_type=system_type)
    
    # Mock the AI response to change on repeat
    mock_ai_responses = ["AI response 1", "AI response 2"]
    mocker.patch('fsm_orquestrador.executar_prompt_ia', side_effect=mock_ai_responses)

    # Initial run (setup_project calls _run_current_step)
    status_initial = fsm_instance.get_status()
    assert status_initial['current_step']['preview_content'] == "AI response 1"

    # Repeat the step
    fsm_instance.process_action("repeat", project_name=project_name)
    status_repeated = fsm_instance.get_status()

    assert fsm_instance.current_step_index == 0 # Should stay on the same step
    assert status_repeated['current_step']['name'] == MOCK_WORKFLOW_STATES[0]['nome']
    assert status_repeated['current_step']['preview_content'] == "AI response 2" # Should have new content

def test_reset_project(fsm_instance, mocker):
    """Testa se a função de reset limpa o ambiente e o estado do FSM."""
    project_name = "ProjetoParaResetar"
    system_type = "SaaS"
    
    # Simulate project files and logs
    (tmp_path / "projetos" / _sanitizar_nome(project_name) / "base_conhecimento").mkdir(parents=True)
    (tmp_path / "projetos" / _sanitizar_nome(project_name) / "base_conhecimento" / "01_base_conhecimento.md").write_text("Manifesto content")
    
    # Create mock prompt directory and files
    (tmp_path / "projetos" / _sanitizar_nome(project_name) / "output" / "prompts" / _sanitizar_nome(system_type)).mkdir(parents=True)
    for stage_name in MOCK_GENERATED_PROMPTS[system_type]:
        (tmp_path / "projetos" / _sanitizar_nome(project_name) / "output" / "prompts" / _sanitizar_nome(system_type) / f"{_sanitizar_nome(stage_name)}.json").write_text(json.dumps(MOCK_GENERATED_PROMPTS[system_type][stage_name]))

    (tmp_path / "logs" / "diario_execucao.json").write_text(json.dumps({"execucoes": [{"etapa": "Etapa 1", "status": "concluída"}]}))
    (tmp_path / "logs" / "proximo_estado.json").write_text(json.dumps({"ultimo_estado": "Etapa 1"}))
    (tmp_path / "logs" / "project_context.json").write_text(json.dumps({"project_name": project_name, "system_type": system_type}))

    # Mock shutil.move to prevent actual file system moves during test
    mocker.patch('fsm_orquestrador.shutil.move')
    mocker.patch('fsm_orquestrador.os.remove') # Mock os.remove for log files

    fsm_instance.project_name = project_name
    fsm_instance.system_type = system_type
    fsm_instance.current_step_index = 1

    fsm_instance.reset_project(project_name_to_reset=project_name)

    # Verify cleanup
    fsm_orquestrador.shutil.move.assert_called_once()
    fsm_orquestrador.os.remove.assert_any_call(str(tmp_path / "logs" / "diario_execucao.json"))
    fsm_orquestrador.os.remove.assert_any_call(str(tmp_path / "logs" / "proximo_estado.json"))
    fsm_orquestrador.os.remove.assert_any_call(str(tmp_path / "logs" / "project_context.json"))

    # Verify FSM state reset
    status = fsm_instance.get_status()
    assert status['project_name'] is None
    assert fsm_instance.system_type is None
    assert fsm_instance.current_step_index == 0
    assert not fsm_instance.is_finished
    assert "Para começar, preciso de algumas informações essenciais" in status['current_step']['preview_content']
