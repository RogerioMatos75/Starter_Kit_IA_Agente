# Regras de Negócio, Restrições e Exceções - Sistema de E-commerce

## Regras de Negócio (RN)

* **RN01:**  Cada produto deve estar associado a pelo menos uma categoria.
* **RN02:** O estoque de um produto nunca pode ser negativo. Vendas somente são permitidas se o estoque for maior que zero.
* **RN03:** Após a confirmação do pagamento, o estoque dos itens do pedido deve ser decrementado atomicamente.
* **RN04:** O endereço de e-mail do cliente deve ser único em todo o sistema.
* **RN05:** As senhas dos clientes devem ser armazenadas usando um algoritmo de hash assimétrico (ex: bcrypt).
* **RN06:** Um pedido só avança no fluxo de processamento após a confirmação explícita do gateway de pagamento.
* **RN07:**  A cada mudança de status principal do pedido (`Confirmado`, `Enviado`), uma notificação correspondente deve ser enviada ao cliente.


## Restrições

* **Restrição de Cupom:** Apenas um cupom de desconto pode ser aplicado por pedido.
* **Restrição de Carrinho:** Um item não pode ser adicionado ao carrinho em quantidade superior ao estoque disponível.
* **Restrição de Autenticação:** A finalização de um pedido (checkout) requer um usuário autenticado.


## Exceções

* **Estoque Indisponível no Checkout:** Se, no momento do checkout, o estoque de um item se esgotar, o usuário deve ser notificado e o item removido/marcado no carrinho, impedindo a conclusão do pedido até que a pendência seja resolvida.
* **Falha no Gateway de Pagamento:** Em caso de erro ou indisponibilidade do gateway de pagamento, o pedido deve receber o status `FALHA_PAGAMENTO` e o usuário deve ser notificado para tentar novamente ou usar outra forma de pagamento.
* **Falha no Serviço de Notificação:** Falhas no envio de e-mails não devem reverter ou bloquear a transação principal. O evento de notificação deve ser enfileirado para tentativas posteriores (dead-letter queue).

