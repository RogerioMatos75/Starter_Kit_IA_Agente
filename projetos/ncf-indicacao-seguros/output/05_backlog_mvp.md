## Funcionalidades (Épicos e User Stories)

**Épico 1: Cadastro e Login**

*   US1: Como administrador, quero poder cadastrar novos usuários (Assegurados e Administradores) para gerenciar as contas.
*   US2: Como Assegurado, quero poder criar uma conta para usar o aplicativo.
*   US3: Como Assegurado, quero poder fazer login com minhas credenciais.
*   US4: Como administrador, quero poder fazer login com minhas credenciais.

**Épico 2: Indicação**

*   US5: Como Assegurado, quero indicar um amigo para receber um desconto no seguro.
*   US6: Como Assegurado, quero receber uma notificação push quando minha indicação for aprovada.
*   US7: Como Indicado, quero receber uma notificação push com os dados do Assegurado que me indicou e a informação de que um consultor entrará em contato.
*   US8: Como administrador, quero visualizar a lista de indicações e aprová-las ou rejeitá-las.

**Épico 3: Painel do Administrador**

*   US9: Como administrador, quero ter acesso a um painel para visualizar métricas do aplicativo (número de indicações, usuários, etc.).
*   US10: Como administrador, quero poder gerenciar os usuários do sistema.


**Épico 4: Fluxo de Convite para o Indicado**

*   US11: Como Indicado, quero receber um link ou código de convite para acessar a oferta especial.
*   US12: Como Indicado, quero poder aceitar a indicação e preencher os meus dados para solicitar o seguro.


## Critérios de Aceitação

*   **US1:** O sistema deve permitir o cadastro de usuários com diferentes perfis (Assegurado e Administrador), validando os campos obrigatórios.
*   **US2, US3, US4:** O sistema deve permitir o login com validação de credenciais (usuário e senha).
*   **US5:** O sistema deve permitir ao Assegurado inserir dados do amigo que será indicado, incluindo um campo para email ou telefone.
*   **US6:** O sistema deve enviar uma notificação push para o Assegurado quando a indicação for aprovada.
*   **US7:** O sistema deve enviar uma notificação push para o Indicado contendo o nome do Assegurado que o indicou, e a informação de que um consultor entrará em contato.
*   **US8:** O sistema deve apresentar ao administrador uma lista das indicações, com opção para aprovação ou rejeição de cada uma.
*   **US9:** O painel do administrador deve apresentar métricas relevantes como número de usuários, número de indicações, número de indicações aprovadas e rejeitadas.
*   **US10:** O administrador deve poder visualizar, editar e deletar usuários do sistema.
*   **US11:** O sistema deve gerar um link ou código único de convite para o Indicado, que o leve a uma tela de cadastro com pré-preenchimento de alguns campos.
*   **US12:** O sistema deve permitir que o Indicado finalize o seu cadastro com as informações necessárias para dar continuidade à solicitação do seguro.


## Priorização (MoSCoW)

**Must Have:**

*   US1 (Cadastro de Usuários)
*   US2 (Cadastro de Assegurado)
*   US3 (Login Assegurado)
*   US4 (Login Administrador)
*   US5 (Indicação de Amigo)
*   US6 (Notificação Push Assegurado - Aprovação)
*   US7 (Notificação Push Indicado)
*   US8 (Aprovação/Rejeição de Indicação pelo Administrador)


**Should Have:**

*   US9 (Painel Administrativo com métricas básicas)
*   US11 (Fluxo de Convite para Indicado - Link/Código)


**Could Have:**

*   US10 (Gerenciamento de Usuários pelo Administrador)
*   US12 (Cadastro do Indicado com pré-preenchimento)


**Won't Have (MVP):**

*   Nenhum item definido para o MVP.
