## Arquitetura

Arquitetura de microsserviços para melhor escalabilidade e manutenção.  Um microsserviço para o frontend (PWA), um para o backend (API REST) e outro para o painel administrativo.  Comunicação entre os microsserviços via API REST.

## Tecnologias

* **Frontend:** React com React Router, CSS Modules, e possivelmente uma biblioteca de UI como Material-UI ou similar.  Service Worker para PWA.
* **Backend:** Node.js com Express.js.
* **Banco de Dados:** PostgreSQL.
* **Mensagens:** Firebase Cloud Messaging (FCM).
* **Autenticação:** JWT (JSON Web Tokens).

## Integrações

* Firebase Cloud Messaging (FCM) para notificações push.
* Potencial integração com o sistema de CRM da seguradora (detalhes não fornecidos).

## Fluxos Principais

**Fluxo de Indicação:**

1. Usuário acessa o PWA e preenche o formulário de indicação.
2. O frontend envia os dados para a API REST do backend.
3. O backend valida os dados e persiste no banco de dados PostgreSQL.
4. O backend envia uma notificação push para o administrador via FCM.
5. O administrador confirma a indicação pelo painel administrativo.
6. O backend atualiza o status da indicação no banco de dados e calcula o desconto.
7. O backend envia uma notificação push para o usuário que indicou via FCM.

**Fluxo de Login:**

1. Usuário acessa a tela de login do PWA.
2. O frontend envia as credenciais para a API REST do backend.
3. O backend autentica o usuário e gera um JWT.
4. O frontend recebe o JWT e o armazena para requisições subsequentes.

**Fluxo de Painel Administrativo:**

1. Administrador acessa o painel administrativo.
2. O frontend faz requisições à API REST para obter dados das indicações.
3. O administrador confirma ou rejeita indicações.
4. O backend atualiza o banco de dados e envia notificações push conforme necessário.

