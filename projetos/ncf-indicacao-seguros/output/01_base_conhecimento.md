## Regras de Negócio
* Cada indicação válida gera 1% de desconto para o usuário que indicou.
* Um desconto adicional de 1% é concedido ao usuário que indicou quando o indicado contrata o seguro.
* O desconto máximo acumulativo é de 10% ao ano na apólice.
* O administrador deve confirmar a validade de cada indicação.
* O sistema deve validar se o amigo indicado já foi cadastrado anteriormente.


## Requisitos Funcionais
* Indicação de amigos: Usuário deve poder indicar amigos através do PWA, fornecendo nome, telefone e e-mail.
* Descontos progressivos: O sistema deve calcular e aplicar descontos com base nas indicações válidas e contratações dos indicados.
* Painel administrativo: O administrador deve ter acesso a um painel para visualizar, confirmar e gerenciar indicações, enviar notificações e gerar relatórios.
* Notificações push: O sistema deve enviar notificações push para o usuário que indicou ao confirmar a indicação e para o administrador quando uma nova indicação é feita.
* Autenticação: O sistema deve ter mecanismos de autenticação para usuários (clientes) e administradores.
* Relatórios: O administrador deve poder gerar relatórios sobre o total de indicações, conversões e descontos concedidos.


## Requisitos Não Funcionais
* Performance: O PWA deve ser rápido e responsivo.
* Disponibilidade: O PWA deve estar disponível 24/7.
* Segurança: Os dados dos usuários devem ser protegidos (HTTPS, validação de dados, autenticação robusta, proteção contra CSRF e XSS, sanitização de dados, rate limiting).
* Escalabilidade: O PWA deve ser escalável para suportar um grande número de usuários.
* Usabilidade: O PWA deve ser fácil de usar e intuitivo.
* Acessibilidade: O PWA deve ser acessível a usuários com deficiência.
* Offline: O PWA deve funcionar parcialmente offline.


## Personas de Usuário
* **Assegurado:** Cliente da seguradora que utiliza o aplicativo para indicar amigos e receber descontos.
* **Indicado:** Pessoa indicada por um assegurado para contratar um seguro.
* **Administrador:** Usuário com permissões elevadas para gerenciar o sistema.


## Fluxos de Usuário
* **Indicação:** O assegurado acessa o aplicativo, preenche um formulário com os dados do indicado e envia a indicação. O sistema envia uma notificação push para o administrador.
* **Administração:** O administrador recebe a notificação, acessa o painel administrativo, visualiza a indicação e a confirma ou rejeita. Se confirmada, o sistema envia uma notificação push para o assegurado, informando sobre o desconto concedido.  O administrador pode enviar um link da proposta para o indicado.
* **Contratação:** Após a confirmação, o indicado recebe a notificação, acessa o link da proposta e contrata o seguro.  O administrador registra a contratação no sistema.  O sistema recalcula o desconto do assegurado.
* **Login:** Assegurados e administradores realizam login no sistema com suas credenciais.
* **Relatórios:** O administrador gera relatórios sobre as indicações, conversões e descontos.

