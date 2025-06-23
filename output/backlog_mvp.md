# Funcionalidades (Épicos e User Stories)
*   **Épico: Catálogo de Produtos**
    *   Como cliente, quero buscar por um produto para encontrá-lo rapidamente.
    *   Como cliente, quero ver os detalhes de um produto (fotos, preço, descrição) para decidir pela compra.
    *   Como admin, quero cadastrar e editar produtos para manter o catálogo atualizado.
*   **Épico: Jornada de Compra**
    *   Como cliente, quero adicionar um item ao meu carrinho de compras.
    *   Como cliente, quero passar por um processo de checkout para informar meu endereço e pagar.
*   **Épico: Contas de Usuário**
    *   Como cliente, quero me cadastrar no site para ter uma conta e acompanhar meus pedidos.
*   **Épico: Notificações**
    *   Como cliente, quero receber um e-mail de confirmação quando meu pedido for aprovado.
    *   Como cliente, quero receber um e-mail quando meu pedido for enviado com o código de rastreio.

# Critérios de Aceitação
*   **User Story:** Como cliente, quero me cadastrar no site para ter uma conta.
    *   **Critério 1:** Dado que estou na página de cadastro, quando preencho meu nome, e-mail e uma senha válida e clico em "Cadastrar", então minha conta é criada e sou redirecionado para a página inicial logado.
    *   **Critério 2:** Dado que tento me cadastrar com um e-mail que já existe, quando clico em "Cadastrar", então vejo uma mensagem de erro "Este e-mail já está em uso".

*   **User Story:** Como cliente, quero receber um e-mail de confirmação quando meu pedido for aprovado.
    *   **Critério 1:** Dado que finalizei uma compra com sucesso, quando meu pagamento é aprovado, então eu devo receber um e-mail no endereço da minha conta.
    *   **Critério 2:** O e-mail recebido deve conter o número do pedido, o resumo dos itens comprados e o valor total pago.

# Priorização (MoSCoW)
### Must-Have (Essencial para o lançamento)
*   Busca de produto.
*   Página de detalhes do produto.
*   Adicionar ao carrinho.
*   Cadastro de cliente.
*   Checkout com Cartão de Crédito.
*   Cálculo de frete dos Correios.
*   Admin: Cadastro de produtos.
*   Admin: Visualização de pedidos.
*   Notificação por e-mail: Pedido Confirmado.
*   Notificação por e-mail: Pedido Enviado.

### Should-Have (Importante, mas não bloqueia)
*   Login com Google.
*   Filtros de busca (preço, categoria).
*   Admin: Gestão de estoque.
*   Pagamento com Pix.

### Could-Have (Desejável)
*   Sistema de avaliação de produtos (estrelas e comentários).
*   Lista de desejos (Wishlist).
*   Admin: Dashboard com gráficos de vendas.

### Won't-Have (Fora do MVP)
*   Marketplace.
*   Programa de fidelidade.