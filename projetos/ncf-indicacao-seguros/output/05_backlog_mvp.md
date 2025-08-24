```markdown
# 05_backlog_mvp.md

## Funcionalidades (Épicos e User Stories)

**Épico 1: Cadastro e Login**

* User Story 1: Como um usuário, eu quero me cadastrar no aplicativo fornecendo minhas informações pessoais e criar uma conta, para que eu possa acessar os recursos do aplicativo.
* User Story 2: Como um usuário, eu quero fazer login no aplicativo usando meu nome de usuário e senha, para que eu possa acessar minha conta e informações.
* User Story 3: Como um usuário, eu quero recuperar minha senha caso eu a esqueça, para que eu possa continuar acessando minha conta.

**Épico 2: Indicação**

* User Story 4: Como um usuário (assegurando), eu quero indicar um amigo ou parente para o aplicativo, fornecendo seus dados de contato, para que ele possa receber um desconto e eu ganhe uma recompensa.
* User Story 5: Como um usuário (indicado), eu quero receber uma notificação push com informações sobre quem me indicou e os benefícios da indicação.
* User Story 6: Como um usuário (assegurando), eu quero receber uma notificação push confirmando que minha indicação foi aprovada e que o indicado recebeu um desconto.

**Épico 3: Administração**

* User Story 7: Como um administrador, eu quero visualizar relatórios de indicações, incluindo o número de indicações, aprovações e recompensas concedidas.
* User Story 8: Como um administrador, eu quero aprovar ou rejeitar indicações.
* User Story 9: Como um administrador, eu quero gerenciar os dados dos usuários, incluindo informações pessoais e histórico de indicações.

**Épico 4:  Fluxo do Indicado**

* User Story 10: Como um indicado, eu quero receber um e-mail/notificação após o cadastro, informando sobre o processo de aprovação da indicação.


## Critérios de Aceitação

* **User Story 1:** O cadastro deve incluir campos para nome completo, CPF, e-mail, telefone e senha. A senha deve atender a critérios de segurança (tamanho mínimo, caracteres especiais etc.).  Um e-mail de boas vindas deve ser enviado após o cadastro.
* **User Story 2:** O login deve ser realizado com sucesso usando as credenciais cadastradas.
* **User Story 3:** Um link para recuperação de senha deve ser enviado ao e-mail cadastrado.
* **User Story 4:** O formulário de indicação deve incluir campos para nome, CPF e telefone do indicado. Um e-mail de notificação de indicação deve ser enviado ao usuário.
* **User Story 5:** Uma notificação push deve ser enviada ao indicado contendo o nome do indicador e a oferta do desconto.
* **User Story 6:** Uma notificação push deve ser enviada ao indicador confirmando a aprovação da indicação.
* **User Story 7:** O relatório de indicações deve mostrar métricas relevantes em um dashboard claro e intuitivo.
* **User Story 8:** A aprovação/rejeição deve ser realizada com um sistema de controle de acesso e auditoria.
* **User Story 9:** A gestão de usuários deve permitir a edição e exclusão de perfis.
* **User Story 10:** O e-mail deve ser enviado automaticamente após a confirmação do cadastro e deve conter as informações de contato para dúvidas sobre o processo.

## Priorização (MoSCoW)

**Must have (M):**

* User Story 1 (Cadastro)
* User Story 2 (Login)
* User Story 4 (Indicação - Usuário Assegurado)
* User Story 5 (Notificação Indicado)
* User Story 8 (Aprovação/Rejeição de Indicação - Admin)

**Should have (S):**

* User Story 3 (Recuperação de Senha)
* User Story 6 (Notificação Indicador)
* User Story 7 (Relatório de Indicações)

**Could have (C):**

* User Story 9 (Gerenciamento de Usuários - Admin)
* User Story 10 (E-mail para o Indicado)

**Won't have (W):**

* Nenhum item definido para esta iteração MVP.

```
