## Regras de Negócio

* Um usuário (Assegurado) pode indicar amigos e parentes para contratar seguros.
* A indicação deve conter informações suficientes para identificar o indicado e o indicador.
* Após a aprovação da indicação, tanto o indicador quanto o indicado recebem notificações push.
* O indicador recebe um desconto pré-definido por cada indicação aprovada.
* O sistema deve gerenciar o acompanhamento das indicações, desde a solicitação até a aprovação.
* O administrador do sistema tem acesso completo a todas as informações e funcionalidades.


## Requisitos Funcionais

* Cadastro e login de usuários (Assegurados e Administrador).
* Tela para realizar indicações, com campos para informações do indicado.
* Sistema de notificações push para indicador e indicado.
* Gerenciamento de descontos para indicadores.
* Painel administrativo para monitoramento de indicações, usuários e descontos.
* Relatórios de indicações aprovadas e rejeitadas.
* Gerenciamento de usuários (cadastro, edição, exclusão).
* Integração com sistema de seguros externo (para aprovação de indicações).


## Requisitos Não Funcionais

* **Performance:** O sistema deve responder em até 2 segundos para todas as solicitações.
* **Segurança:** O sistema deve proteger as informações dos usuários contra acessos não autorizados.  Implementação de autenticação robusta e criptografia de dados sensíveis.
* **Usabilidade:** A interface do usuário deve ser intuitiva e fácil de usar para todos os perfis de usuário.
* **Escalabilidade:** O sistema deve ser capaz de lidar com um grande número de usuários e indicações simultaneamente.
* **Disponibilidade:** O sistema deve estar disponível 24 horas por dia, 7 dias por semana, com tempo de inatividade mínimo.
* **Manutenibilidade:** O sistema deve ser fácil de manter e atualizar.
* **Portabilidade:** O sistema deve ser compatível com diferentes dispositivos móveis (Android e iOS).


## Personas de Usuário

* **Assegurado:** Usuário que já possui um seguro e pode indicar novos clientes.
* **Indicado:** Usuário indicado por um Assegurado para contratar um seguro.
* **Administrador:** Usuário com acesso total ao sistema, responsável por gerenciar usuários, indicações e relatórios.


## Fluxos de Usuário

* **Fluxo de Indicação:** Assegurado acessa o aplicativo, preenche o formulário de indicação com dados do indicado, envia a indicação. O sistema notifica o indicado. O Indicado aceita ou rejeita a indicação. O Administrador aprova a indicação. Notificação para Assegurado e Indicado com status da indicação.
* **Fluxo de Administrador:** Administrador acessa o sistema, monitora indicações, aprova/rejeita indicações, gerencia usuários e gera relatórios.
* **Fluxo de Login:** Usuário (Assegurado ou Administrador) insere credenciais, autentica-se e acessa o sistema.
