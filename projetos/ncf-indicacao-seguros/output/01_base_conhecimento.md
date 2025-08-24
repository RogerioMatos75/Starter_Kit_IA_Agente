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

