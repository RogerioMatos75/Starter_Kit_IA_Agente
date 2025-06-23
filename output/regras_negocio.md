# Regras de Negócio
*   **RN01:** Um produto deve estar associado a, no mínimo, uma categoria.
*   **RN02:** O estoque de um produto não pode ser negativo. A venda só é permitida para estoque > 0.
*   **RN03:** Após a confirmação do pagamento, o estoque dos itens do pedido deve ser atomicamente decrementado.
*   **RN04:** O e-mail do cliente é um identificador único em todo o sistema.
*   **RN05:** As senhas dos clientes devem ser armazenadas utilizando um algoritmo de hash assimétrico (ex: bcrypt).
*   **RN06:** Um pedido só avança no fluxo de processamento após a confirmação explícita do gateway de pagamento.
*   **RN07:** A cada mudança de status principal do pedido (`Confirmado`, `Enviado`), uma notificação correspondente deve ser disparada para o cliente.

# Restrições
*   **Restrição de Cupom:** Apenas um cupom de desconto pode ser aplicado por pedido.
*   **Restrição de Carrinho:** Um item não pode ser adicionado ao carrinho em quantidade superior ao estoque disponível.
*   **Restrição de Autenticação:** A finalização de um pedido (checkout) é restrita a usuários autenticados.

# Exceções
*   **Estoque Indisponível no Checkout:** Se, no momento da finalização da compra, o estoque de um item se esgotar, o usuário deve ser notificado na tela de checkout com uma mensagem clara, e o item deve ser removido ou marcado em seu carrinho, impedindo a conclusão do pedido até que a pendência seja resolvida.
*   **Falha no Gateway de Pagamento:** Se o gateway de pagamento retornar um erro ou ficar indisponível, o pedido deve ser mantido com o status `FALHA_PAGAMENTO` e o usuário deve receber feedback imediato para tentar novamente ou usar outra forma de pagamento.
*   **Falha no Serviço de Notificação:** Uma falha no envio de e-mail não deve, em hipótese alguma, reverter ou bloquear a transação principal (confirmação do pedido). O evento de notificação deve ser colocado em uma fila de "tentativas posteriores" (dead-letter queue).

# Decisões
*   **Arquitetura de Microsserviços:** Decisão tomada para garantir escalabilidade granular (escalar apenas os serviços mais demandados, como o de catálogo) e resiliência (uma falha no serviço de notificações não derruba o checkout).
*   **Comunicação Assíncrona para Eventos:** Decisão tomada para desacoplar os serviços. Isso permite que a confirmação de um pedido seja uma operação rápida para o usuário, enquanto tarefas mais lentas (enviar e-mail, atualizar analytics) acontecem em background, sem impactar a experiência principal.