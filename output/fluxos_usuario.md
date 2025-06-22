# Fluxos de Usuário Principais

Esta seção descreve as jornadas mais comuns dos usuários na plataforma.

### 1. Fluxo: Descoberta de Produto e Adição ao Carrinho
1.  **Usuário Anônimo** acessa a página inicial.
2.  Visualiza banners de destaque e listas de produtos (ex: "Mais Vendidos", "Novidades").
3.  Usa a **barra de busca** para procurar por "smartphone".
4.  O sistema exibe uma página de resultados com uma lista de smartphones.
5.  O usuário aplica **filtros**: "Marca X" e faixa de preço "R$ 1000 - R$ 2000".
6.  A lista de produtos é atualizada conforme os filtros.
7.  O usuário clica em um produto para ver a **página de detalhes**.
8.  Ele lê a descrição, vê as imagens e as avaliações de outros clientes.
9.  Clica no botão **"Adicionar ao Carrinho"**.
10. Um pop-up ou mini-carrinho confirma que o produto foi adicionado.

### 2. Fluxo: Checkout (Cliente Novo)
1.  O usuário clica no ícone do carrinho e depois em **"Finalizar Compra"**.
2.  É redirecionado para a página de checkout. Como não está logado, o sistema solicita **identificação**.
3.  O usuário insere seu e-mail e seleciona a opção para criar uma conta.
4.  **Etapa 1: Dados Pessoais e Endereço.** Preenche nome, CPF, telefone e o endereço de entrega.
5.  **Etapa 2: Frete.** O sistema, com base no CEP, exibe as opções de frete (PAC, Sedex) com seus respectivos custos e prazos. O usuário seleciona uma.
6.  **Etapa 3: Pagamento.** O usuário vê o resumo do pedido (produtos + frete). Ele seleciona a forma de pagamento (ex: Cartão de Crédito).
7.  Preenche os dados do cartão. O sistema envia esses dados diretamente para o gateway de pagamento (não armazena localmente).
8.  Aplica um **cupom de desconto**, se tiver um. O valor total é recalculado.
9.  Clica em **"Confirmar Pedido"**.
10. O sistema exibe uma tela de **sucesso** com o número do pedido e envia um e-mail de confirmação. A nova conta de usuário é criada em background.

### 3. Fluxo: Acompanhamento de Pedido (Cliente Logado)
1.  O usuário faz **login** em sua conta.
2.  Navega até a seção **"Meus Pedidos"**.
3.  O sistema exibe uma lista com todos os seus pedidos e o status atual de cada um.
4.  O usuário clica em um pedido com status **"Enviado"**.
5.  A página de detalhes do pedido exibe o histórico de status e o **código de rastreamento** da transportadora.