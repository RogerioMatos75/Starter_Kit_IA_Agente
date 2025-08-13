## Regras de Negócio

* **Indicação:** Um cliente (Indicação) pode indicar um novo cliente (Indicado) para a NCF Indicação Seguros.
* **Aprovação:** A indicação só será considerada válida após a aprovação do Indicado pela NCF Indicação Seguros.  A aprovação implica na efetivação de uma apólice de seguros.
* **Desconto:** Após a aprovação do Indicado, o cliente que fez a indicação (Indicação) receberá um desconto pré-definido em sua próxima renovação de apólice. O valor do desconto será definido pela empresa e pode variar ao longo do tempo.
* **Notificação:** Após a aprovação do Indicado, ambos receberão uma notificação *push*: o Indicação receberá uma notificação de sucesso da indicação, e o Indicado receberá uma notificação com os dados do Indicação e a informação de que um consultor entrará em contato em breve.
* **Cadastro Indicado:** O indicado precisará cadastrar-se completamente na plataforma, fornecendo todas as informações necessárias para a análise de risco e emissão da apólice. Informações incompletas podem levar à reprovação da indicação.
* **Consultor:** Um consultor entrará em contato com o Indicado após a aprovação da sua indicação para dar andamento ao processo de contratação do seguro.
* **Limite de Indicação:**  Será definido um limite máximo de indicações por cliente em um período determinado (ex: 3 indicações por ano).
* **Múltiplas Indicações:** Um Indicado pode ser indicado por múltiplos Indicação, mas apenas o primeiro Indicação que resultar na aprovação do Indicado receberá o desconto.
* **Administrador:** O administrador do sistema terá acesso a todas as informações, incluindo as indicações, aprovações, descontos aplicados e dados dos clientes.


## Restrições

* O sistema deverá garantir a segurança e privacidade dos dados dos clientes.
* O sistema deverá ser escalável para suportar um número crescente de usuários e indicações.
* A integração com o sistema de emissão de apólices de seguros deverá ser estável e eficiente.
* O sistema deve ser compatível com diferentes dispositivos móveis (Android e iOS).


## Exceções

* **Reprovação da Indicação:** Se a indicação for reprovada, nenhuma notificação de sucesso será enviada ao Indicação, e o Indicado receberá uma notificação informando sobre a reprovação e o motivo.
* **Informações Incompletas:** Se o Indicado fornecer informações incompletas durante o cadastro, a indicação será suspensa até que as informações sejam completadas.
* **Falha na Notificação Push:** Em caso de falha na entrega da notificação *push*, o sistema deverá registrar o erro e tentar novamente após um período determinado.  Um aviso será dado ao administrador do sistema.
* **Fraude:** Em caso de suspeita de fraude, a indicação será investigada e, se comprovada a fraude, a indicação será rejeitada e as medidas cabíveis serão tomadas.


## Decisões

* A plataforma utilizará notificações *push* para manter os clientes informados sobre o status de suas indicações.
* O sistema de descontos será implementado de forma a garantir a rastreabilidade e a auditoria.
* A interface do usuário será amigável e intuitiva, tanto para o administrador quanto para os clientes.
* O sistema de segurança será robusto, garantindo a confidencialidade e integridade dos dados.
* O valor do desconto para o Indicação será revisado periodicamente e poderá ser alterado conforme as estratégias de negócio.


<br>
<hr>
<br>

### 🧠 Instruções para o Agente de Desenvolvimento

**📝 Prompt Complementar:**
Este documento define as regras de negócio, restrições e exceções para o desenvolvimento do backend do sistema de indicações da NCF Indicação Seguros, um MicroSaaS.  A próxima fase de desenvolvimento deve focar na implementação de uma única funcionalidade central: o processo de indicação, desde o cadastro da indicação até a aprovação e notificação dos envolvidos, utilizando uma arquitetura simples e escalável adequada para um MicroSaaS.

**👍 Instruções Positivas:**
Foque em entregar uma única feature central: o fluxo completo de indicação, incluindo os endpoints RESTful para cadastro de indicação, aprovação/reprovação, notificações push (com tratamento de falhas), e consulta de status. Utilize um banco de dados simples e relacional (ex: PostgreSQL ou MySQL) para armazenar as informações necessárias, como dados do Indicação, Indicado, status da indicação e informações de desconto. Implemente a lógica de negócio de forma clara e modular, com funções bem definidas e testáveis. Priorize a segurança dos dados, utilizando mecanismos de autenticação e autorização apropriados (ex: JWT).  A integração com o sistema de emissão de apólices deve ser representada por um único endpoint de simulação, sem a necessidade de uma integração real nesta fase.  Foque na clareza do código e na documentação adequada dos endpoints.

**👎 Instruções Negativas:**
Evite a implementação de funcionalidades adicionais não essenciais nesta fase, como o painel administrativo completo, relatórios complexos ou a integração com sistemas externos além da simulação do sistema de emissão de apólices. Não utilize frameworks de backend complexos ou micro-serviços. Evite o uso de bibliotecas desnecessárias que possam comprometer o desempenho ou a simplicidade do sistema. Não implemente um sistema de notificações genérico para futuras features, focando apenas nas notificações necessárias para o fluxo de indicação.  Não crie uma estrutura de módulos complexa ou lógica genérica que possa ser reutilizada em outros módulos ou sistemas.  A prioridade é a entrega de um MVP funcional e escalável para a feature central de indicação.
