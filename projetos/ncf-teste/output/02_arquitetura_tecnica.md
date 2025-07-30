# 02_arquitetura_tecnica.md

## Arquitetura

Será utilizada uma arquitetura de microsserviços para permitir maior escalabilidade, manutenibilidade e flexibilidade. Os microsserviços serão:

* **Serviço de Usuários:** Gerenciamento de usuários (Indicadores e Indicados), autenticação e autorização.
* **Serviço de Seguros:** Catálogo de seguros, informações sobre planos e preços.  Integração com APIs de seguradoras (se necessário).
* **Serviço de Indicações:** Gerenciamento de indicações, cálculo de descontos e registro de aprovações.
* **Serviço de Notificações:** Envio de notificações push (Android e iOS).
* **Serviço de Gamificação:** Sistema de pontos, recompensas e ranking.
* **Gateway API:** Ponto único de entrada para todos os microsserviços, com roteamento e balanceamento de carga.


## Tecnologias

* **Frontend:** React Native (para desenvolvimento cross-platform - Android e iOS), podendo ser React para versão web.
* **Backend:** Node.js com Express.js (ou similar como Spring Boot ou .NET para maior performance se necessário, dependendo de volume futuro).
* **Banco de Dados:** PostgreSQL (ou similar como MongoDB se houver alta necessidade de flexibilidade de dados).
* **Mensageria:** RabbitMQ (ou Kafka para alta escalabilidade) para comunicação assíncrona entre microsserviços.
* **Notificações Push:** Firebase Cloud Messaging (FCM) ou Apple Push Notification service (APNs).
* **Cloud Provider:** AWS, Google Cloud ou Azure (a ser definido).
* **Testes:** Jest, Cypress (Frontend), Mocha, Chai (Backend).


## Integrações

* **APIs de Seguradoras:** Integração com APIs de seguradoras para obtenção de informações sobre seguros (se aplicável).  Esta integração deverá ser bem definida no escopo do projeto e detalhada posteriormente.  Considerar o uso de padrões como REST e OAuth 2.0.
* **Serviços de Notificações Push:** Integração com FCM e/ou APNs.


## Fluxos Principais

**1. Fluxo de Indicação:**

1. O Indicador acessa o aplicativo e seleciona um seguro para indicar.
2. O Indicador insere os dados do Indicado (nome, email, telefone).
3. O sistema valida os dados e registra a indicação no Serviço de Indicações.
4. Uma notificação é enviada ao Indicado através do Serviço de Notificações.
5. O Indicado aceita a indicação e completa o processo de contratação do seguro (através da integração com a seguradora se aplicável).
6. Após a aprovação da seguradora, o Indicador e o Indicado recebem notificações push informando sobre a aprovação.

**2. Fluxo de Gerenciamento de Indicações:**

1. O Indicador acessa a seção "Minhas Indicações" no aplicativo.
2. O sistema recupera as informações das indicações do Serviço de Indicações.
3. O sistema exibe a lista de indicações, status e recompensas.

**3. Fluxo de Resgate de Desconto:**

1. O Indicado acessa a seção "Meus Descontos".
2. O sistema recupera as informações de descontos do Serviço de Indicações.
3. O Indicado seleciona o desconto a ser resgatado.
4. O sistema aplica o desconto no processo de contratação do seguro (integração com a seguradora se aplicável).

**4. Fluxo de Administração:**

* O administrador terá acesso a um painel para monitorar o sistema, visualizar dados e gerenciar usuários.  Um microsserviço dedicado para a administração pode ser considerado se necessário.  Acesso com autenticação e autorização robustas.

**Observação:** A complexidade e os detalhes de cada fluxo serão definidos em etapas posteriores com a participação da equipe de desenvolvimento e análise.
