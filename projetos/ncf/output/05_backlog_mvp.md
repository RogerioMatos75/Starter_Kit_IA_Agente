# 05_backlog_mvp.md

## Funcionalidades (Épicos e User Stories)

**Épico 1: Cadastro e Login**

* **User Story 1:** Como um usuário, quero me cadastrar no aplicativo fornecendo minhas informações pessoais, para poder acessar as funcionalidades.
* **User Story 2:** Como um usuário, quero fazer login no aplicativo usando meu e-mail e senha, para acessar minha conta.
* **User Story 3:** Como um usuário, quero recuperar minha senha caso a esqueça, para poder acessar minha conta.


**Épico 2: Indicação de Seguros**

* **User Story 4:** Como um indicador, quero indicar um seguro para um amigo, fornecendo os dados do indicado, para que ele receba a oferta.
* **User Story 5:** Como um indicador, quero acompanhar o status das minhas indicações, para saber se foram aprovadas ou não.

**Épico 3: Gerenciamento de Indicações**

* **User Story 6:** Como um indicador, quero visualizar o histórico das minhas indicações, incluindo data, status e recompensas recebidas.
* **User Story 7:** Como um indicado, quero visualizar a indicação recebida, incluindo os dados do indicador e detalhes do seguro.

**Épico 4: Notificações Push**

* **User Story 8:** Como um indicador, quero receber uma notificação push quando uma indicação for aprovada.
* **User Story 9:** Como um indicado, quero receber uma notificação push quando receber uma indicação de seguro, contendo informações sobre o indicador.


**Épico 5:  Administração (Painel Administrativo)**

* **User Story 10:** Como administrador, quero visualizar relatórios de indicações, para monitorar o desempenho do aplicativo.
* **User Story 11:** Como administrador, quero gerenciar usuários, incluindo cadastro, edição e exclusão.


**Épico 6:  Descontos**

* **User Story 12:** Como um indicado, quero visualizar o desconto oferecido na indicação recebida.
* **User Story 13:** Como um indicado, quero aplicar o desconto no momento da contratação do seguro.


## Critérios de Aceitação

* **User Story 1:** O cadastro deve validar os campos obrigatórios e permitir o cadastro apenas com dados válidos.  Um email de confirmação deve ser enviado.
* **User Story 2:** O login deve validar as credenciais do usuário.
* **User Story 3:** O sistema deve enviar um email com instruções para a recuperação da senha.
* **User Story 4:** O sistema deve registrar a indicação e enviar uma notificação para o indicado.
* **User Story 5:** O sistema deve exibir o status da indicação (pendente, aprovada, rejeitada).
* **User Story 6:**  A interface deve exibir as indicações de forma clara e organizada, incluindo data, status e recompensas.
* **User Story 7:** A interface deve exibir os dados do indicador e os detalhes do seguro indicado de forma clara e concisa.
* **User Story 8:** A notificação deve conter informações sobre a indicação aprovada.
* **User Story 9:** A notificação deve conter o nome do indicador e os detalhes da oferta do seguro.
* **User Story 10:** O painel deve fornecer relatórios sobre o número de indicações, aprovações, rejeições e outros dados relevantes.
* **User Story 11:** O sistema deve permitir a criação, edição e exclusão de usuários com controle de acesso adequado.
* **User Story 12:** O desconto deve ser claramente exibido na interface do indicado.
* **User Story 13:** O sistema deve integrar-se com o sistema de seguros para aplicar o desconto automaticamente.


## Priorização (MoSCoW)

**Must have:**

* User Story 1 (Cadastro)
* User Story 2 (Login)
* User Story 4 (Indicar Seguro)
* User Story 7 (Visualizar Indicação - Indicado)
* User Story 8 (Notificação Push - Indicador - Aprovação)
* User Story 9 (Notificação Push - Indicado)


**Should have:**

* User Story 3 (Recuperação de Senha)
* User Story 5 (Acompanhar Status da Indicação)
* User Story 12 (Visualizar Desconto)


**Could have:**

* User Story 6 (Histórico de Indicações)
* User Story 10 (Relatórios Administrativos)
* User Story 11 (Gerenciamento de Usuários - Admin)
* User Story 13 (Aplicação de Desconto)


**Won't have (MVP):**

* Nenhuma funcionalidade no MVP.  Estas serão consideradas em versões futuras.
