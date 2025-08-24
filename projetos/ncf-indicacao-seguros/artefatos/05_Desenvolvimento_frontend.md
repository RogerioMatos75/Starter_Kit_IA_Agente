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

<br>
<hr>
<br>

### 🧠 Instruções para o Agente de Desenvolvimento

**📝 Prompt Complementar:**
Este documento define as funcionalidades mínimas viáveis (MVP) para o frontend do nosso MicroSaaS de indicação, focando no cadastro, login e fluxo de indicação.  A próxima fase de desenvolvimento deve se concentrar na implementação da interface do usuário, priorizando a clareza, simplicidade e usabilidade para garantir uma experiência otimizada para o usuário, levando em conta a natureza enxuta e escalável de um MicroSaaS. A priorização dos itens "Must Have" deste documento é crucial para o lançamento inicial do MVP.

**👍 Instruções Positivas:**
Interface simples e intuitiva, com foco no CTA principal (Cadastro e Indicação).  Priorize a acessibilidade (conformidade com WCAG), carregamento rápido da página, uso de componentes leves e responsividade para diferentes tamanhos de tela. Utilize apenas as bibliotecas essenciais para garantir performance otimizada.  O design deve refletir a simplicidade e eficiência esperadas de um MicroSaaS. Implemente mecanismos de feedback ao usuário em cada etapa do processo, incluindo mensagens de sucesso ou erro claras e concisas.  As notificações push devem ser implementadas de forma não intrusiva e respeitosa à experiência do usuário.

**👎 Instruções Negativas:**
Não use frameworks de UI pesados como Angular Material ou React Bootstrap integralmente.  Evite animações complexas ou elementos visuais desnecessários que possam afetar o desempenho.  Não implemente múltiplas páginas ou fluxos de navegação complexos, a menos que absolutamente necessário para as funcionalidades MVP.  Não inclua funcionalidades de personalização ou configurações avançadas nesta etapa.  Evite bibliotecas de terceiros desnecessárias que possam aumentar o tamanho do bundle e comprometer a performance.  Não implemente recursos que não estejam explicitamente definidos como "Must have" neste documento para o MVP.  A interface deve ser concisa e focada na tarefa principal.


--- REFINAMENTO DO ARCHON AI ---

Esta etapa é crucial para validar o core do negócio (indicacão) e o fluxo de usuários, permitindo iterações rápidas com base em feedback real antes de investir em funcionalidades adicionais.  O foco no MVP assegura um lançamento rápido, minimizando riscos e maximizando o aprendizado com o mínimo de recursos.
