## Fluxos de Usuário

### Fluxo de Indicação (Assegurado):

1. O Assegurado acessa o aplicativo NCF e navega até a seção "Indique um Amigo".
2. O Assegurado preenche um formulário com os dados do amigo/parente a ser indicado (nome, telefone e e-mail).
3. O sistema valida os dados fornecidos.
4. O sistema envia um convite (e-mail/SMS) para o amigo/parente com um link para o aplicativo ou um código de indicação.
5. O Assegurado recebe uma confirmação da solicitação de indicação.
6. Após a aprovação da indicação pelo sistema, o Assegurado recebe um push notificando sobre o sucesso da indicação e o desconto recebido.


### Fluxo de Aceite (Indicado):

1. O Indicado recebe um convite via e-mail/SMS/push.
2. O Indicado clica no link do convite ou insere o código de indicação no aplicativo.
3. O Indicado é redirecionado para uma tela com informações sobre o programa de indicação e os dados do Assegurado que o indicou.
4. O Indicado realiza o cadastro no aplicativo, caso ainda não seja usuário.
5. O sistema registra a indicação do Indicado.
6. O Indicado recebe um push notificando que um consultor entrará em contato em breve.


### Fluxo de Administração (Administrador):

1. O Administrador acessa o painel administrativo do aplicativo.
2. O Administrador visualiza as indicações recebidas, podendo filtrar por status (pendente, aprovado, rejeitado).
3. O Administrador pode aprovar ou rejeitar as indicações.
4. O Administrador monitora o desempenho do programa de indicação, visualizando métricas como número de indicações, taxa de conversão, etc.
5. O Administrador pode gerenciar as configurações do programa de indicação, como valores de desconto, etc.


## Navegação

### Assegurado:

* Tela Inicial > Indique um Amigo > Formulário de Indicação > Confirmação de Indicação

### Indicado:

* Link/SMS/Push > Tela de Boas-Vindas > Cadastro (se necessário) > Tela de Confirmação da Indicação

### Administrador:

* Painel Administrativo > Indicados > Detalhes da Indicação > Aprovar/Rejeitar Indicação > Relatórios


## Interações

### Assegurado:

* **Ação:** Preencher formulário de indicação.
* **Resposta:** Validação de dados e confirmação de envio.

* **Ação:** Acessar seção "Indique um Amigo".
* **Resposta:** Exibição da seção com as informações necessárias.

* **Ação:** Receber push de indicação aprovada.
* **Resposta:** Push notificando o sucesso da indicação e desconto.


### Indicado:

* **Ação:** Clicar no link do convite.
* **Resposta:** Redirecionamento para a tela de informações da indicação.

* **Ação:** Realizar cadastro.
* **Resposta:** Criação da conta e confirmação do cadastro.

* **Ação:** Receber push de contato do consultor.
* **Resposta:** Push notificando que um consultor entrará em contato em breve.


### Administrador:

* **Ação:** Aprovar/Rejeitar indicação.
* **Resposta:** Atualização do status da indicação e notificação ao Assegurado e/ou Indicado.

* **Ação:** Visualizar relatórios.
* **Resposta:** Exibição de métricas e dados do programa de indicação.
