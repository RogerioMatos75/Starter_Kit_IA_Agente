## Arquitetura

Microsserviços.  A aplicação será dividida em microsserviços independentes para maior escalabilidade, manutenibilidade e flexibilidade.  Os principais microsserviços serão:  Módulo de Usuário (Administrador, Assegurado, Indicado), Módulo de Indicacão, Módulo de Notificações (Push Notifications), e Módulo de Integração com Seguradora (se aplicável).

## Tecnologias

* **Frontend:** React Native (para iOS e Android), React (para painel administrativo web).
* **Backend:** Node.js com Express.js (ou similar, como Spring Boot (Java) ou .NET).
* **Banco de Dados:** PostgreSQL (ou similar banco de dados relacional).  Considerar uso de Redis para cache.
* **Mensageria:** RabbitMQ (ou similar, como Kafka) para comunicação assíncrona entre microsserviços.
* **Push Notifications:** Firebase Cloud Messaging (FCM) ou similar.
* **Cloud Provider:** AWS (ou Google Cloud, Azure).


## Integrações

* **Integração com Seguradora:**  API REST para comunicação com o sistema da seguradora (detalhes a serem definidos em projeto detalhado).  Esta integração pode exigir adaptadores específicos dependendo da API da seguradora.
* **Integração com serviço de envio de SMS:** Para notificações complementares (opcional).
* **Integração com serviço de pagamento:** Se necessário para processamento de pagamentos.


## Fluxos Principais

**Fluxo de Indicação:**

1. Usuário (Assegurado) gera um link de indicação.
2. O link é compartilhado com o Indicado.
3. Indicado clica no link e preenche seus dados.
4. Módulo de Indicação valida os dados e submete a solicitação à seguradora.
5.  Módulo de Notificações envia Push Notification para Assegurado e Indicado com o status da indicação.
6. Após aprovação pela seguradora, o Módulo de Notificações envia Push Notification ao Assegurado confirmando a indicação bem sucedida.

**Fluxo de Administração:**

1. Administrador acessa o painel administrativo web.
2. Painel permite monitorar indicadores de performance, gerenciar usuários, e visualizar relatórios.


**Fluxo de Login:**

1. Usuário insere credenciais.
2. Autenticação via JWT (JSON Web Token) ou similar.
3. Token é usado para autenticação em todas as requisições subsequentes.
