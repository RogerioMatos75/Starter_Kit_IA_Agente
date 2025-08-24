## Arquitetura

A arquitetura proposta para o aplicativo NCF Indicação Seguros é baseada em microsserviços, permitindo escalabilidade e manutenabilidade individual de cada componente.  Utilizaremos uma arquitetura orientada a eventos para garantir a comunicação assíncrona entre os microsserviços.  Um gateway de API será responsável por rotear as requisições para os microsserviços apropriados.

## Tecnologias

* **Frontend:** React Native (para Android e iOS), permitindo uma base de código única e performance otimizada.
* **Backend:** Node.js com Express.js, oferecendo escalabilidade e performance para o tratamento das requisições.
* **Banco de Dados:** PostgreSQL para dados transacionais e persistência dos dados principais. Redis para cache e melhoria de performance.
* **Mensageria:** RabbitMQ para comunicação assíncrona entre os microsserviços.
* **Cloud:** AWS (Amazon Web Services) ou Google Cloud Platform (GCP) para infraestrutura e serviços em nuvem.
* **Push Notifications:** Firebase Cloud Messaging (FCM) ou AWS SNS para envio de notificações push.


## Integrações

* **Integração com provedor de seguros:** API para consulta de informações de apólices e aprovação de novos seguros.  A especificação da API dependerá do provedor escolhido.
* **Integração com gateway de pagamento:** API para processamento de pagamentos (se aplicável).  A escolha do gateway dependerá das necessidades específicas.
* **Integração com serviço de SMS (opcional):** Para notificações alternativas caso o push falhe.

## Fluxos Principais

**Fluxo de Indicação:**

1. O usuário (Assegurado) acessa o aplicativo e gera um código de indicação.
2. O código é enviado ao indicado via SMS ou aplicativo de mensagens.
3. O indicado utiliza o código para se cadastrar no aplicativo.
4. O indicado finaliza o processo de cadastro e solicitação de seguro.
5. O sistema verifica a aprovação do seguro do indicado.
6. Após aprovação:
    * O Assegurado recebe uma notificação push indicando o sucesso da indicação.
    * O Indicado recebe uma notificação push com os dados do Assegurado e informações sobre o contato de um consultor.
7. Um microsserviço de notificações dispara as mensagens push utilizando FCM.

**Fluxo de Administração:**

1. O administrador acessa o painel administrativo via web.
2. O painel administrativo permite a visualização de relatórios, gestão de usuários, configuração de parâmetros, etc.
3. O painel administrativo se comunica com os microsserviços via API REST.

**Fluxo de Consulta de Seguros (Assegurado):**

1. O Assegurado acessa o aplicativo e realiza login.
2. O aplicativo consulta informações de seguros via API.
3. Os dados são exibidos no aplicativo.
