## Regras de Negócio

* **Cadastro e Login:** Usuários (assegurados e administradores) devem se cadastrar no sistema fornecendo informações completas e precisas. O login deve ser seguro, utilizando mecanismos de autenticação robustos.
* **Indicação:** Um usuário (assegurado) pode indicar um novo cliente (indicado) fornecendo seus dados pessoais.  Cada indicação é rastreada pelo sistema, associada ao usuário que a criou.
* **Notificações Push:** Ao criar uma indicação, o usuário (assegurado) recebe uma notificação push confirmando o envio.  O indicado também recebe uma notificação push informando sobre a indicação e que um consultor entrará em contato.
* **Aprovação da Indicação:** A indicação só é considerada válida após a aprovação do novo cliente (indicado). A aprovação dependerá da conclusão do processo de contratação do seguro.
* **Aplicação de Desconto:** Após a aprovação da indicação, tanto o usuário (assegurado) que indicou quanto o indicado recebem um desconto previamente definido nas suas apólices de seguro.
* **Gerenciamento do Sistema (Administrador):** O administrador possui acesso a um painel para monitorar o desempenho do programa de indicações, gerar relatórios, e gerenciar usuários.
* **Visualização de Informações:** O usuário (assegurado) pode visualizar suas informações pessoais, detalhes das suas indicações e o status de cada uma. O indicado pode visualizar informações sobre quem o indicou e os próximos passos para concluir o processo.


## Restrições

* O sistema deve suportar um volume considerável de usuários e indicações simultaneamente, garantindo performance e escalabilidade.
* A integração com o sistema de seguros da NCF deve ser robusta e eficiente, garantindo a atualização em tempo real dos dados.
* O sistema de notificações push deve ser confiável e garantir a entrega das mensagens aos usuários.
* O valor do desconto aplicado deve ser configurado pelo administrador e deve ser previamente definido e imutável durante o processo.


## Exceções

* **Indicação Inválida:** Caso o indicado não forneça informações corretas ou não conclua o processo de contratação, a indicação será considerada inválida, e nenhum desconto será aplicado.
* **Falha na Notificação Push:** Caso haja falha na entrega de uma notificação push, o sistema deve registrar o erro e tentar reenviá-la posteriormente.
* **Cadastro Duplicado:** O sistema deve impedir cadastros duplicados, garantindo a unicidade dos usuários.


## Decisões

* Foi decidido utilizar notificações push para melhorar o engajamento e a comunicação com os usuários.
* Foi definido que o sistema de indicações será baseado em um modelo de rastreamento e aprovação.
* O desenvolvimento será realizado em etapas sequenciais (Discovery, Design, Desenvolvimento, Testes, Implantação), seguindo metodologias ágeis.
* A plataforma será desenvolvida para iOS e Android.
* O sistema de descontos será configurado pelo administrador.

