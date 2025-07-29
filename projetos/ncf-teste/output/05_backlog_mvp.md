# 05_backlog_mvp.md

## NCF-Teste - Backlog MVP

**Data:** 20/07/2025

**Versão:** 1.0


### Funcionalidades (Épicos e User Stories)

**Épico 1: Cadastro e Login**

* **US1:** Como um usuário, desejo me cadastrar no aplicativo fornecendo minhas informações pessoais (nome, email, senha) para poder acessar as funcionalidades.
* **US2:** Como um usuário, desejo logar no aplicativo utilizando meu email e senha cadastrados.
* **US3:** Como um usuário, desejo recuperar minha senha caso eu a esqueça.

**Épico 2: Indicar Seguro**

* **US4:** Como um indicador, desejo indicar um seguro para um amigo, fornecendo o nome e o telefone do indicado.
* **US5:** Como um indicador, desejo visualizar o histórico das minhas indicações, incluindo o status de cada uma.


**Épico 3: Gerenciar Indicações**

* **US6:** Como um indicador, desejo receber notificações push sobre o status das minhas indicações (aprovado/rejeitado).
* **US7:** Como um indicado, desejo receber uma notificação push com os dados de quem me indicou e a informação de que um consultor entrará em contato.

**Épico 4: Notificações Push**

* **US8:** Como um administrador, desejo enviar notificações push personalizadas para os usuários.


**Épico 5:  Painel do Administrador (MVP - Funcionalidades Básicas)**

* **US9:** Como administrador, desejo visualizar um painel com métricas gerais do aplicativo (número de usuários, indicações, etc.).

**Épico 6: Descontos (Para MVP - apenas visualização do desconto)**

* **US10:** Como um indicado, desejo visualizar o desconto oferecido após a aprovação da indicação.


### Critérios de Aceitação

* **US1:**  O cadastro deve validar o email e a senha (comprimento mínimo, caracteres especiais).  Um email de confirmação deve ser enviado.
* **US2:** O login deve validar as credenciais e redirecionar para a tela inicial.
* **US3:** A recuperação de senha deve enviar um email com instruções para redefinição.
* **US4:**  O sistema deve validar o número de telefone do indicado.
* **US5:** O histórico deve mostrar data da indicação, nome do indicado, status (pendente, aprovado, rejeitado).
* **US6:** As notificações push devem ser enviadas em tempo real.
* **US7:** A notificação para o indicado deve incluir o nome do indicador e uma breve mensagem.
* **US8:** O administrador deve poder selecionar o público-alvo da notificação e o conteúdo da mensagem.
* **US9:** O painel deve ser intuitivo e mostrar as principais métricas.
* **US10:**  O valor do desconto deve ser claramente exibido.


### Priorização (MoSCoW)

**Must have (M):** US1, US2, US4, US5, US7

**Should have (S):** US6, US8, US10

**Could have (C):** US3, US9

**Won't have (W):**  ---
