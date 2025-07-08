

import json
from unittest.mock import patch, MagicMock
import pytest
from app import app

@pytest.fixture
def client():
    """Cria um cliente de teste para a aplicação Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Mocks para as respostas da IA
mock_dados_custos_json = json.dumps({
    "projectName": "Projeto de Teste",
    "coreFeatures": ["Login", "Dashboard"],
    "suggestedTeam": "1 Dev Pleno, 1 QA",
    "estimatedTimelineMonths": 3,
    "estimatedMonthlyTeamCost": 15000
})
mock_texto_introducao = "## Introdução\nEste é um projeto de teste para demonstrar a funcionalidade."

@patch('app.extract_text_from_file', return_value="Contexto do PDF de custos.")
@patch('app.executar_prompt_ia', side_effect=[mock_dados_custos_json, mock_texto_introducao])
def test_gerar_estimativa_success(mock_executar_ia, mock_extract_text, client):
    """
    Testa o sucesso da rota /api/gerar-estimativa, verificando a estrutura da resposta.
    """
    # Faz a requisição para a API
    response = client.post(
        '/api/gerar-estimativa',
        data=json.dumps({'description': 'Um novo app de tarefas'}),
        content_type='application/json'
    )

    # Verifica o status da resposta
    assert response.status_code == 200
    
    # Verifica o conteúdo da resposta
    data = response.get_json()
    assert 'dados_orcamento' in data
    assert 'texto_introducao' in data
    
    # Verifica a estrutura dos dados do orçamento
    orcamento = data['dados_orcamento']
    assert 'projectName' in orcamento and orcamento['projectName']
    assert 'estimatedMonthlyTeamCost' in orcamento and isinstance(orcamento['estimatedMonthlyTeamCost'], int)
    
    # Verifica o texto de introdução
    assert 'texto_introducao' in data and isinstance(data['texto_introducao'], str) and data['texto_introducao']
    
    # Verifica se a função de extração de texto foi chamada
    mock_extract_text.assert_called_once()
    
    # Verifica se a IA foi chamada duas vezes com os prompts corretos
    assert mock_executar_ia.call_count == 2

def test_gerar_estimativa_no_description(client):
    """
    Testa se a rota /api/gerar-estimativa retorna erro 400 se a descrição não for fornecida.
    """
    response = client.post(
        '/api/gerar-estimativa',
        data=json.dumps({}),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == "A descrição do projeto é obrigatória."


