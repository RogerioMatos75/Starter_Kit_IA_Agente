## Regras de Negócio

* Um cliente (assegurando) pode indicar amigos e parentes para contratar seguros.
* A indicação precisa ser aprovada para que o cliente e o indicado recebam benefícios.
* O cliente que indica recebe um desconto (a ser definido) por cada indicação aprovada.
* O indicado recebe um benefício (a ser definido) por ser indicado.
* O sistema deve registrar todas as indicações, seu status (pendente, aprovado, rejeitado) e os benefícios concedidos.
* O administrador do sistema tem acesso completo a todos os dados e funcionalidades.

## Requisitos Funcionais

* Cadastro e login de usuários (assegurando e administrador).
* Tela para o Assegurado realizar indicações (inserindo dados do indicado).
* Sistema de notificações push para o Assegurado e o Indicado.
* Tela para o administrador visualizar relatórios de indicações e gerenciar usuários.
* Fluxo de aprovação/rejeição de indicações pelo administrador.
* Integração com sistema de seguros para validação da contratação do indicado.
* Gestão de descontos para o Assegurado que realiza indicações.
* Gerenciamento de benefícios para os Indicados.
* Sistema de busca e filtro para o administrador.


## Requisitos Não Funcionais

* Alta disponibilidade e performance do sistema.
* Segurança dos dados dos usuários (criptografia, autenticação forte).
* Interface intuitiva e amigável para todos os usuários.
* Escalabilidade para lidar com um grande número de usuários e indicações.
* Compatibilidade com dispositivos móveis (Android e iOS).
* Resposta rápida a notificações push.
* Conformidade com leis e regulamentos de privacidade de dados (LGPD).


## Personas de Usuário

* **Assegurado:** Cliente atual da seguradora que realiza indicações.
* **Indicado:** Pessoa indicada por um Assegurado para contratar um seguro.
* **Administrador:** Usuário com privilégios administrativos para gerenciar o sistema.


## Fluxos de Usuário

* **Fluxo de Indicação:** Assegurado acessa o aplicativo, insere os dados do Indicado, envia a indicação. O administrador aprova ou rejeita.  Notificações são enviadas ao Assegurado e ao Indicado.
* **Fluxo de Administração:** Administrador acessa o aplicativo, visualiza relatórios, aprova/rejeita indicações, gerencia usuários.
* **Fluxo de Login:** Usuários (Assegurado e Administrador) realizam login com credenciais seguras.
* **Fluxo de Cadastro:** Usuários (Assegurado e Administrador) realizam cadastro fornecendo as informações necessárias.


<br>
<hr>
<br>

### 🧠 Instruções para o Agente de Desenvolvimento

**📝 Prompt Complementar:**
Este documento define os requisitos para um MicroSaaS de indicação de seguros, focando na conexão entre asegurados e potenciais clientes. A próxima fase de desenvolvimento deve se concentrar na construção de um MVP (Minimum Viable Product) altamente específico, validando as funcionalidades essenciais com um pequeno grupo de usuários-alvo (assegurados).  O objetivo é comprovar a viabilidade do modelo de indicação e iterar rapidamente com base no feedback recebido, antes de expandir para funcionalidades mais complexas.

**👍 Instruções Positivas:**
Mapeie um problema altamente específico de um nicho dentro do mercado de seguros, focando em um tipo particular de seguro (ex: seguro auto, seguro residencial) para validar a dor com poucos usuários asegurados. Priorize a implementação do fluxo de indicação, incluindo o cadastro de asegurados e indicados, o envio da indicação, a aprovação/rejeição pelo administrador e o sistema de notificações.  Implemente apenas as funcionalidades essenciais que entreguem valor imediato aos asegurados, como o desconto por indicação aprovada.  Concentre-se em uma interface intuitiva e amigável para o asegurados, facilitando o processo de indicação.  Utilize uma arquitetura escalável, mesmo que simples, para acomodar o crescimento futuro, sem comprometer a velocidade de desenvolvimento do MVP.  Priorize a segurança dos dados, utilizando boas práticas de autenticação e criptografia, mesmo que em uma escala reduzida.

**👎 Instruções Negativas:**
Evite implementar recursos complexos de relatórios e dashboards administrativos neste estágio inicial. Nada de integração com sistemas de seguros externos antes de validar o core do fluxo de indicação.  Não implemente funcionalidades para múltiplos tipos de seguros, diferentes tipos de benefícios, ou funcionalidades para o indicado além do recebimento de notificações.  Evite criar um sistema de gerenciamento de usuários muito robusto, focando em um sistema simples e funcional para o MVP.  Não se preocupe com a compatibilidade com todos os dispositivos móveis (Android e iOS) inicialmente.  Foque em um único dispositivo como base para o teste inicial do MVP.  Não gaste tempo com funcionalidades de busca e filtro sofisticadas para o administrador.  Evite  implementar qualquer recurso que não tenha sido validado com um pequeno grupo de usuários-alvo.


--- REFINAMENTO DO ARCHON AI ---

Sim.  O manifesto é claro e prioriza corretamente a construção de um MVP validável.  A definição de escopo, focando no fluxo de indicação e descartando funcionalidades secundárias, é adequada para a fase inicial.  O foco em um nicho de seguro e a iteração rápida com base em feedback são estratégias válidas.
