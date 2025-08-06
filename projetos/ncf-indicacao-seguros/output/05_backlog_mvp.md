## Funcionalidades (Épicos e User Stories)

**Épico 1: Cadastro e Login**

* US1: Como usuário, quero me cadastrar no aplicativo fornecendo minhas informações pessoais (nome, CPF, telefone, email) para poder acessar os recursos.
* US2: Como usuário, quero fazer login no aplicativo usando meu email e senha para acessar minha conta.
* US3: Como usuário, quero recuperar minha senha caso eu a esqueça.

**Épico 2: Indicação de Seguros**

* US4: Como usuário (assegurado), quero indicar um amigo ou parente para um seguro, fornecendo o nome e o telefone do indicado.
* US5: Como usuário (assegurado), quero receber uma notificação push quando uma indicação minha for aprovada.
* US6: Como usuário (indicado), quero receber uma notificação push com as informações do meu indicador e a previsão de contato de um consultor.

**Épico 3: Administração**

* US7: Como administrador, quero acessar um painel administrativo para visualizar estatísticas de indicações e aprovações.
* US8: Como administrador, quero gerenciar os usuários cadastrados no sistema.
* US9: Como administrador, quero visualizar e gerenciar as indicações recebidas.


**Épico 4:  Visualização de dados do usuário**

* US10: Como usuário (assegurado), quero visualizar meu histórico de indicações e os descontos que obtive.

## Critérios de Aceitação

* **US1:**  Cadastro com validação de campos obrigatórios e formato de email.  Sucesso na criação da conta com envio de email de confirmação (opcional).
* **US2:** Login com validação de credenciais.  Tratamento de erro para credenciais inválidas.
* **US3:** Recuperação de senha via email com link para redefinição.
* **US4:**  Formulário de indicação com validação de campos obrigatórios (nome e telefone do indicado).
* **US5:** Notificação push enviada ao usuário após a aprovação da indicação, informando o sucesso da indicação.
* **US6:** Notificação push enviada ao indicado com nome do indicador e mensagem de contato do consultor (prazo).
* **US7:** Painel administrativo com gráficos de indicações e aprovações (total, por período, etc.).
* **US8:**  Interface administrativa para pesquisa, edição e exclusão de usuários.
* **US9:** Interface administrativa para visualizar o status das indicações (pendente, aprovado, rejeitado).
* **US10:**  Tela com histórico de indicações, data, status e valor do desconto obtido.


## Priorização (MoSCoW)

**Must Have:**

* US1 (Cadastro)
* US2 (Login)
* US4 (Indicação)
* US5 (Notificação Assegurado)
* US6 (Notificação Indicado)

**Should Have:**

* US3 (Recuperação de Senha)
* US7 (Painel Administrativo - visão geral)
* US10 (Visualização de histórico de indicações)


**Could Have:**

* US8 (Gerenciamento de Usuários - Admin)
* US9 (Gerenciamento de Indicações - Admin)

**Won't Have (MVP):**

* Nenhum item definido para esta categoria no MVP.
