# 01_base_conhecimento.md

## Projeto: NCF-Teste (Archon - Aplicativo de Indicação de Seguros)

### Regras de Negócio (RN)

* **RN1:** Um usuário pode indicar um seguro para outro usuário, registrando uma indicação.
* **RN2:**  Ao ser aprovada, uma indicação garante um desconto para o indicado e uma recompensa para o indicador.
* **RN3:**  Indicadores podem gerenciar suas indicações e visualizar seus ganhos (recompensas).
* **RN4:** Indicados recebem notificações push sobre indicações e descontos.
* **RN5:**  O sistema de descontos é configurado pelo administrador.
* **RN6:** O administrador pode visualizar relatórios e gerenciar usuários.
* **RN7:**  O sistema deve garantir a segurança das informações dos usuários.
* **RN8:**  Notificações push devem conter informações claras e concisas.
* **RN9:** O sistema deve permitir o resgate do desconto pelo indicado após a aprovação do seguro.


### Requisitos Funcionais (RF)

* **RF1:** Cadastro de usuário (Indicador e Indicado).
* **RF2:** Login de usuário.
* **RF3:** Tela para indicar um seguro, incluindo informações do indicado e do seguro.
* **RF4:** Tela para gerenciar indicações (Indicador).
* **RF5:** Tela para visualizar descontos e recompensas (Indicador).
* **RF6:** Tela para visualizar indicações recebidas (Indicado).
* **RF7:** Sistema de notificações push (para Indicador e Indicado).
* **RF8:**  Painel administrativo para gerenciamento de usuários, seguros, descontos e relatórios.
* **RF9:**  Integração com sistema externo de seguros (se aplicável).
* **RF10:**  Funcionalidade para resgate de desconto.


### Requisitos Não Funcionais (RNF)

* **RNF1:**  Alta disponibilidade e performance do sistema.
* **RNF2:**  Escalabilidade para suportar um grande número de usuários.
* **RNF3:**  Segurança da informação, protegendo dados sensíveis dos usuários.
* **RNF4:**  Interface intuitiva e amigável para todos os tipos de usuários.
* **RNF5:**  Aplicativo responsivo para diferentes dispositivos (mobile e web).
* **RNF6:**  Testes unitários e de integração completos.
* **RNF7:**  Documentação completa do sistema.


### Personas de Usuário

* **Indicador:** Usuário que busca gerar renda extra indicando seguros para amigos e familiares.
* **Indicado:** Usuário que busca economizar na contratação de seguros.
* **Administrador:** Usuário com privilégios para gerenciar o sistema e visualizar relatórios.


### Fluxos de Usuário

* **Fluxo 1 (Indicador):** Cadastro/Login → Indicar Seguro (Preencher dados do indicado e informações do seguro) → Acompanhar Indicação (Visualizar status e ganhos) → Receber Notificação (Aprovação/Reprovação da indicação).
* **Fluxo 2 (Indicado):** Cadastro/Login → Receber Indicação (Notificação Push) → Visualizar Detalhes da Indicação → Resgatar Desconto (após aprovação).
* **Fluxo 3 (Administrador):** Login → Gerenciar Usuários → Gerenciar Seguros → Gerenciar Descontos → Visualizar Relatórios.

