```plantuml
@startuml
!include <c4/C4_Context>
!include <c4/C4_Container>
!include <c4/C4_Component>

System_Boundary(c1, "Sistema de E-commerce") {
    Person(cliente, "Cliente", "Usuário do sistema")

    Container(apiGateway, "API Gateway", "Kong", "Roteamento de requisições, autenticação (JWT)")

    Container(frontend, "Frontend", "React.js com Next.js", "Interface do usuário")
    Rel(cliente, frontend, "Acessa", "HTTP")
    Rel(frontend, apiGateway, "Interage com", "REST")

    ContainerDb(dbPostgreSQL, "Banco de Dados Transacional", "PostgreSQL", "Dados transacionais (Pedidos, Usuários)")
    ContainerDb(dbMongoDB, "Banco de Dados NoSQL", "MongoDB", "Dados flexíveis (Catálogo)")

    Container(servicoPedidos, "Serviço de Pedidos", "Node.js com NestJS", "Processamento de pedidos")
    Rel(apiGateway, servicoPedidos, "Roteia requisições", "REST")
    Rel(servicoPedidos, dbPostgreSQL, "Persiste dados", "JDBC")

    Container(servicoNotificacoes, "Serviço de Notificações", "Node.js com NestJS", "Envia notificações por email")
    Rel(servicoPedidos, servicoNotificacoes, "Publica evento", "RabbitMQ")
    Rel(servicoNotificacoes, "Amazon SES", "Envia emails", "SMTP")

    Container(servicoEstoque, "Serviço de Estoque", "Node.js com NestJS", "Gerencia estoque de produtos")
    Rel(servicoPedidos, servicoEstoque, "Publica evento", "RabbitMQ")
    Rel(servicoEstoque, dbPostgreSQL, "Persiste dados", "JDBC")

    Container(servicoCatalogo, "Serviço de Catálogo", "Node.js com NestJS", "Gerencia informações de produtos")
    Rel(apiGateway, servicoCatalogo, "Roteia requisições", "REST")
    Rel(servicoCatalogo, dbMongoDB, "Persiste dados", "MongoDB Driver")

    Container(cacheRedis, "Cache", "Redis", "Cache de dados")
    Rel(servicoPedidos, cacheRedis, "Consulta/Grava", "Redis Protocol")
    Rel(servicoCatalogo, cacheRedis, "Consulta/Grava", "Redis Protocol")

    Rel(apiGateway, cacheRedis, "Armazena Sessões", "Redis Protocol")


}

System_Ext(gatewayPagamento, "Gateway de Pagamento", "Stripe/Pagar.me", "Processamento de pagamentos")
Rel(servicoPedidos, gatewayPagamento, "Processa pagamento", "REST")

System_Ext(apiFrete, "API de Frete", "Correios/Melhor Envio", "Cálculo de frete")
Rel(servicoPedidos, apiFrete, "Calcula frete", "REST")

@enduml
```
