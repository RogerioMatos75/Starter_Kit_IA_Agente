## Fluxos de Usuário

**Fluxo de Indicação (Usuário):**

1. Usuário acessa o aplicativo NCF Indicação Seguros.
2. Usuário realiza login (caso não esteja logado).
3. Usuário acessa a tela de indicação.
4. Usuário preenche o formulário com os dados do indicado (nome, telefone, email).
5. Usuário envia a indicação.
6. Sistema valida os dados e retorna uma mensagem de confirmação.
7. Sistema envia notificação push para o administrador.
8. Após aprovação do administrador, usuário recebe notificação push confirmando a indicação e informando sobre o desconto.

**Fluxo de Administração (Administrador):**

1. Administrador acessa o aplicativo NCF Indicação Seguros.
2. Administrador realiza login.
3. Administrador acessa o painel administrativo.
4. Administrador visualiza as indicações pendentes.
5. Administrador visualiza detalhes da indicação (quem indicou e quem foi indicado).
6. Administrador confirma ou rejeita a indicação.
7. Se confirmado, sistema envia notificação push ao usuário que indicou e envia um link para o indicado.
8. Administrador registra a contratação do seguro pelo indicado (se aplicável).
9. Sistema gera relatórios sobre indicações, conversões e descontos concedidos.

**Fluxo de Indicação (Indicado):**

1. Indicado recebe notificação push com informações sobre a indicação e o contato do indicador.
2. Indicado acessa o link da proposta.
3. Indicado decide se contrata o seguro.
4. Se contratado, sistema notifica o administrador e o indicador.


## Navegação

**Usuário:**

* Tela inicial: Login/Cadastro, Indicar Amigo, Meus Descontos.
* Tela de Login: Campo email, campo senha, botão login, link para recuperação de senha, link para cadastro.
* Tela de Cadastro: Campos de preenchimento de dados pessoais.
* Tela de Indicar Amigo: Formulário com campos para nome, telefone e email do indicado, botão "Indicar".
* Tela Meus Descontos: Exibição do percentual de desconto acumulado.


**Administrador:**

* Tela inicial: Painel Administrativo.
* Painel Administrativo: Lista de indicações pendentes, detalhes da indicação, botões para confirmar/rejeitar indicações, geração de relatórios.
* Tela de Detalhes da Indicação: Dados completos da indicação, incluindo nome do indicador, nome do indicado, status da indicação, opção para enviar link ao indicado, registro de contratação.
* Tela de Relatórios: Opções de filtro e geração de relatórios.


## Interações

**Usuário:**

* Inserir dados no formulário de indicação.
* Enviar a indicação.
* Receber notificação push de confirmação de indicação e desconto concedido.
* Acessar a tela de Meus Descontos.
* Realizar login.

**Sistema (Usuário):**

* Validar dados do formulário de indicação.
* Enviar notificação push ao administrador.
* Enviar notificação push ao usuário após aprovação da indicação.
* Exibir o desconto acumulado.
* Redirecionar para tela de sucesso após envio da indicação.


**Administrador:**

* Visualizar lista de indicações pendentes.
* Visualizar detalhes da indicação.
* Confirmar ou rejeitar uma indicação.
* Enviar link para o indicado.
* Registrar a contratação do seguro.
* Gerar relatórios.
* Realizar login.

**Sistema (Administrador):**

* Enviar notificação push para o administrador quando uma nova indicação é feita.
* Atualizar o status da indicação.
* Enviar link da proposta para o indicado.
* Enviar notificação push ao indicador após a confirmação da indicação.
* Gerar relatórios em diferentes formatos (PDF, CSV, etc.).
* Mostrar mensagem de erro caso o login seja inválido.

**Indicado:**

* Receber notificação push.
* Acessar o link da proposta.

**Sistema (Indicado):**

* Enviar notificação push com dados do indicador e link da proposta.
* Redirecionar para a página da proposta ao clicar no link.

