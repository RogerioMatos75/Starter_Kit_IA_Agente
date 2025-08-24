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

<br>
<hr>
<br>

### 🧠 Instruções para o Agente de Desenvolvimento

**📝 Prompt Complementar:**
Este documento de prototipagem define a arquitetura e as tecnologias para o NCF Indicação Seguros, um MicroSaaS focado em indicações de seguros.  A próxima fase de desenvolvimento deve focar na construção de um MVP (Minimum Viable Product) funcional, validando o core do negócio: o fluxo de indicação e cadastro de novos clientes.  O objetivo é construir a funcionalidade mínima necessária para atrair os primeiros usuários e coletar feedback, permitindo iterações rápidas e ajustes baseados em dados reais.

**👍 Instruções Positivas:**
Desenhe um MVP enxuto, com interface mínima viável, focando exclusivamente no fluxo de indicação. Priorize a implementação do fluxo principal: geração do código de indicação pelo usuário (assegurado), envio do código para o indicado, cadastro do indicado, solicitação de seguro, aprovação e notificações de sucesso (push notifications para ambos). Implemente a integração com o provedor de seguros, mas utilize dados mockados inicialmente para testes e validação do fluxo. Concentre-se em um único método de notificação (FCM ou SMS) e um único gateway de pagamento se este for considerado necessário.  Utilize um banco de dados local para desenvolvimento e testes iniciais, migrando para PostgreSQL e Redis apenas quando necessário.  O painel administrativo deve ser limitado às funções essenciais para monitorar o fluxo de indicações e usuários.  Utilize a abordagem de microsserviços de forma pragmática, podendo ser implementados como monolito inicialmente caso isso facilite o desenvolvimento do MVP.

**👎 Instruções Negativas:**
Não adicione dashboards completos, relatórios complexos, perfis avançados de usuário, funcionalidades de gerenciamento de usuários complexas ou painéis de admin completos nesta fase. Evite a implementação de integrações com múltiplos gateways de pagamento ou serviços de SMS redundantes, e limite as notificações ao essencial. Não implemente recursos opcionais, como a consulta de seguros pelo segurado, antes de validar a viabilidade do fluxo principal.  Adiar a utilização de frameworks complexos para gerenciamento de microsserviços e a definição do ambiente de cloud (AWS ou GCP) até que o MVP seja validado.  Evite sobre-engenharia e concentre-se em entregar o valor mínimo para o usuário final o mais rápido possível.


--- REFINAMENTO DO ARCHON AI ---

Fluxo de Indicação (revisado):

1. O usuário (Assegurado) acessa o aplicativo e gera um código de indicação.
2. O código é enviado ao indicado via SMS ou aplicativo de mensagens.
3. O indicado utiliza o código para se cadastrar no aplicativo.
4. O indicado finaliza o processo de cadastro e solicitação de seguro.
5. O sistema verifica a aprovação do seguro do indicado.
6. Após aprovação:
    * O Assegurado recebe uma notificação push indicando o sucesso da indicação e o desconto de 1% ganho.
    * O Indicado recebe uma notificação push com os dados do Assegurado e informações sobre o contato de um consultor.
7. Um microsserviço de notificações dispara as mensagens push utilizando FCM.
