```markdown
# Backlog MVP - Loja Online

## Épicos e User Stories

**Épico: Catálogo de Produtos**

* US1: Como cliente, quero buscar por um produto para encontrá-lo rapidamente.  (Must-Have)
* US2: Como cliente, quero ver os detalhes de um produto (fotos, preço, descrição) para decidir pela compra. (Must-Have)
* US3: Como admin, quero cadastrar e editar produtos para manter o catálogo atualizado. (Must-Have)

**Épico: Jornada de Compra**

* US4: Como cliente, quero adicionar um item ao meu carrinho de compras. (Must-Have)
* US5: Como cliente, quero passar por um processo de checkout para informar meu endereço e pagar. (Must-Have)  - Inclui pagamento com cartão de crédito e cálculo de frete dos correios.

**Épico: Contas de Usuário**

* US6: Como cliente, quero me cadastrar no site para ter uma conta e acompanhar meus pedidos. (Must-Have)

**Épico: Notificações**

* US7: Como cliente, quero receber um e-mail de confirmação quando meu pedido for aprovado. (Must-Have)
* US8: Como cliente, quero receber um e-mail quando meu pedido for enviado com o código de rastreio. (Must-Have)

## Critérios de Aceitação

**US6: Como cliente, quero me cadastrar no site para ter uma conta.**
* CA1: Dado que estou na página de cadastro, quando preencho meu nome, e-mail e uma senha válida e clico em "Cadastrar", então minha conta é criada e sou redirecionado para a página inicial logado.
* CA2: Dado que tento me cadastrar com um e-mail que já existe, quando clico em "Cadastrar", então vejo uma mensagem de erro "Este e-mail já está em uso".

**US7: Como cliente, quero receber um e-mail de confirmação quando meu pedido for aprovado.**
* CA1: Dado que finalizei uma compra com sucesso, quando meu pagamento é aprovado, então eu devo receber um e-mail no endereço da minha conta.
* CA2: O e-mail recebido deve conter o número do pedido, o resumo dos itens comprados e o valor total pago.

**US8: Como cliente, quero receber um e-mail quando meu pedido for enviado com o código de rastreio.**
* CA1: Dado que meu pedido foi aprovado e enviado, então eu recebo um email contendo o código de rastreio.


## Tarefas (Priorizadas por MoSCoW)

**Must-Have:**

* [ ] Implementar Busca de Produtos (US1)
* [ ] Implementar Página de Detalhes do Produto (US2)
* [ ] Implementar Adição ao Carrinho (US4)
* [ ] Implementar Cadastro de Cliente (US6)
* [ ] Implementar Checkout com Cartão de Crédito (US5)
* [ ] Implementar Cálculo de Frete dos Correios (US5)
* [ ] Implementar Cadastro de Produtos (Admin) (US3)
* [ ] Implementar Visualização de Pedidos (Admin) (US3) -  (considerar prioridade alta)
* [ ] Implementar Notificação por e-mail: Pedido Confirmado (US7)
* [ ] Implementar Notificação por e-mail: Pedido Enviado (US8)

**Should-Have:**

* [ ] Implementar Login com Google (US6)
* [ ] Implementar Filtros de Busca (US1)
* [ ] Implementar Gestão de Estoque (Admin) (US3)
* [ ] Implementar Pagamento com Pix (US5)

**Could-Have:**

* [ ] Implementar Sistema de Avaliação de Produtos
* [ ] Implementar Lista de Desejos

**Won't-Have:**

* Marketplace
* Programa de Fidelidade
```
