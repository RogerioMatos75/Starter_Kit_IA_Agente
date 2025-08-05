## Arquitetura

Microsserviços.  A aplicação será dividida em microsserviços independentes para melhor escalabilidade, manutenção e desenvolvimento. Microsserviços separados para:  Usuário (Assegurado e Administrador), Indicador, Notificações Push, e Processamento de Indicacao.

## Tecnologias

* **Frontend:** React Native (para iOS e Android), React para o painel administrativo.
* **Backend:** Node.js com Express.js ou similar.
* **Banco de Dados:** PostgreSQL (para dados principais) e Redis (para cache).
* **Mensageria:** RabbitMQ ou Kafka para comunicação assíncrona entre microsserviços.
* **Notificações Push:** Firebase Cloud Messaging (FCM) ou similar.
* **Infraestrutura:** AWS ou Google Cloud Platform (GCP).
* **Testes:** Jest, Cypress, Mocha.


## Integrações

* **Integração com provedor de notificações push:** FCM ou similar.
* **Integração com gateway de pagamento:** (a definir dependendo da solução de pagamento escolhida).
* **Integração com serviço de envio de SMS:** (opcional, para comunicação adicional).
* **Integração com sistema de CRM:** (opcional, para gerenciamento de relacionamento com o cliente).


## Fluxos Principais

**Fluxo de Indicação:**

1. O Assegurado acessa a tela de indicação e insere os dados do indicado.
2. O sistema valida os dados e cria um registro de indicação.
3. O indicado recebe uma notificação push com um link para completar o cadastro.
4. O indicado completa o cadastro.
5. O sistema valida o cadastro do indicado.
6. Se aprovado, o Assegurado e o Indicado recebem notificações push.
7. Um consultor é notificado para dar um retorno ao indicado.

**Fluxo de Administração:**

1. O administrador acessa o painel administrativo.
2. O administrador pode visualizar relatórios, gerenciar usuários, e monitorar indicadores.


