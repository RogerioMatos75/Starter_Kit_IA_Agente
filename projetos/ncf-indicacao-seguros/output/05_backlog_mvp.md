## Funcionalidades (Épicos e User Stories)

**Épico 1: Cadastro e Login**

* US1: Como um usuário, desejo me cadastrar no aplicativo fornecendo minhas informações pessoais para poder acessar minhas funcionalidades.
* US2: Como um usuário, desejo fazer login no aplicativo utilizando meu e-mail e senha para acessar minhas informações e funcionalidades.
* US3: Como um usuário, desejo recuperar minha senha caso eu a esqueça para continuar utilizando o aplicativo.


**Épico 2: Sistema de Indicação**

* US4: Como um cliente atual (Asegurado), desejo indicar um amigo ou familiar para que ele receba um desconto e eu também ganhe um benefício.
* US5: Como um cliente atual (Asegurado), desejo visualizar o status das minhas indicações (aprovadas, pendentes, rejeitadas).
* US6: Como um indicado, desejo receber um push com as informações da pessoa que me indicou e o próximo passo para a aprovação do meu seguro.


**Épico 3: Notificações Push**

* US7: Como um cliente que indicou, desejo receber uma notificação push confirmando a aprovação da indicação.
* US8: Como um indicado, desejo receber uma notificação push com as informações sobre a indicação e o próximo passo para obter o desconto.


**Épico 4: Painel do Administrador**

* US9: Como um administrador, desejo acessar um painel para visualizar relatórios sobre as indicações, aprovações e descontos aplicados.
* US10: Como um administrador, desejo aprovar ou rejeitar indicações no sistema.


**Épico 5: Visualização de Informações**

* US11: Como um cliente (Asegurado), desejo visualizar informações da minha apólice de seguro.
* US12: Como um indicado, desejo visualizar informações sobre quem me indicou e os benefícios que posso receber.


**Épico 6: Aplicação de Descontos**

* US13: Como um sistema, desejo aplicar automaticamente o desconto ao indicado e ao cliente que indicou após a aprovação da indicação.


## Critérios de Aceitação

* **US1:** Campos de cadastro obrigatórios validados, senha com critérios de segurança, mensagem de sucesso após cadastro e redirecionamento para tela de login.
* **US2:** Validação de email e senha, mensagem de erro para credenciais inválidas, redirecionamento para tela inicial após login bem sucedido.
* **US3:** Opção para recuperação de senha via email, envio de email com link para redefinição de senha, redefinição de senha com validação.
* **US4:** Formulário para inserir dados do indicado, validação dos dados, confirmação de envio da indicação.
* **US5:** Tela para visualizar lista de indicações com status (aprovado, pendente, rejeitado).
* **US6:** Notificação push com informações sobre o indicador e instruções claras.
* **US7:** Notificação push contendo a confirmação da indicação e o valor do desconto recebido.
* **US8:** Notificação push com informações da indicação, próximos passos e possíveis documentos necessários.
* **US9:** Painel com gráficos e relatórios detalhados sobre as indicações e descontos, filtro por data, visualização de informações dos usuários.
* **US10:** Botão para aprovação/rejeição de indicações, atualização do status da indicação em tempo real.
* **US11:** Tela com informações detalhadas da apólice, número da apólice, data de vencimento, coberturas.
* **US12:** Tela com informações do indicador, valor do desconto e próximos passos para obter o benefício.
* **US13:** Desconto aplicado automaticamente após a aprovação da indicação, registro do desconto aplicado no sistema.


## Priorização (MoSCoW)

**Must have (Essencial):**

* US1 (Cadastro)
* US2 (Login)
* US4 (Criar Indicação)
* US6 (Notificação para Indicado)
* US7 (Notificação para Indicador)
* US10 (Aprovação/Rejeição de Indicação pelo Administrador)
* US13 (Aplicação de Desconto)


**Should have (Importante):**

* US3 (Recuperação de Senha)
* US5 (Visualizar Status da Indicação)
* US9 (Painel Administrativo - Relatórios)
* US11 (Visualizar informações da apólice)


**Could have (Desejável):**

* US8 (Detalhes da notificação para indicado)
* US12 (Visualizar detalhes da indicação - Indicado)


**Won't have (Não será feito no MVP):**

* Nenhum item definido para esta categoria neste MVP.

