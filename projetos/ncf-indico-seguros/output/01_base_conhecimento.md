# 01_base_conhecimento.md

## Projeto: NCF-Indico-Seguros

### Regras de Negócio (RN)

* **RN1:**  Um usuário (Asegurado) pode indicar quantos potenciais clientes desejar.
* **RN2:** Cada indicação é rastreada pelo sistema, permitindo o acompanhamento do seu status (pendente, aprovado, recusado).
* **RN3:**  Um desconto é aplicado para o Asegurado que indicou e para o Potencial Cliente (Indicado) após a aprovação da apólice do Indicado.
* **RN4:** O valor do desconto é definido pela NCF e pode variar conforme a política de indicações.
* **RN5:**  O administrador do sistema tem permissão para visualizar, gerenciar e aprovar/recusar indicações.
* **RN6:** O administrador pode gerar relatórios sobre o desempenho do programa de indicações.
* **RN7:** O sistema deve garantir a segurança e confidencialidade dos dados dos usuários.
* **RN8:**  Notificações push serão enviadas ao Asegurado e ao Indicado sobre o status da indicação.


### Requisitos Funcionais (RF)

* **RF1:** Cadastro e login de usuários (Asegurados e Administradores).
* **RF2:**  Sistema de criação de indicações com rastreamento completo do processo.
* **RF3:**  Envio de notificações push para Asegurados e Indicados.
* **RF4:**  Painel de administração com funcionalidades de gerenciamento e geração de relatórios.
* **RF5:**  Visualização das informações da apólice de seguro pelo Asegurado.
* **RF6:**  Visualização dos detalhes da indicação pelo Indicado e Asegurado.
* **RF7:**  Sistema de aprovação/recusa de indicações pelo administrador.
* **RF8:**  Aplicação automática de descontos após a aprovação da apólice do Indicado.


### Requisitos Não Funcionais (RNF)

* **RNF1:**  Alta performance e escalabilidade do sistema.
* **RNF2:**  Interface intuitiva e amigável para todos os tipos de usuários.
* **RNF3:**  Segurança robusta para proteger os dados dos usuários.
* **RNF4:**  Disponibilidade do sistema 24/7.
* **RNF5:**  Compatibilidade com iOS e Android.
* **RNF6:**  Testes rigorosos para garantir a qualidade do software.
* **RNF7:**  Integração com sistema de gestão de apólices da NCF (se aplicável).


### Personas de Usuário

* **Asegurado:** Cliente atual da NCF que utiliza o aplicativo para indicar novos clientes.
* **Potencial Cliente (Indicado):**  Novo cliente indicado por um Asegurado.
* **Administrador do Sistema:** Usuário com permissão para gerenciar o sistema e gerar relatórios.


### Fluxos de Usuário

* **Fluxo 1 (Asegurado):** Login > Criar Indicação (preenchendo dados do Indicado) > Acompanhamento do status da indicação > Visualização do desconto aplicado (após aprovação).
* **Fluxo 2 (Indicado):** Recebe notificação push > Acessa o link da indicação > Preenche informações necessárias para a contratação do seguro.
* **Fluxo 3 (Administrador):** Login > Gerenciamento de indicações (aprovar/recusar) > Geração de relatórios > Monitoramento do desempenho do programa de indicações.

