# 01_base_conhecimento.md

## Projeto: NCF-Teste (Archon)

### Regras de Negócio (RN)

* **RN1:** Um usuário pode indicar um seguro para outro usuário, fornecendo seu nome e informações de contato.
* **RN2:** O usuário indicado recebe uma notificação push informando sobre a indicação e o nome do indicador.
* **RN3:** O indicador recebe uma notificação push quando a indicação é aprovada.
* **RN4:** O indicado recebe um desconto no seguro caso a indicação seja aprovada.
* **RN5:** O sistema deve registrar todas as indicações, incluindo o status (pendente, aprovado, rejeitado).
* **RN6:**  O administrador pode visualizar todas as indicações e gerenciar o sistema.
* **RN7:**  O sistema de descontos deve ser configurado pelo administrador.
* **RN8:** O sistema deve possuir mecanismo de autenticação e autorização de usuários.
* **RN9:**  O sistema deve garantir a confidencialidade das informações do usuário.


### Requisitos Funcionais (RF)

* **RF1:** Cadastro de usuários (Indicador e Indicado).
* **RF2:**  Indicação de seguros (incluindo informações do indicado).
* **RF3:**  Gerenciamento de indicações (visualização, status e detalhes).
* **RF4:** Sistema de notificações push (para Indicador e Indicado).
* **RF5:**  Aplicação de descontos para indicados aprovados.
* **RF6:**  Painel administrativo para gestão de usuários, indicações e descontos.
* **RF7:** Relatórios de indicações e descontos.
* **RF8:**  Integração com APIs de seguros (se aplicável).


### Requisitos Não Funcionais (RNF)

* **RNF1:** Alta disponibilidade do sistema.
* **RNF2:**  Escalabilidade para suportar um grande número de usuários e indicações.
* **RNF3:**  Segurança da informação (proteção de dados dos usuários).
* **RNF4:**  Desempenho responsivo (tempos de resposta rápidos).
* **RNF5:**  Usabilidade intuitiva e amigável para todos os tipos de usuários.
* **RNF6:**  Manutenibilidade do código (facilidade de atualização e manutenção).
* **RNF7:**  Compatibilidade com diferentes dispositivos móveis (Android e iOS).
* **RNF8:**  Teste unitário e integração.


### Personas de Usuário

* **Indicador:** Usuário que busca recompensas ao indicar seguros.
* **Indicado:** Usuário que busca descontos em seguros.
* **Administrador:** Usuário com privilégios para gerenciar o sistema.


### Fluxos de Usuário

* **Fluxo 1 (Indicador):** Cadastro > Login > Indicar Seguro > Acompanhar Indicação > Receber Notificação (após aprovação).
* **Fluxo 2 (Indicado):** Receber Notificação > Verificar Indicação > Resgatar Desconto (se aprovado).
* **Fluxo 3 (Administrador):** Login > Gerenciar Usuários > Gerenciar Indicações > Gerenciar Descontos > Gerar Relatórios.

