# Regras de Negócio do E-commerce

Este documento descreve as regras que governam as operações da plataforma.

### 1. Produtos e Estoque
*   **RN001:** Um produto deve pertencer a pelo menos uma categoria.
*   **RN002:** O preço de um produto não pode ser negativo. O preço de venda (com desconto) não pode ser maior que o preço original.
*   **RN003:** Um produto só pode ser vendido se seu estoque for maior que zero.
*   **RN004:** Ao adicionar um produto ao carrinho, o sistema deve reservar a quantidade do estoque por um tempo limitado (ex: 15 minutos). Se o tempo expirar, a reserva é liberada.
*   **RN005:** Após a confirmação do pagamento de um pedido, o estoque dos produtos correspondentes deve ser decrementado permanentemente.
*   **RN006:** Em caso de cancelamento de um pedido (antes do envio), o estoque dos produtos deve ser restaurado.

### 2. Pedidos e Pagamentos
*   **RN007:** Um cliente deve estar autenticado para finalizar um pedido.
*   **RN008:** Um pedido só é considerado "Confirmado" após a aprovação do pagamento pelo gateway.
*   **RN009:** O status de um pedido deve seguir um fluxo predefinido: `Aguardando Pagamento` -> `Pagamento Aprovado` -> `Em Separação` -> `Enviado` -> `Entregue`. Status adicionais podem incluir `Cancelado` ou `Devolvido`.
*   **RN010:** O valor do frete é calculado com base no CEP de destino, peso e dimensões dos produtos no carrinho.

### 3. Clientes e Autenticação
*   **RN011:** O e-mail de um cliente é único na plataforma.
*   **RN012:** A senha do cliente deve ser armazenada usando um algoritmo de hash forte e unidirecional (ex: bcrypt ou Argon2).
*   **RN013:** Um cliente pode ter múltiplos endereços de entrega cadastrados.

### 4. Promoções e Cupons
*   **RN014:** Um cupom de desconto pode ser de valor fixo (ex: R$ 20,00) ou percentual (ex: 10%).
*   **RN015:** Um cupom pode ter restrições, como valor mínimo do pedido, data de validade, limite de usos ou ser aplicável apenas a produtos/categorias específicas.
*   **RN016:** Apenas um cupom pode ser aplicado por pedido.