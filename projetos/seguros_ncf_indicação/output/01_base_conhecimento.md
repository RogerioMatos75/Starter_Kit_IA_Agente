## Regras de Negócio

* Um cliente atual (assegurado) pode indicar um novo cliente (potencial cliente).
* Ao indicar um novo cliente, o cliente atual recebe um código de indicação único.
* O novo cliente precisa utilizar o código de indicação durante o seu cadastro para que a indicação seja validada.
* Após a aprovação do seguro do cliente indicado, tanto o cliente que indicou quanto o indicado recebem descontos.
* O valor do desconto para o cliente que indicou e para o indicado será definido pela NCF e informado no aplicativo.
* O sistema rastreia todas as indicações, permitindo o monitoramento do programa de indicações.
* O administrador do sistema tem acesso a um painel para gerenciar o programa e gerar relatórios.
* O sistema envia notificações push para o cliente que indicou e para o indicado em momentos estratégicos do processo.


## Requisitos Funcionais

* Cadastro e login de usuários (assegurados e administradores).
* Criação de indicações por parte dos clientes atuais.
* Envio de notificações push para o cliente que indicou e para o indicado.
* Gerenciamento do sistema e geração de relatórios para administradores.
* Visualização de informações da apólice de seguro pelo cliente.
* Visualização dos detalhes da indicação pelo cliente indicado.
* Aplicação de descontos para o cliente que indicou e para o indicado após aprovação do seguro.
* Painel administrativo com relatórios e controle do programa de indicação.


## Requisitos Não Funcionais

* **Performance:** O aplicativo deve ser responsivo e carregar rapidamente em diferentes dispositivos e conexões de internet.
* **Segurança:** O sistema deve proteger as informações dos usuários contra acesso não autorizado e garantir a confidencialidade dos dados.
* **Usabilidade:** O aplicativo deve ser intuitivo e fácil de usar, com uma interface amigável para todos os tipos de usuários.
* **Escalabilidade:** O sistema deve ser capaz de suportar um crescimento significativo no número de usuários e indicações.
* **Disponibilidade:** O aplicativo deve estar disponível o máximo de tempo possível, com alta confiabilidade.
* **Manutenibilidade:** O código deve ser limpo, bem documentado e fácil de manter.


## Personas de Usuário

* **Cliente Atual (Asegurado):** Usuário já cadastrado na NCF, que pode indicar novos clientes e acompanhar o status das suas indicações.
* **Potencial Cliente (Indicado):** Novo usuário indicado por um cliente atual, que precisa realizar o seu cadastro e acompanhar o processo de aprovação do seu seguro.
* **Administrador do Sistema:** Usuário com privilégios administrativos para gerenciar o sistema, monitorar o desempenho do programa de indicações e gerar relatórios.


## Fluxos de Usuário

* **Fluxo de Indicação:** Cliente atual acessa o aplicativo, encontra a opção de "Indicar um amigo", gera um código de indicação único, compartilha o código com o indicado. O indicado utiliza o código durante o seu cadastro.  Após a aprovação do seguro do indicado, ambos recebem notificações e descontos.
* **Fluxo de Cadastro/Login:** Usuário acessa a tela de login e cadastra-se ou faz login com credenciais.
* **Fluxo de Administrador:** Administrador acessa o painel administrativo para monitorar as indicações, gerar relatórios, controlar descontos e outras funções administrativas.
* **Fluxo de Visualização de Apólice:** Cliente atual acessa o aplicativo e visualiza as informações de sua apólice.
* **Fluxo de Visualização de Detalhes de Indicação (Indicado):** Indicado acessa o aplicativo e visualiza informações sobre a indicação (quem o indicou, status, etc.).

