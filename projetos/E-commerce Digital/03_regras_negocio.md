## Regras de Negócio, Restrições e Exceções - E-commerce

**1. Regras de Negócio:**

* **RN01 - Associação de Categoria:** Todo produto deve estar associado a pelo menos uma categoria.
* **RN02 - Controle de Estoque:** O estoque de um produto nunca pode ser negativo. Vendas só são permitidas se o estoque for maior que zero.
* **RN03 - Decremento Atômico de Estoque:** Após a confirmação do pagamento, o estoque dos itens do pedido deve ser decrementado atomicamente.
* **RN04 - Unicidade de E-mail:** O e-mail do cliente deve ser único em todo o sistema.
* **RN05 - Armazenamento de Senha:** As senhas dos clientes devem ser armazenadas utilizando um algoritmo de hash assimétrico (ex: bcrypt).
* **RN06 - Confirmação de Pagamento:** Um pedido só avança no fluxo de processamento após a confirmação explícita do gateway de pagamento.
* **RN07 - Notificação de Mudança de Status:** A cada mudança de status principal do pedido (`Confirmado`, `Enviado`), uma notificação correspondente deve ser disparada para o cliente.


**2. Restrições:**

* **Restrição de Cupom:** Apenas um cupom de desconto pode ser aplicado por pedido.
* **Restrição de Carrinho:** Um item não pode ser adicionado ao carrinho em quantidade superior ao estoque disponível.
* **Restrição de Autenticação:** A finalização de um pedido (checkout) é restrita a usuários autenticados.


**3. Exceções:**

* **Exceção de Estoque Indisponível:** Se, no momento da finalização da compra, o estoque de um item se esgotar, o usuário deve ser notificado na tela de checkout com uma mensagem clara, e o item deve ser removido ou marcado em seu carrinho, impedindo a conclusão do pedido até que a pendência seja resolvida.
* **Exceção de Falha no Gateway de Pagamento:** Se o gateway de pagamento retornar um erro ou ficar indisponível, o pedido deve ser mantido com o status `FALHA_PAGAMENTO` e o usuário deve receber feedback imediato para tentar novamente ou usar outra forma de pagamento.
* **Exceção de Falha no Serviço de Notificação:** Uma falha no envio de e-mail não deve reverter ou bloquear a transação principal (confirmação do pedido). O evento de notificação deve ser colocado em uma fila de "tentativas posteriores" (dead-letter queue).

