## Arquitetura

Arquitetura de microsserviços para maior escalabilidade, manutenibilidade e flexibilidade.  Os microsserviços serão:  Módulo de Usuários, Módulo de Indicados, Módulo de Indicadores, Módulo de Notificações Push, Módulo de Administração.

## Tecnologias

* **Frontend:** React Native (para iOS e Android), React para o painel administrativo.
* **Backend:** Node.js com Express.js (ou similar, como Python com Flask/Django).
* **Banco de Dados:** PostgreSQL (ou similar banco relacional).  Considerar Redis para cache.
* **Mensageria:** RabbitMQ ou Kafka para comunicação assíncrona entre microsserviços.
* **Notificações Push:** Firebase Cloud Messaging (FCM) ou similar.
* **Orquestração:** Docker e Kubernetes para deploy e gerenciamento dos microsserviços.
* **API Gateway:**  Kong ou similar para roteamento e segurança de APIs.


## Integrações

* **Integração com provedor de notificações push:** FCM ou similar para envio de notificações aos usuários.
* **Integração com serviço de SMS (opcional):**  Para notificação complementar, caso necessário.
* **Integração com CRM (futuro):**  Para integração com sistema de gestão de relacionamento com o cliente.


## Fluxos Principais

**Fluxo de Indicação:**

1. Assegurado acessa o aplicativo e gera um link de convite.
2. O link é compartilhado com o indicado.
3. Indicado acessa o link, preenche seus dados e confirma o convite.
4. O sistema valida os dados do indicado.
5. Se aprovado, o indicado e o indicador recebem notificações push. O indicador recebe um push de parabéns, e o indicado recebe um push com dados do indicador e a mensagem de contato de um consultor.
6.  O status da indicação é atualizado no sistema.

**Fluxo de Administração:**

1. Administrador acessa o painel administrativo.
2. Pode visualizar relatórios, gerenciar usuários, aprovar/rejeitar indicações, etc.

**Fluxo de Notificações:**

1. Evento aciona a fila de mensagens (ex: indicação aprovada).
2. Serviço de notificações consome mensagem da fila.
3. Serviço de notificações envia push para usuários relevantes através do FCM.
