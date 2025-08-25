## Fluxos de Usuário

**Fluxo 1: Indicação de um novo cliente por um Asegurado**

1. O Asegurado acessa o aplicativo NCF e navega até a seção "Indique um Amigo".
2. O Asegurado preenche os dados do indicado (nome, telefone e e-mail).
3. O sistema valida os dados inseridos.
4. O Asegurado confirma a indicação.
5. O sistema envia uma notificação push para o Asegurado confirmando o recebimento da indicação.
6. O sistema envia uma notificação push para o indicado com as informações do Asegurado que o indicou e instruções para o próximo passo.

**Fluxo 2: Processo do Indicado**

1. O Indicado recebe a notificação push e acessa o aplicativo NCF (ou um link direcionado para o cadastro).
2. O Indicado realiza o cadastro ou login na plataforma.
3. O Indicado visualiza os detalhes da indicação, incluindo o nome do Asegurado que o indicou.
4. O Indicado prossegue com o processo de solicitação de seguro.
5. O Indicado recebe retorno do consultor após a aprovação do seguro.


**Fluxo 3: Monitoramento do Administrador**

1. O Administrador acessa o painel administrativo do aplicativo NCF.
2. O Administrador visualiza relatórios sobre as indicações, incluindo o número de indicações, aprovações e descontos aplicados.
3. O Administrador pode filtrar e segmentar os dados para análise mais detalhada.
4. O Administrador pode aprovar ou rejeitar indicações.
5. O Administrador pode gerenciar as configurações do programa de indicações.


## Navegação

**Asegurado:** Tela inicial > Indique um amigo > Preenchimento de dados do indicado > Confirmação da indicação > Visualização de status das indicações.

**Indicado:** Notificação Push > Tela de detalhes da indicação > Cadastro/Login > Preenchimento de dados para solicitação de seguro.

**Administrador:** Tela de login administrativa > Dashboard de relatórios > Filtros e segmentação de dados > Detalhes de indicações individuais > Gerenciamento de configurações.


## Interações

**Asegurado:** Inserir dados do indicado, confirmar indicação, visualizar status de indicações, receber notificações push.

**Indicado:** Receber notificações push, visualizar informações da indicação, realizar cadastro/login, preencher formulário de solicitação de seguro.

**Administrador:** Visualizar relatórios, filtrar dados, aprovar/rejeitar indicações, gerenciar configurações do sistema, receber notificações sobre status das indicações.

<br>
<hr>
<br>

### 🧠 Instruções para o Agente de Desenvolvimento

**📝 Prompt Complementar:**
Este documento define os fluxos de usuário, navegação e interações para a funcionalidade de indicação de clientes no MicroSaaS NCF.  A próxima fase de desenvolvimento deve focar na implementação da feature central de indicação, priorizando simplicidade, escalabilidade e manutenabilidade para este MicroSaaS, assegurando a integração perfeita com os sistemas de notificação push e o painel administrativo.  A entrega deve ser um MVP funcional, permitindo testes e iterações futuras.

**👍 Instruções Positivas:**
Foque em entregar uma única feature central – o sistema de indicação de clientes – com endpoints RESTful claros e concisos, utilizando um banco de dados simples (como PostgreSQL ou MySQL) e uma lógica de negócio enxuta e fácil de manter. Implemente notificações push como uma integração com um serviço externo (ex: Firebase Cloud Messaging).  Priorize a testabilidade de cada componente, incluindo testes unitários e de integração.  O painel administrativo deve ser minimalista e focado na visualização dos dados essenciais do sistema de indicações.  Documente a API RESTful de forma clara e concisa, utilizando Swagger ou similar.

**👎 Instruções Negativas:**
Evite a criação de um sistema complexo e sobre-engenheirado.  Não implemente funcionalidades adicionais além do core do sistema de indicações (ex: gerenciamento de usuários completo, autenticação complexa,  funcionalidades de relatório elaboradas).  Não utilize frameworks ou bibliotecas desnecessários que possam comprometer a simplicidade e a manutenibilidade do código.  Evite a criação de múltiplos módulos ou serviços independentes para esta feature; a prioridade é a simplicidade e a entrega rápida.  Não implemente lógica genérica que possa ser utilizada em outras áreas do sistema sem a confirmação clara de necessidade para esta versão MVP do MicroSaaS.
