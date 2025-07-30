# 01_base_conhecimento.md

## Projeto: NCF-Teste (Archon)

### Regras de Negócio (RN)

* **RN1:** Um usuário pode indicar um seguro para outro usuário.
* **RN2:** O usuário indicado recebe um desconto no seguro.
* **RN3:** O usuário que indica recebe uma recompensa (a ser definida) pela indicação aprovada.
* **RN4:** O sistema notifica via push tanto o indicador quanto o indicado sobre o status da indicação.
* **RN5:** O indicador pode gerenciar suas indicações, visualizando seu status e recompensas.
* **RN6:** O indicado precisa aceitar a indicação para receber o desconto.
* **RN7:**  O desconto aplicado ao indicado é previamente definido e configurado pelo administrador.
* **RN8:** Apenas indicações aprovadas geram recompensas para o indicador.
* **RN9:** O administrador pode visualizar relatórios sobre as indicações, descontos e recompensas.

### Requisitos Funcionais (RF)

* **RF1:** Cadastro e login de usuários (Indicador e Indicado).
* **RF2:** Tela de indicação de seguro com campos para dados do indicado e informações do seguro.
* **RF3:** Sistema de notificações push (para indicador e indicado).
* **RF4:**  Gerenciamento de indicações (visualizar status, recompensas, etc.).
* **RF5:** Aplicação de descontos para indicados.
* **RF6:**  Painel administrativo para gerenciamento de usuários, seguros, descontos, e relatórios.
* **RF7:**  Integração com sistema de seguros (se necessário).


### Requisitos Não Funcionais (RNF)

* **RNF1:** Alta disponibilidade e escalabilidade do sistema.
* **RNF2:** Segurança de dados (criptografia, autenticação, autorização).
* **RNF3:**  Interface intuitiva e amigável para todos os tipos de usuários.
* **RNF4:**  Performance adequada (tempos de resposta rápidos).
* **RNF5:**  Compatibilidade com diferentes dispositivos móveis (Android e iOS).
* **RNF6:**  Testes unitários, de integração e de sistema.
* **RNF7:**  Manutenibilidade e facilidade de atualização do sistema.


### Personas de Usuário

* **Indicador:** Usuário que indica seguros a outros. Possui conta no aplicativo e busca recompensas.
* **Indicado:** Usuário que recebe a indicação de seguro. Busca descontos e facilidade na contratação.
* **Administrador:** Usuário com privilégios administrativos, responsável por gerenciar o sistema e visualizar relatórios.

### Fluxos de Usuário

* **Fluxo 1 (Indicar Seguro):** Indicador acessa o aplicativo, seleciona o seguro, preenche os dados do indicado e envia a indicação.  Recebe notificação sobre o status.
* **Fluxo 2 (Receber Indicação):** Indicado recebe notificação push. Acessa o aplicativo, visualiza a indicação e aceita ou rejeita.
* **Fluxo 3 (Gerenciar Indicações):** Indicador acessa o aplicativo e visualiza o histórico de suas indicações, status e recompensas.
* **Fluxo 4 (Administrador):** Administrador acessa o painel administrativo, gerencia usuários, seguros, descontos e visualiza relatórios.
* **Fluxo 5 (Resgatar Desconto):** Indicado após aprovação da indicação, utiliza o código de desconto na contratação do seguro.

