## Fluxos de Usuário

**Fluxo 1: Usuário Assinado Indica um Amigo**

1. Usuário logado acessa a tela principal do aplicativo NCF Indicação Seguros.
2. Usuário visualiza opção "Indicar Amigo" (botão, ícone, link).
3. Usuário clica em "Indicar Amigo".
4. Usuário insere dados do indicado (nome, telefone, email).
5. Sistema valida os dados inseridos.
6. Sistema envia um convite por SMS e/ou email para o indicado.
7. Sistema apresenta mensagem de confirmação ao usuário com um ID de indicação.
8. Indicado aceita o convite e se cadastra no aplicativo.
9. Após aprovação do indicado, o usuário recebe uma notificação push parabenizando pela indicação bem-sucedida.


**Fluxo 2: Indicado Aceita o Convite**

1. Indicado recebe convite por SMS e/ou email com link para o aplicativo.
2. Indicado acessa o link e é direcionado para a tela de cadastro do aplicativo.
3. Indicado preenche o formulário de cadastro.
4. Sistema valida os dados inseridos.
5. Indicado recebe uma notificação push confirmando o cadastro e informando que um consultor entrará em contato.
6. Consultor entra em contato com o indicado.


**Fluxo 3: Administrador gerencia indicações**

1. Administrador acessa o painel administrativo.
2. Administrador seleciona a opção "Indicados".
3. Administrador visualiza lista de indicações, com status (pendente, aprovado, rejeitado).
4. Administrador pode filtrar e ordenar a lista por data, status, etc.
5. Administrador pode visualizar detalhes de cada indicação.
6. Administrador pode aprovar ou rejeitar indicações.


## Navegação

**Tela Principal (Usuário Assinado):** Botão/Link "Indicar Amigo", acesso ao perfil, etc.
**Tela Indicar Amigo:** Campos para inserir dados do indicado (nome, telefone, email), botão "Enviar convite".
**Tela Confirmação de Indicação:** Mensagem de sucesso com ID de indicação.
**Tela Cadastro (Indicado):** Formulário de cadastro padrão.
**Painel Administrativo:** Menu com opção "Indicados", tela de listagem de indicações, tela de detalhe da indicação.


## Interações

**Usuário:** Clica em botões, preenche formulários, recebe e interage com notificações push.
**Sistema:** Valida dados, envia convites, notifica usuários, apresenta mensagens de sucesso e erro, gerencia o status das indicações.  
**Notificações Push:**  Parabeniza o usuário pela indicação bem-sucedida (após aprovação do indicado). Informa ao indicado que foi indicado e que um consultor entrará em contato.
