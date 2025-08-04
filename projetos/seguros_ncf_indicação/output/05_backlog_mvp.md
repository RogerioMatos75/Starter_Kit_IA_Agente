## Funcionalidades (Épicos e User Stories)

**Épico 1: Cadastro e Login**

*   **US1:** Como um novo usuário, eu quero me cadastrar no aplicativo fornecendo minhas informações pessoais e de contato, para que eu possa acessar os recursos do aplicativo.
*   **US2:** Como um usuário cadastrado, eu quero poder fazer login no aplicativo usando meu nome de usuário e senha, para que eu possa acessar minhas informações e funcionalidades.
*   **US3:** Como um usuário, eu quero recuperar minha senha caso eu a esqueça, para que eu possa continuar a usar o aplicativo.


**Épico 2: Indicação**

*   **US4:** Como um cliente atual (assegurado), eu quero poder indicar um amigo ou familiar para o seguro, para que ele possa receber um desconto e eu também.
*   **US5:** Como um cliente atual (assegurado), eu quero receber um código de indicação único para compartilhar, para facilitar o processo de indicação.
*   **US6:** Como um indicado, eu quero receber informações claras sobre a indicação e o desconto oferecido, para que eu possa decidir se quero contratar o seguro.

**Épico 3: Notificações Push**

*   **US7:** Como um cliente que indicou, eu quero receber uma notificação push confirmando que minha indicação foi aprovada, para que eu saiba que vou receber meu desconto.
*   **US8:** Como um indicado, eu quero receber uma notificação push com informações sobre quem me indicou e um contato para prosseguir com o processo de contratação do seguro.

**Épico 4: Administração**

*   **US9:** Como administrador, eu quero acessar um painel administrativo com relatórios e dados sobre as indicações, para monitorar o desempenho do programa.
*   **US10:** Como administrador, eu quero aprovar ou rejeitar as indicações, para garantir a integridade do programa.


**Épico 5: Visualização de Informações**

*   **US11:** Como um cliente (assegurado), eu quero visualizar as informações da minha apólice de seguro, para que eu tenha fácil acesso aos detalhes do meu seguro.
*   **US12:** Como um cliente (assegurado), eu quero visualizar o status das minhas indicações (pendentes, aprovadas, rejeitadas), para monitorar o andamento das minhas indicações.
*   **US13:** Como um indicado, eu quero visualizar os detalhes da indicação, incluindo informações sobre o cliente que me indicou.


**Épico 6: Aplicação de Desconto**

*   **US14:** Como sistema, eu quero aplicar o desconto automaticamente para o cliente que indicou e para o indicado, após a aprovação da indicação.


## Critérios de Aceitação

*   **US1:** Campos de cadastro com validações, armazenamento seguro das informações e sucesso no login após cadastro.
*   **US2:** Login com validação de credenciais e redirecionamento para tela inicial após login bem-sucedido.
*   **US3:** Fluxo de recuperação de senha com envio de email ou SMS.
*   **US4:** Geração de um código de indicação único e compartilhamento através de meios como email ou SMS.
*   **US5:** Registro da indicação no sistema e visualização do status da indicação pelo usuário.
*   **US6:** Notificação com informações do cliente que indicou e instruções claras.
*   **US7:** Notificação push enviada para o cliente que indicou assim que a indicação for aprovada.
*   **US8:** Notificação push para o indicado com detalhes do indicador e instruções sobre os próximos passos.
*   **US9:** Painel administrativo com gráficos e tabelas, com filtros e ordenação dos dados.
*   **US10:** Interface de aprovação/rejeição com justificativa para rejeições.
*   **US11:** Tela com informações essenciais da apólice em formato legível.
*   **US12:** Tela de status das indicações com filtros e ordenação.
*   **US13:** Tela com informações do indicador, código de indicação e status da indicação.
*   **US14:** Desconto aplicado corretamente no valor final da apólice para o indicado e creditado para o indicador.


## Priorização (MoSCoW)

**Must have (Essencial):** US1, US2, US4, US6, US7, US8, US9, US14

**Should have (Importante):** US3, US5, US11, US13

**Could have (Desejável):** US10, US12

**Won't have (Não Essencial para o MVP):**  Nenhum no momento.
