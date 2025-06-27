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
    Rel(frontend, apiGateway, "Requisições", "HTTP")

    ContainerDb(postgreSQL, "PostgreSQL", "Banco de dados relacional", "Dados transacionais (Pedidos, Usuários)")
    ContainerDb(mongoDB, "MongoDB", "Banco de dados NoSQL", "Dados flexíveis (Catálogo)")

    Container(servicoPedidos, "Serviço de Pedidos", "Node.js com NestJS", "Processamento de pedidos")
    Rel(apiGateway, servicoPedidos, "Roteia requisição", "HTTP")
    Rel(servicoPedidos, postgreSQL, "Persistência", "JDBC")

    Container(servicoNotificacoes, "Serviço de Notificações", "Node.js com NestJS", "Envio de emails e notificações")
    Rel(servicoNotificacoes, apiGateway, "Envia mensagens", "HTTP")

    Container(servicoEstoque, "Serviço de Estoque", "Node.js com NestJS", "Gerenciamento de estoque")
    Rel(servicoPedidos, servicoEstoque, "Decrementa estoque", "RabbitMQ")


    Container(rabbitmq, "RabbitMQ", "Message Broker", "Comunicação assíncrona")
    Rel(servicoPedidos, rabbitmq, "Publica evento PedidoPago", "AMQP")
    Rel(servicoNotificacoes, rabbitmq, "Consome evento PedidoPago", "AMQP")
    Rel(servicoEstoque, rabbitmq, "Consome evento PedidoPago", "AMQP")


    Rel(servicoPedidos, "Gateway de Pagamento (Stripe)", "Processa pagamento", "REST")
    Rel(servicoNotificacoes, "Amazon SES", "Envio de emails", "SMTP/REST")

    Container(redis, "Redis", "Cache", "Armazenamento em cache")
    Rel(servicoPedidos, redis, "Consulta cache", "Redis protocol")

}


@enduml
```
