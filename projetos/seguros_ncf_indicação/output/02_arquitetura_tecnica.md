## Arquitetura

Arquitetura baseada em microsserviços para melhor escalabilidade, manutenibilidade e flexibilidade.  Serão criados microsserviços independentes para: Usuário, Indicação, Notificação Push, Apólice e Desconto.  Um gateway API centralizará o acesso aos microsserviços.  A comunicação entre os microsserviços será feita via API REST.

## Tecnologias

* **Frontend:** React Native (para iOS e Android), permitindo código base compartilhado e desenvolvimento mais rápido.
* **Backend:** Node.js com Express.js (para agilidade e escalabilidade).
* **Banco de Dados:** PostgreSQL (para robustez e escalabilidade).
* **Mensageria:** RabbitMQ (para lidar com notificações push de forma assíncrona e eficiente).
* **Cloud:** AWS (ou similar), para hospedagem dos microsserviços e banco de dados.
* **Notificações Push:** Firebase Cloud Messaging (FCM) para Android e Apple Push Notification service (APNs) para iOS.

## Integrações

* Integração com sistema legado da NCF (se existir) para acesso a informações de apólices e clientes.
* Integração com serviço de envio de SMS (opcional, para notificações complementares).

## Fluxos Principais

**Fluxo de Indicação:**

1. O Asegurado acessa o aplicativo e cria uma nova indicação, fornecendo dados do Potencial Cliente.
2. O microsserviço de Indicação registra a indicação e notifica o microsserviço de Notificação Push.
3. O microsserviço de Notificação Push envia uma notificação para o Asegurado confirmando a indicação.
4. O Potencial Cliente recebe uma notificação push com informações sobre a indicação.
5. Após aprovação da indicação, o microsserviço de Desconto aplica os descontos para ambos, Asegurado e Potencial Cliente.
6. Notificação push para o Asegurado sobre a aprovação da indicação.

**Fluxo de Administração:**

1. O Administrador acessa o painel administrativo via aplicativo web.
2. O painel exibe relatórios e dados sobre as indicações, usuários e descontos.
3. O Administrador pode gerenciar usuários, aprovar/rejeitar indicações e gerar relatórios customizados.

**Fluxo de Login e Cadastro:**

1. O usuário acessa a tela de login/cadastro no aplicativo.
2. O microsserviço de Usuário processa a autenticação/cadastro.
3. Em caso de sucesso, um token de acesso é gerado e usado para acessar as funcionalidades do app.
