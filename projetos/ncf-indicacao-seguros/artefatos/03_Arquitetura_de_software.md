## Regras de Negócio

* **Indicação:**  Um cliente (Indicação) pode indicar outro cliente (Indicado) para adquirir um seguro.
* **Aprovação:** A indicação precisa ser aprovada pela NCF Indicação Seguros para que o cliente que indicou e o indicado recebam os benefícios.  A aprovação envolve a verificação dos dados do indicado e a efetiva contratação do seguro pelo indicado.
* **Desconto:**  Tanto o cliente que indicou (Indicação) quanto o indicado recebem um desconto no seguro. A porcentagem do desconto deve ser definida e configurada na plataforma.
* **Notificação:** Ao aprovar a indicação, tanto a Indicação quanto o Indicado recebem uma notificação push. A notificação para a Indicação parabeniza pela indicação bem-sucedida. A notificação para o Indicado inclui informações sobre quem o indicou e a promessa de contato de um consultor.
* **Consultor:** Após a aprovação da indicação, um consultor da NCF Indicação Seguros deve entrar em contato com o Indicado.
* **Cadastro:** O indicado precisa ter um cadastro completo e aprovado na plataforma.
* **Limite de Indicações:**  Pode haver um limite de indicações por cliente (Indicação) em um determinado período, este limite deve ser configurado na plataforma.
* **Identificação:**  A plataforma deve manter um registro claro da relação entre Indicação e Indicado, com a data da indicação e o status da aprovação.


## Restrições

* **Dados do Indicado:**  A informação fornecida pelo Indicado na indicação deve ser precisa e validada pela NCF Indicação Seguros. Dados inconsistentes ou inválidos podem impedir a aprovação da indicação.
* **Validação de Cadastro:** O cadastro do indicado deve atender a todos os requisitos definidos pela NCF Indicação Seguros.
* **Integração com Sistema de Seguros:** A plataforma precisa se integrar com o sistema de seguros da NCF para processar as informações de contratação e aplicar os descontos.
* **Disponibilidade do Consultor:** A garantia de um retorno do consultor ao indicado dentro de um tempo hábil deve ser considerada.

## Exceções

* **Indicação Rejeitada:** Caso a indicação seja rejeitada, tanto a Indicação quanto o Indicado devem ser notificados com o motivo da rejeição.
* **Erro na Notificação:**  O sistema deve ter mecanismos de tratamento de erros para garantir que as notificações push sejam entregues corretamente. Caso contrário, deve existir um mecanismo de reenvio.
* **Falha na Integração:**  Se houver falha na integração com o sistema de seguros, a indicação deve ser colocada em um estado de pendência, e um alerta deve ser gerado para a equipe de administração.
* **Consultor Indisponível:**  Deve haver um protocolo para lidar com situações onde o consultor não consegue entrar em contato com o indicado dentro do prazo estabelecido.

## Decisões

* **Tecnologia:** A tecnologia para desenvolvimento do aplicativo será definida em outra etapa do projeto.
* **Design da Interface:** O design da interface do usuário será definido após a aprovação das regras de negócio.
* **Metodologia de Desenvolvimento:** A metodologia de desenvolvimento será definida em outra etapa do projeto.
* **Sistema de Notificações:** O sistema de notificações push será integrado com um provedor externo.
* **Plataforma de Administração:** Uma plataforma de administração será desenvolvida para monitorar as indicações, aprovações, descontos e relatórios.


<br>
<hr>
<br>

### 🧠 Instruções para o Agente de Desenvolvimento

**📝 Prompt Complementar:**
Este documento define as regras de negócio, restrições, exceções e decisões iniciais para o desenvolvimento do MicroSaaS de indicação de seguros da NCF.  A próxima fase de desenvolvimento deve focar na implementação de uma arquitetura robusta, porém simples e escalável, que suporte as funcionalidades essenciais descritas, permitindo um lançamento rápido e iterativo do MVP.  O foco deve ser na implementação das regras de negócio e na integração com o sistema de seguros da NCF, priorizando a estabilidade e a facilidade de manutenção.

**👍 Instruções Positivas:**
Implemente uma estrutura monolítica leve utilizando uma linguagem e framework adequados para o desenvolvimento ágil e rápido.  Priorize a simplicidade e clareza do código, com um backend direto ao ponto e focado nas regras de negócio definidas.  A aplicação deve ser projetada para escalabilidade horizontal, permitindo a adição de recursos de computação conforme necessário, sem exigir uma complexa infraestrutura de microsserviços.  Utilize um banco de dados relacional para facilitar o gerenciamento dos dados de indicações, clientes e seguros.  Implemente robustas validações de dados para garantir a integridade da informação e o funcionamento correto do sistema, conforme definido nas restrições.  Inclua tratamento de exceções e mecanismos de logging para facilitar a monitoração e a resolução de problemas.  Incorpore um sistema de notificações push confiável e eficiente, utilizando um serviço externo como provedor, garantindo o reenvio de mensagens em caso de falha.  Desenvolva uma interface administrativa simples e intuitiva para monitorar as indicações, aprovações, descontos e gerar relatórios.  Considere a utilização de testes unitários e de integração para garantir a qualidade do código.

**👎 Instruções Negativas:**
Não utilize microsserviços a menos que haja uma justificativa clara e comprovada necessidade. Evite a utilização de frameworks pesados ou complexos que possam dificultar o desenvolvimento e a manutenção.  Não implemente funcionalidades além do escopo mínimo viável (MVP) definido neste documento.  Não utilize tecnologias ou infraestruturas que exijam um DevOps complexo ou especializado.  Não deixe de implementar mecanismos robustos de tratamento de erros e exceções.  Não negligencie a segurança da aplicação e dos dados.  Não construa uma solução com alta dependência de integrações externas sem mecanismos de fallback e monitoramento robustos.  Evite implementar uma interface de usuário complexa e desnecessária na primeira versão.  Não complique a estrutura de dados, focando em simplicidade e facilidade de manutenção.


--- REFINAMENTO DO ARCHON AI ---

O documento está bem estruturado, mas carece de detalhes técnicos cruciais para a implementação.  Sugiro adicionar:

* **Especificação da arquitetura de dados:**  Modelo de dados detalhado incluindo tabelas, campos e relacionamentos (relacionamento entre Indicação e Indicado, status da indicação, etc.).
* **Fluxo de aprovação:** Diagrama de fluxo detalhando as etapas de aprovação de uma indicação, incluindo os pontos de decisão e as ações tomadas em cada etapa.
* **Esboço da API:** Descrição das APIs (endpoints, métodos, parâmetros, respostas) para as principais funcionalidades, incluindo a integração com o sistema de seguros.
* **Critérios de aceitação:**  Definição clara dos critérios de aceite para cada funcionalidade do MVP.
* **Tecnologias propostas:** Sugestão específica de linguagem de programação, framework backend e banco de dados, justificando a escolha.

A priorização de um MVP monolítico é adequada, porém a escalabilidade horizontal precisa ser considerada na escolha da tecnologia de banco de dados e na arquitetura da aplicação (considerar o uso de filas de mensagens para lidar com a alta demanda de notificações).
