## Arquitetura

Será utilizada uma arquitetura de microsserviços para garantir escalabilidade, manutenabilidade e flexibilidade.  Os microsserviços serão independentes e comunicáveis através de uma API Gateway.  Cada microsserviços será responsável por uma funcionalidade específica, como cadastro de usuários, processamento de indicações e envio de notificações.

## Tecnologias

* **Frontend:** React Native (para garantir compatibilidade com iOS e Android), utilizando um framework de UI como o React Navigation.
* **Backend:** Node.js com Express.js para a API.
* **Banco de Dados:** PostgreSQL para dados persistentes. Redis para cache.
* **Mensageria:** RabbitMQ ou Kafka para comunicação assíncrona entre microsserviços.
* **Notificações Push:** Firebase Cloud Messaging (FCM).
* **API Gateway:** Kong ou similar.
* **Infraestrutura:** AWS (ou similar), utilizando serviços como EC2, S3, RDS, e EKS (Kubernetes).


## Integrações

* **Integração com provedor de pagamentos:** Integração com uma API de gateway de pagamentos (ex: Stripe, PayPal) para processar pagamentos de seguros.
* **Integração com serviço de envio de SMS:** Integração com um serviço de envio de SMS (ex: Twilio) para notificações complementares.
* **Integração com CRM (opcional):** Integração com um sistema de CRM (ex: Salesforce, HubSpot) para gerenciamento de clientes.


## Fluxos Principais

**Fluxo de Indicação:**

1. Usuário (Assegurado) indica um amigo/parente através do aplicativo.
2. O aplicativo envia uma requisição à API de indicações.
3. A API valida os dados e registra a indicação.
4. Uma mensagem é publicada na fila de mensagens para processar a indicação.
5. O microsserviço de notificações envia uma notificação push para o Assegurado confirmando a indicação.
6. Uma vez aprovada a indicação, a API envia uma notificação push para o indicado com dados do Assegurado e informação de contato do consultor.
7. O Consultor é notificado (via CRM ou outro método) sobre a nova indicação.

**Fluxo de Administração:**

1. Administrador acessa o painel administrativo.
2. O painel administrativo interage com a API para exibir relatórios, gerenciar usuários e controlar as diferentes funcionalidades do sistema.

**Fluxo de Cadastro:**

1. Usuário se cadastra via app.
2. Dados são enviados para a API de usuários.
3. Dados são validados e persistidos no banco de dados.
4. Usuário recebe um e-mail de confirmação.
