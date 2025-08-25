## Arquitetura

Arquitetura em microsserviços para maior escalabilidade, manutenibilidade e flexibilidade.  Os microsserviços serão:  Serviço de Usuário, Serviço de Indicação, Serviço de Notificação, Serviço de Apólice e Serviço de Administrador.  Um gateway API será utilizado para orquestrar as requisições.


## Tecnologias

* **Frontend:** React Native (para iOS e Android), permitindo código compartilhado e desenvolvimento mais rápido.
* **Backend:** Node.js com Express.js para APIs RESTful.
* **Banco de Dados:** PostgreSQL para armazenamento persistente de dados.  Considerar o uso de um banco de dados NoSQL (como MongoDB) para dados menos estruturados, como logs de notificações.
* **Mensageria:** RabbitMQ ou Kafka para comunicação assíncrona entre microsserviços, essencial para o envio de notificações push.
* **Notificações Push:** Firebase Cloud Messaging (FCM) para envio de notificações para dispositivos iOS e Android.
* **Testes:** Jest e Cypress para testes de unidade e integração.


## Integrações

* **Integração com provedor de pagamentos:** Para futuras funcionalidades de pagamento de prêmios.  A escolha do provedor dependerá da análise de requisitos específicos.
* **Integração com provedor de SMS:**  Para notificações complementares ao push (opcional).


## Fluxos Principais

**Fluxo de Indicação:**

1. O Asegurado acessa o aplicativo e cria uma nova indicação, informando os dados do indicado.
2. O Serviço de Usuário valida os dados do Asegurado.
3. O Serviço de Indicação cria um novo registro de indicação, associando-o ao Asegurado.
4. O Serviço de Notificação envia uma notificação push para o Asegurado confirmando a indicação.
5. O Serviço de Notificação envia uma notificação push para o Indicado, com informações sobre o Asegurado que o indicou.
6. O Indicado completa o processo de cadastro e contratação do seguro.
7. O Serviço de Apólice cria a nova apólice.
8. Após aprovação da apólice, o Serviço de Desconto (implementado no Serviço de Apólice ou um serviço separado) calcula e aplica os descontos para o Asegurado e Indicado.
9. Notificações push são enviadas para ambos, comunicando a aprovação e o desconto aplicado.

**Fluxo de Administração:**

1. O Administrador acessa o painel administrativo via web.
2. O Serviço de Administrador fornece acesso ao painel com dashboards e relatórios, permitindo monitorar todas as indicações, usuários, apólices e descontos aplicados.
3. O Administrador pode gerar relatórios personalizados para análise de dados.
