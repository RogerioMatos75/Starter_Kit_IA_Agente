## Regras de Negócio

* Um cliente (Assegurado) pode indicar outro cliente (Indicado) para um seguro.
* A indicação só é válida se o Indicado for aprovado.
* Ao ser aprovada a indicação, tanto o Assegurado quanto o Indicado recebem notificações push.
* O Assegurado recebe uma notificação de parabéns pela indicação bem-sucedida.
* O Indicado recebe uma notificação com os dados do Assegurado que o indicou e a informação de que um consultor entrará em contato.
* O sistema deve registrar todas as indicações, incluindo seu status (pendente, aprovado, rejeitado).
* O sistema deve controlar os descontos oferecidos aos Assegurados por indicações aprovadas.

## Requisitos Funcionais

* Cadastro e login de Assegurados.
* Cadastro e login de Administradores.
* Tela para o Assegurado indicar um novo cliente.
* Tela para visualizar o status das indicações do Assegurado.
* Tela para o Administrador visualizar todas as indicações.
* Tela para o Administrador aprovar ou rejeitar indicações.
* Sistema de notificações push para Assegurados e Indicados.
* Relatórios para o Administrador sobre as indicações.
* Gerenciamento de descontos para Assegurados.
* Integração com sistema de seguros (para verificação de aprovação).

## Requisitos Não Funcionais

* Alta disponibilidade do sistema.
* Segurança de dados (criptografia, autenticação forte).
* Usabilidade intuitiva para todos os perfis de usuário.
* Desempenho responsivo em diferentes dispositivos (mobile e desktop).
* Escalabilidade para lidar com um grande volume de usuários e indicações.
* Manutenibilidade e facilidade de atualização do sistema.
* Conformidade com as leis e regulamentações de privacidade de dados.

## Personas de Usuário

* **Assegurado:** Cliente já existente que indica novos clientes.
* **Indicado:** Novo cliente indicado por um Assegurado.
* **Administrador:** Usuário com privilégios para gerenciar o sistema, aprovar/rejeitar indicações e gerar relatórios.

## Fluxos de Usuário

* **Assegurado indica um novo cliente:** O Assegurado acessa o aplicativo, preenche os dados do Indicado e envia a indicação.  Recebe notificação de confirmação e, após aprovação, notificação de sucesso.
* **Indicado recebe a notificação:** O Indicado recebe uma notificação push com os dados do Assegurado e a informação de contato.
* **Administrador aprova/rejeita indicação:** O Administrador acessa o painel administrativo, visualiza as indicações pendentes e aprova ou rejeita cada uma.  O sistema notifica o Assegurado e o Indicado sobre a decisão.
* **Assegurado acompanha status das indicações:** O Assegurado pode visualizar o status de todas as suas indicações.
* **Administrador gera relatórios:** O Administrador pode gerar relatórios sobre o número de indicações, taxa de aprovação e descontos aplicados.

