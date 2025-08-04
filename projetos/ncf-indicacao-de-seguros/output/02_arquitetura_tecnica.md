## Arquitetura

Microsserviços, com separação clara entre serviços de usuário (Assegurado, Administrador), serviço de notificações push e serviço de processamento de indicações.  Cada microsserviços terá sua própria base de dados.  Comunicação entre microsserviços via API RESTful.

## Tecnologias

* **Frontend:** React Native (para assegurar compatibilidade com iOS e Android), React para o painel administrativo.
* **Backend:** Node.js com Express.js (por sua escalabilidade e performance).
* **Banco de Dados:** PostgreSQL (para o serviço de usuários e indicações) e Redis (para cache de dados sensíveis à performance como informações de usuários ativos e status de notificações).
* **Mensageria:** RabbitMQ ou Kafka para comunicação assíncrona entre microsserviços, especialmente para o processamento de indicações e envio de notificações.
* **Notificações Push:** Firebase Cloud Messaging (FCM).
* **Infraestrutura:**  Utilizar serviço de cloud como AWS ou Google Cloud Platform para escalabilidade e resiliência.


## Integrações

* **Integração com provedor de seguros:** API para consultar e processar informações de apólices de seguros.  (Detalhes da API precisarão ser definidos em conjunto com o provedor).
* **Integração com serviço de SMS (opcional):** Para notificações complementares caso o push falhe.


## Fluxos Principais

* **Fluxo de Indicação:** O Assegurado indica um novo cliente através do aplicativo. A informação é enviada ao serviço de processamento de indicações. Este serviço valida a indicação, consulta a API do provedor de seguros, e atualiza o status.  Um evento é enviado para a fila de mensagens para disparar notificações push.
* **Fluxo de Notificação:** O serviço de notificações recebe mensagens da fila de mensagens (RabbitMQ ou Kafka) para enviar notificações push (FCM) para o Assegurado e o indicado.
* **Fluxo de Administração:** O administrador acessa o painel administrativo (React) para monitorar indicações, usuários, e gerar relatórios.  Este painel se comunica com os microsserviços via API RESTful.
* **Fluxo de Login:** Autenticação e autorização de usuários (Assegurados e Administradores) via JWT.
