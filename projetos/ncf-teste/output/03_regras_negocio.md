# 03_regras_negocio.md

## Regras de Negócio

* **Indicação:** Um usuário (Indicador) pode indicar um seguro para outro usuário (Indicado).  A indicação deve conter informações mínimas: nome do Indicado, e-mail ou número de telefone do Indicado e o tipo de seguro.
* **Aprovação:** A indicação precisa ser aprovada pelo sistema antes que o Indicador e o Indicado recebam benefícios. A aprovação pode ser automática ou manual, dependendo da configuração do sistema.
* **Notificações Push:** Ao ser aprovada a indicação, o Indicador recebe uma notificação de sucesso, e o Indicado recebe uma notificação contendo o nome do Indicador e informando que um consultor entrará em contato.
* **Descontos:** O Indicado recebe um desconto pré-determinado no seguro indicado, após a aprovação da indicação.  O valor do desconto deve ser configurado pelo administrador.
* **Gamificação (futuro):**  Um sistema de gamificação pode ser implementado posteriormente para premiar os Indicadores com base no número de indicações bem-sucedidas.
* **Gestão de Indicadores:** Os Indicadores podem visualizar o status de suas indicações (pendente, aprovada, rejeitada).
* **Gestão de Indicados:** Os Indicados podem visualizar as indicações recebidas e os descontos correspondentes.
* **Cadastro de Usuário:**  É necessário um processo de cadastro para ambos os usuários (Indicador e Indicado), com validação de dados (email e telefone).
* **Segurança:**  O sistema deve garantir a segurança dos dados dos usuários, seguindo as melhores práticas de segurança.
* **Painel Administrativo:** O administrador deve ter acesso a um painel para gerenciar usuários, seguros, descontos, notificações e relatórios.


## Restrições

* **Integração com APIs de Seguros:** A integração com APIs externas de seguros poderá ser necessária para automatizar processos (consulta de preços, aprovação de seguros) mas está fora do escopo inicial.
* **Plataforma:** O aplicativo poderá ser desenvolvido para web e/ou mobile (Android e iOS).  A decisão final de plataforma será tomada após a fase de Discovery.
* **Orçamento:** O orçamento do projeto é limitado a R$ 1.815,00.


## Exceções

* **Indicação Rejeitada:** Se uma indicação for rejeitada, o Indicador e o Indicado receberão notificações informando o motivo da rejeição.
* **Falha na Notificação Push:**  O sistema deve ter um mecanismo de fallback para notificar o usuário caso haja falha no envio da notificação Push (ex: e-mail ou SMS).
* **Dados Incompletos:** O sistema deve validar os dados de cadastro e indicação, impedindo a submissão de informações incompletas ou inválidas.


## Decisões

* **Priorização de Funcionalidades:** As funcionalidades de indicação, aprovação, notificações e descontos são prioritárias na primeira versão. A gamificação será considerada em versões futuras.
* **Plataforma Inicial:** A prioridade inicial será para o desenvolvimento da versão web, podendo ser seguida de versão mobile.
