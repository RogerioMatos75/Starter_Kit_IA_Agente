# 05_backlog_mvp.md

## Funcionalidades (Épicos e User Stories)

**Épico 1: Cadastro e Login**

* **User Story 1:** Como um usuário, eu quero me cadastrar no aplicativo fornecendo minhas informações pessoais e de contato, para que eu possa acessar os recursos do aplicativo.
* **User Story 2:** Como um usuário, eu quero fazer login no aplicativo usando meu nome de usuário e senha, para que eu possa acessar minha conta e meus dados.
* **User Story 3:** Como um usuário, eu quero recuperar minha senha caso eu a esqueça, para que eu possa continuar acessando minha conta.

**Épico 2: Indicação de Seguros**

* **User Story 4:** Como um usuário, eu quero indicar um amigo ou parente para um seguro, fornecendo seus dados de contato, para que ele possa receber uma proposta.
* **User Story 5:** Como um usuário, eu quero acompanhar o status da minha indicação, para que eu saiba se meu amigo foi aprovado ou não.
* **User Story 6:** Como um usuário, eu quero receber uma notificação push quando uma indicação minha for aprovada, para que eu saiba que receberei o meu desconto.

**Épico 3:  Administração**

* **User Story 7:** Como um administrador, eu quero acessar um painel administrativo para visualizar relatórios de indicações e usuários.
* **User Story 8:** Como um administrador, eu quero gerenciar usuários e suas informações.
* **User Story 9:** Como um administrador, eu quero ter acesso a métricas chave do negócio.

**Épico 4: Notificações Push**

* **User Story 10:** Como um usuário que indicou, quero receber uma notificação push quando a minha indicação for aprovada.
* **User Story 11:** Como um usuário indicado, quero receber uma notificação push com os dados de quem me indicou e informando que um consultor entrará em contato.


## Critérios de Aceitação

* **User Story 1:** Campos de cadastro devem ser validados (nome, email, telefone, CPF). Cadastro deve gerar um email de boas vindas.
* **User Story 2:** Login deve validar usuário e senha.
* **User Story 3:** Sistema deve permitir o envio de link para redefinição de senha via email.
* **User Story 4:** Formulário de indicação deve coletar informações essenciais do indicado (nome, email, telefone).
* **User Story 5:**  Interface deve mostrar o status da indicação (pendente, aprovado, rejeitado).
* **User Story 6:** Notificação push deve conter informação sobre o desconto ganho.
* **User Story 7:** Painel administrativo deve conter gráficos e relatórios relevantes.
* **User Story 8:**  Funcionalidades de edição e exclusão de usuários.
* **User Story 9:** Métricas devem incluir número de usuários, indicações, aprovações e rejeições.
* **User Story 10:** Notificação deve informar o nome do usuário que indicou e o valor do desconto.
* **User Story 11:** Notificação deve conter nome do usuário que indicou e um breve texto informando contato de um consultor.

## Priorização (MoSCoW)

**Must have:**

* User Story 1 (Cadastro)
* User Story 2 (Login)
* User Story 4 (Indicação)
* User Story 10 (Notificação para quem indicou)
* User Story 11 (Notificação para indicado)

**Should have:**

* User Story 3 (Recuperação de senha)
* User Story 5 (Acompanhamento de indicação)
* User Story 7 (Painel administrativo básico)

**Could have:**

* User Story 6 (Notificação push aprovação)
* User Story 8 (Gerenciamento de usuários)
* User Story 9 (Métricas administrativas)

**Won't have (para o MVP):**

* Nenhum item definido para esta categoria no MVP.
