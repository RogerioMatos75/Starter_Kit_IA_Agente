## Arquitetura

Será utilizada uma arquitetura de microsserviços para maior escalabilidade, manutenibilidade e flexibilidade.  Os microsserviços serão independentes e se comunicarão através de uma API Gateway.  Um serviço dedicado será responsável pelo envio de notificações Push.

## Tecnologias

* **Frontend:** React Native (para iOS e Android), permitindo código base única e melhor performance.
* **Backend:** Node.js com Express.js, para agilidade no desenvolvimento e escalabilidade.
* **Banco de Dados:** PostgreSQL, por sua robustez e escalabilidade, com suporte a transações e relacionamentos complexos.  Redis será usado para cache.
* **API Gateway:** Kong ou similar, para roteamento de requisições, autenticação e segurança.
* **Mensageria:** RabbitMQ para comunicação assíncrona entre microsserviços.
* **Notificações Push:** Firebase Cloud Messaging (FCM) ou similar.
* **Infraestrutura:** Cloud Provider (AWS, GCP ou Azure), para escalabilidade e resiliência.


## Integrações

* **Integração com provedor de pagamentos:**  Para processamento de pagamentos de seguros.  (Exemplo: Stripe, PayPal).
* **Integração com serviço de envio de SMS:** Para comunicação complementar às notificações push. (Exemplo: Twilio).
* **Integração com serviço de geolocalização:** Para funcionalidades futuras (opcional).


## Fluxos Principais

**Fluxo de Indicação:**

1. O usuário (Assegurado) acessa a tela de indicação e insere os dados do indicado.
2. O sistema valida os dados.
3. Um convite é enviado ao indicado via Push Notification.
4. O indicado aceita o convite.
5. O indicado recebe um Push Notification com os dados do indicador.
6. Ao aprovação da indicação, o Assegurado recebe um Push Notification.
7. O sistema notifica um consultor para entrar em contato com o indicado.

**Fluxo de Administração:**

1. O administrador acessa o painel administrativo.
2. O administrador pode visualizar relatórios, gerenciar usuários, configurar promoções e acompanhar o status das indicações.

**Fluxo de Assegurado:**

1. O Assegurado acessa o aplicativo e visualiza suas informações.
2. O Assegurado pode visualizar o status das suas indicações.
3. O Assegurado pode visualizar os seus dados e os dados do seu plano.
