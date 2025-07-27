# 01_base_conhecimento.md

## Projeto: NCF - Archon

### Regras de Negócio (RN)

* **RN1:**  Um usuário pode indicar um seguro para outro usuário, fornecendo os dados do indicado.
* **RN2:**  O indicado receberá um desconto pré-determinado no seguro ao ser aprovado.
* **RN3:** O indicador receberá uma recompensa (definida previamente) após a aprovação do indicado.
* **RN4:** O sistema deve gerenciar o histórico de indicações de cada usuário.
* **RN5:**  O sistema enviará notificações push para o indicador e o indicado após a aprovação da indicação.  A notificação para o indicado deve incluir informações sobre o indicador.
* **RN6:**  O sistema deve possuir mecanismos para validar a informação do indicado e garantir a integridade dos dados.
* **RN7:** O sistema deve permitir ao administrador gerenciar usuários, seguros, descontos e recompensas.
* **RN8:** O sistema deve garantir a segurança e privacidade dos dados dos usuários.
* **RN9:** O sistema deve registrar todas as transações realizadas.


### Requisitos Funcionais (RF)

* **RF1:** Cadastro e login de usuários (Indicador e Indicado).
* **RF2:** Tela para indicar um seguro, incluindo a inserção de dados do indicado.
* **RF3:** Tela de gerenciamento de indicações para o indicador, exibindo o status de cada indicação (pendente, aprovado, rejeitado).
* **RF4:** Tela para o indicado visualizar a indicação recebida e resgatar o desconto.
* **RF5:** Sistema de notificações push para indicadores e indicados.
* **RF6:** Painel administrativo para gerenciamento do sistema.
* **RF7:**  Integração com APIs externas de seguros (se necessário).
* **RF8:** Relatórios de indicações e performance do sistema.


### Requisitos Não Funcionais (RNF)

* **RNF1:**  Escalabilidade: O sistema deve suportar um número crescente de usuários e indicações.
* **RNF2:**  Performance: O sistema deve ser responsivo e eficiente.
* **RNF3:**  Segurança: O sistema deve proteger os dados dos usuários contra acesso não autorizado.
* **RNF4:**  Disponibilidade: O sistema deve estar disponível 24/7.
* **RNF5:**  Usabilidade: O sistema deve ser intuitivo e fácil de usar para todos os tipos de usuários.
* **RNF6:**  Manutenibilidade: O sistema deve ser fácil de manter e atualizar.


### Personas de Usuário

* **Indicador:** Usuário que busca recompensas por indicar seguros para amigos e conhecidos.
* **Indicado:** Usuário que busca descontos em seguros através de indicações.
* **Administrador:** Usuário com privilégios para gerenciar o sistema.


### Fluxos de Usuário

* **Fluxo 1 (Indicador):** Login -> Indicar Seguro -> Inserir dados do indicado -> Enviar -> Monitorar indicação -> Receber Notificação (após aprovação).
* **Fluxo 2 (Indicado):** Receber Notificação -> Acessar aplicativo -> Visualizar indicação -> Resgatar desconto.
* **Fluxo 3 (Administrador):** Login -> Gerenciar Usuários -> Gerenciar Seguros -> Gerenciar Descontos -> Gerenciar Indicadores -> Gerar Relatórios.

