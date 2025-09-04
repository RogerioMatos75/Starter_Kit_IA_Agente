## Funcionalidades (Épicos e User Stories)

**Épico 1: Indicação de Seguros**

* US1: Como um usuário, quero indicar um amigo para que ele possa receber um desconto no seguro.
* US2: Como um usuário, quero receber um desconto progressivo por cada amigo que eu indicar e contratar o seguro.
* US3: Como um usuário, quero receber uma notificação push quando um amigo que eu indique for aprovado.
* US4: Como um usuário indicado, quero receber uma notificação push informando quem me indicou e que um consultor entrará em contato.

**Épico 2: Painel Administrativo**

* US5: Como um administrador, quero visualizar todas as indicações realizadas.
* US6: Como um administrador, quero aprovar ou rejeitar uma indicação.
* US7: Como um administrador, quero enviar um link de proposta para o indicado.
* US8: Como um administrador, quero registrar a contratação do seguro pelo indicado.
* US9: Como um administrador, quero receber notificações push sobre novas indicações.
* US10: Como um administrador, quero gerar relatórios sobre o total de indicações, conversões e descontos concedidos.


**Épico 3: Autenticação e Segurança**

* US11: Como um usuário, quero me autenticar no aplicativo usando minhas credenciais.
* US12: Como um administrador, quero ter um login separado com permissões elevadas.

## Critérios de Aceitação

* **US1:** O formulário de indicação deve coletar nome, telefone e e-mail do indicado. O sistema deve validar se o indicado já existe.  Após o envio, o sistema deve confirmar o recebimento da indicação.
* **US2:** O desconto deve ser progressivo (1% por indicação válida, +1% por contratação). O desconto máximo anual é 10%. O sistema deve calcular e exibir o desconto corretamente.
* **US3:** O usuário que indicou deve receber uma notificação push após a aprovação da indicação e confirmação do desconto.
* **US4:** O usuário indicado deve receber uma notificação push com o nome de quem o indicou e a informação de que um consultor entrará em contato.
* **US5:** O painel administrativo deve exibir uma lista de todas as indicações com informações completas (quem indicou, quem foi indicado, status).
* **US6:** O administrador deve poder aprovar ou rejeitar indicações através de um botão no painel administrativo. O status da indicação deve ser atualizado em tempo real.
* **US7:** Ao aprovar a indicação, o administrador deve ter a opção de enviar um link de proposta para o indicado por e-mail.
* **US8:** Após a contratação, o administrador deve poder registrar esta informação no sistema.
* **US9:** O administrador deve receber uma notificação push para cada nova indicação.
* **US10:** Os relatórios devem conter filtros por data e permitir download em formato CSV.
* **US11:** O sistema deve usar um mecanismo de autenticação seguro (ex: JWT).
* **US12:** O login de administrador deve ter autenticação separada e acesso a funcionalidades restritas.


## Priorização (MoSCoW)

**Must have (M):**

* US1 (Indicação de amigo)
* US2 (Desconto progressivo)
* US3 (Notificação para o usuário que indicou)
* US4 (Notificação para o usuário indicado)
* US5 (Visualizar indicações no painel administrativo)
* US6 (Aprovar/rejeitar indicações)
* US11 (Autenticação de usuário)
* US12 (Login de administrador)

**Should have (S):**

* US7 (Enviar link de proposta)
* US8 (Registrar contratação)
* US9 (Notificações push para o administrador)


**Could have (C):**

* US10 (Relatórios administrativos)

**Won't have (W):**

*  Nenhuma funcionalidade definida para esta categoria no MVP.

