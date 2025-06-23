# Arquitetura
A arquitetura adotada será baseada no padrão de **Microsserviços orquestrados por eventos**. Cada domínio de negócio principal (ex: Catálogo, Pedidos, Usuários, Notificações) será implementado como um serviço independente e autocontido.

A comunicação entre o cliente (Frontend) e o backend será feita através de um **API Gateway**, que atua como um ponto de entrada único, simplificando a segurança e o roteamento. A comunicação interna entre os microsserviços será primariamente **assíncrona**, utilizando uma Fila de Mensagens (Message Broker) para garantir desacoplamento e resiliência.

**Exemplo de Diagrama de Fluxo:**
`[Cliente] -> [API Gateway] -> [Serviço de Pedidos] -> [Fila de Mensagens] -> [Serviço de Notificações] -> [Serviço Externo de E-mail]`

# Tecnologias
| Componente | Tecnologia Recomendada | Justificativa |
| :--- | :--- | :--- |
| **Frontend** | React.js (com Next.js) | SSR para SEO, ecossistema robusto, componentização. |
| **Backend** | Node.js (com NestJS) | Linguagem unificada (JS), alta performance para I/O, excelente para arquiteturas de eventos. |
| **Bancos de Dados** | PostgreSQL & MongoDB | **PostgreSQL** para dados transacionais (ACID); **MongoDB** para dados flexíveis como catálogo. |
| **API Gateway** | Kong ou AWS API Gateway | Centralização de segurança (JWT), rate limiting e roteamento. |
| **Mensageria** | RabbitMQ | Padrão AMQP, roteamento flexível de mensagens, ideal para desacoplar eventos. |
| **Cache** | Redis | Armazenamento de sessões, cache de dados frequentemente acessados. |
| **Infraestrutura** | Docker & Kubernetes (AWS EKS) | Containerização para portabilidade e orquestração para escalabilidade e resiliência. |

# Integrações
As integrações são pontos de contato com serviços de terceiros, essenciais para a operação.
*   **Pagamentos:** Conexão com Gateways de Pagamento via API REST para processar transações.
    *   *Exemplo:* Stripe, Pagar.me.
*   **Frete:** Conexão com APIs de Transportadoras ou Hubs de Frete para cálculo de preço e prazo em tempo real.
    *   *Exemplo:* Correios, Melhor Envio.
*   **Notificações:** Conexão com Serviços de E-mail Transacional (SMTP ou API).
    *   *Exemplo:* Amazon SES, SendGrid.
*   **Autenticação:** Opcional, via OAuth2, para login com provedores sociais.
    *   *Exemplo:* Google, Facebook.

# Fluxos Principais (Técnicos)
**Fluxo de Finalização de Pedido:**
1.  O Frontend envia uma requisição `POST /orders` para o API Gateway.
2.  O Gateway valida o token JWT e roteia a chamada para o `serviço-de-pedidos`.
3.  O `serviço-de-pedidos` valida os dados, processa a lógica de negócio e salva o pedido no PostgreSQL com status `AGUARDANDO_PAGAMENTO`.
4.  Ele chama a API do gateway de pagamento. Com a confirmação, o status é atualizado para `PAGAMENTO_APROVADO`.
5.  O serviço publica um evento `PedidoPago` na fila de mensagens (RabbitMQ).
6.  O `serviço-de-notificacoes`, que está ouvindo essa fila, consome o evento.
7.  O `serviço-de-notificacoes` formata o e-mail e o envia através da API do Amazon SES.
8.  O `serviço-de-estoque` também consome o evento e decrementa o estoque dos produtos.