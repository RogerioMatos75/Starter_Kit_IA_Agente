# Documentação da API REST

Esta documentação detalha todos os endpoints da API REST fornecidos pelo `app.py`. A API é a ponte de comunicação entre o painel de controle do frontend e o orquestrador do backend.

## Endpoints do Core

Estes endpoints gerenciam o fluxo principal do projeto.

---

### Obter Status do Projeto

*   **Endpoint:** `GET /api/status`
*   **Descrição:** Retorna o estado completo e atual da Máquina de Estados Finitos (FSM), incluindo a linha do tempo, o conteúdo de pré-visualização da etapa atual e as ações disponíveis para o supervisor.
*   **Requisição:** N/A
*   **Resposta de Sucesso (200 OK):**
    ```json
    {
      "timeline": [
        {"name": "Coleta de Requisitos", "status": "completed"},
        {"name": "Definição de Arquitetura", "status": "in-progress"},
        {"name": "Regras de Negócio", "status": "pending"}
      ],
      "current_step": {
        "name": "Definição de Arquitetura",
        "preview_content": "Conteúdo gerado pela IA para a etapa de arquitetura...",
        "from_cache": false
      },
      "actions": {
        "can_go_back": true,
        "is_finished": false
      },
      "project_name": "Meu-Projeto-Teste"
    }
    ```

---

### Iniciar um Novo Projeto

*   **Endpoint:** `POST /api/setup_project`
*   **Descrição:** Inicia um novo projeto. Recebe o nome do projeto e os arquivos da base de conhecimento (`.md`), valida-os e executa a primeira etapa do workflow para gerar o preview inicial.
*   **Requisição (multipart/form-data):**
    *   `project_name`: (string) O nome do projeto.
    *   `files`: (file list) Uma lista de arquivos `.md` da base de conhecimento.
*   **Resposta de Sucesso (200 OK):** O mesmo formato do endpoint `GET /api/status`, com o estado inicial do projeto.
*   **Resposta de Erro (400 Bad Request):**
    ```json
    {
      "error": "Nome do projeto é obrigatório"
    }
    ```
    ```json
    {
      "error": "Validação da base de conhecimento falhou..."
    }
    ```

---

### Executar uma Ação do Supervisor

*   **Endpoint:** `POST /api/action`
*   **Descrição:** Processa uma ação do supervisor (aprovar, repetir, voltar, pausar) para a etapa atual.
*   **Requisição (JSON):**
    ```json
    {
      "action": "approve",
      "observation": "O código parece bom, mas adicione mais comentários.",
      "project_name": "Meu-Projeto-Teste"
    }
    ```
*   **Resposta de Sucesso (200 OK):** O novo estado do FSM, no mesmo formato do endpoint `GET /api/status`.

---

### Resetar o Projeto

*   **Endpoint:** `POST /api/reset_project`
*   **Descrição:** Reinicia completamente o estado do sistema, apagando todos os logs, caches e projetos gerados. Retorna o sistema ao seu estado inicial.
*   **Requisição:** N/A
*   **Resposta de Sucesso (200 OK):** O estado inicial do FSM, no mesmo formato do endpoint `GET /api/status`.

---

### Obter Logs de Execução

*   **Endpoint:** `GET /api/logs`
*   **Descrição:** Retorna o histórico completo de execuções, decisões e observações registradas no `diario_execucao.json`.
*   **Requisição:** N/A
*   **Resposta de Sucesso (200 OK):**
    ```json
    [
      {
        "etapa": "Coleta de Requisitos",
        "tarefa": "Coleta de Requisitos",
        "status": "concluída",
        "decisao": "aprovada",
        "data_hora": "2023-10-27T10:00:00.000Z",
        "resposta_agente": "...",
        "observacao": "Tudo certo."
      }
    ]
    ```

## Endpoints de Utilitários e IA

---

### Download dos Templates

*   **Endpoint:** `GET /api/download_templates`
*   **Descrição:** Gera e envia um arquivo `.zip` contendo os arquivos modelo da pasta `documentos_base/`.
*   **Requisição:** N/A
*   **Resposta de Sucesso (200 OK):** Um arquivo `templates_archon_ai.zip` para download.

---

### Consultar a IA para Refinamento

*   **Endpoint:** `POST /api/consult_ai`
*   **Descrição:** Permite que o supervisor envie uma pergunta ou instrução de refinamento para a IA, usando o conteúdo atual do preview como contexto.
*   **Requisição (JSON):**
    ```json
    {
      "query": "Poderia refatorar este código para usar uma classe em vez de funções soltas?",
      "context": "código_gerado_anteriormente..."
    }
    ```
*   **Resposta de Sucesso (200 OK):**
    ```json
    {
      "refined_content": "novo_codigo_refatorado_pela_ia..."
    }
    ```
*   **Resposta de Erro (500 Internal Server Error):**
    ```json
    {
      "error": "Ocorreu um erro ao consultar a IA: ..."
    }
    ```

## Endpoints de Pagamento (Stripe)

---

### Criar Sessão de Checkout

*   **Endpoint:** `POST /create-checkout-session`
*   **Descrição:** Cria uma sessão de pagamento no Stripe para a compra do produto.
*   **Requisição (JSON):** `{"email": "cliente@exemplo.com"}`
*   **Resposta de Sucesso (200 OK):** `{"id": "cs_test_a1B2c3D4..."}` (O ID da sessão de checkout do Stripe).

---

### Webhook do Stripe

*   **Endpoint:** `POST /webhook`
*   **Descrição:** Endpoint para receber notificações (webhooks) do Stripe. É usado para confirmar pagamentos e disparar a lógica de entrega do produto.
*   **Requisição:** Payload enviado pelo Stripe.
*   **Resposta de Sucesso (200 OK):** `{"success": true}`

