## Fluxos de Usuário

**Fluxo 1: Usuário indica um amigo (Assegurado)**

1. Usuário acessa a seção "Indique um Amigo" no aplicativo.
2. Usuário insere os dados do amigo (nome, telefone, email).
3. Usuário confirma a indicação.
4. Sistema envia notificação push para o usuário confirmando o recebimento da indicação.
5. Sistema envia notificação push para o amigo indicado com os dados do usuário que o indicou e a informação de que um consultor entrará em contato.
6. Consultor entra em contato com o amigo indicado.
7. Se o amigo indicado for aprovado, o usuário recebe uma notificação push de recompensa.


**Fluxo 2: Amigo Indicado (Novo Usuário)**

1. Amigo indicado recebe notificação push com os dados do usuário que o indicou.
2. Amigo indicado acessa o aplicativo através do link na notificação push ou diretamente.
3. Amigo indicado preenche o formulário de cadastro.
4. Amigo indicado conclui o processo de cadastro e aprovação do seguro.

**Fluxo 3: Administrador**

1. Administrador acessa o painel administrativo.
2. Administrador visualiza relatórios de indicações.
3. Administrador gerencia usuários.
4. Administrador monitora o processo de aprovação de novos usuários.
5. Administrador configura as campanhas de incentivo.



## Navegação

**Assegurado:**

* Tela inicial
* Seção "Indique um Amigo"
* Tela de inserção de dados do indicado
* Tela de confirmação de indicação
* Notificações Push

**Indicado:**

* Tela inicial (após clicar no link da notificação)
* Tela de cadastro
* Tela de aprovação do seguro

**Administrador:**

* Tela de login
* Painel administrativo (dashboard)
* Relatórios de indicações
* Gerenciamento de usuários
* Configuração de campanhas


## Interações

**Assegurado:**

* **Ação:** Clicar em "Indique um Amigo".
* **Resposta:** Abre a tela de inserção de dados do indicado.
* **Ação:** Inserir dados do amigo.
* **Resposta:** Validação dos dados.
* **Ação:** Confirmar indicação.
* **Resposta:** Notificação push de confirmação e envio de notificação para o indicado.

**Indicado:**

* **Ação:** Clicar no link da notificação.
* **Resposta:** Abre a tela inicial do aplicativo.
* **Ação:** Preencher o formulário de cadastro.
* **Resposta:** Validação dos dados.
* **Ação:** Enviar formulário.
* **Resposta:** Notificação de aprovação ou rejeição.

**Administrador:**

* **Ação:** Acessar o painel administrativo.
* **Resposta:** Dashboard com métricas.
* **Ação:** Visualizar relatórios.
* **Resposta:** Exibição de relatórios detalhados.
* **Ação:** Gerenciar usuários.
* **Resposta:** Acesso às informações e ações sobre os usuários.


<br>
<hr>
<br>

### 🧠 Instruções para o Agente de Desenvolvimento

**📝 Prompt Complementar:**
Este documento define os fluxos de usuário, navegação e interações para a feature central do MicroSaaS: o sistema de indicação de amigos. A próxima fase do desenvolvimento deve focar na implementação desta feature específica, priorizando simplicidade e escalabilidade para o futuro, mantendo a arquitetura leve e eficiente própria de um MicroSaaS.  A entrega de um MVP funcional desta funcionalidade é o objetivo principal, permitindo validação rápida e iteração com os usuários.


**👍 Instruções Positivas:**
Foque em entregar uma única feature central, o sistema de indicação, com endpoints RESTful claros e concisos (para cada ação descrita nas interações), utilizando um banco de dados simples como PostgreSQL ou SQLite.  Priorize a lógica de negócio diretamente relacionada ao fluxo de indicações, incluindo validação de dados, envio de notificações push (utilizando uma solução como Firebase Cloud Messaging ou similar), e a geração de relatórios básicos para o administrador.  Implemente apenas as telas e funcionalidades descritas na seção "Navegação", evitando funcionalidades adicionais neste momento.  Utilize uma arquitetura de microsserviços, se aplicável, focando em um único serviço para esta funcionalidade, com código limpo, bem documentado e testável. A prioridade é a entrega funcional da feature, com espaço para melhorias e expansões em iterações futuras.


**👎 Instruções Negativas:**
Evite a implementação de funcionalidades além do sistema de indicação de amigos descrito neste documento.  Não crie módulos ou componentes genéricos para futuras funcionalidades.  Evite a utilização de bancos de dados complexos ou frameworks pesados desnecessários para esta fase inicial do projeto.  Não implemente integrações com outros sistemas ou serviços externos neste momento, a menos que sejam absolutamente críticos para a funcionalidade principal.  Não crie um sistema de autenticação complexo, utilize uma solução simples e eficaz para esta versão MVP.  Evite a implementação de um sistema de relatórios completo e sofisticado; concentre-se em relatórios básicos para monitoramento do sistema de indicação.  Não sobrecarregue a aplicação com features extras que possam comprometer a entrega da feature principal e o foco no MVP.


--- REFINAMENTO DO ARCHON AI ---

Checklist:

* **Funcionalidades:** Foco apenas no sistema de indicação de amigos.  Funcionalidades extras foram excluídas?
* **Arquitetura:** Arquitetura de microsserviços aplicada?  Um único serviço para a funcionalidade?
* **Banco de Dados:** PostgreSQL ou SQLite utilizado? Bancos de dados complexos evitados?
* **Endpoints:** Endpoints RESTful definidos para cada ação?
* **Notificações Push:** Solução como Firebase Cloud Messaging ou similar implementada?
* **Relatórios:** Relatórios básicos para o administrador implementados? Relatórios complexos evitados?
* **Autenticação:** Solução de autenticação simples e eficaz implementada?
* **Validação de Dados:** Validação de dados implementada em todos os fluxos?
* **Testes:** Código limpo, bem documentado e testável?
* **MVP:** Entrega funcional da feature principal priorizada?

