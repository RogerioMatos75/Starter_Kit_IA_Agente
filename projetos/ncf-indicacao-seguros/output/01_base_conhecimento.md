## Regras de Negócio

* Cada cliente pode indicar amigos e parentes para contratar seguros.
* A indicação só é válida se o indicado for aprovado.
* Ao aprovar a indicação, o cliente que indicou recebe um desconto (a ser definido).
* O cliente que indicou recebe um push notificando a aprovação da indicação.
* O indicado recebe um push com os dados do cliente que o indicou e a informação de que um consultor entrará em contato.
* O sistema deve registrar todas as indicações, aprovações e descontos aplicados.
* O sistema deve permitir a administração completa dos usuários, seguros e indicações.

## Requisitos Funcionais

* Cadastro de clientes (assegurados).
* Cadastro de seguros.
* Sistema de indicação de clientes.
* Aprovação/reprovação de indicações pelo administrador.
* Emissão de push notifications para o cliente que indicou e para o indicado.
* Aplicação de descontos para clientes que indicaram com sucesso.
* Relatórios de indicações e descontos.
* Painel de administração para gerenciamento de usuários, seguros e indicações.
* Gerenciamento de usuários (cadastro, edição, exclusão).
* Gerenciamento de seguros (cadastro, edição, exclusão).
* Consulta de histórico de indicações.

## Requisitos Não Funcionais

* Alta disponibilidade do sistema.
* Segurança dos dados dos usuários.
* Interface intuitiva e fácil de usar.
* Performance adequada para resposta rápida às solicitações.
* Escalabilidade para suportar um grande número de usuários e indicações.
* Segurança das transações e informações sensíveis.
* Compatibilidade com diferentes dispositivos móveis (Android e iOS).
* Manutenibilidade e facilidade de atualização do sistema.

## Personas de Usuário

* **Administrador:** Responsável pela administração do sistema, aprovação de indicações e geração de relatórios.
* **Assegurado:** Cliente que possui um seguro e pode indicar outros clientes.
* **Indicado:** Pessoa indicada por um cliente para contratar um seguro.

## Fluxos de Usuário

* **Fluxo de Indicação:** Assegurado acessa o sistema, indica um novo cliente, o indicado recebe uma mensagem para prosseguir com a contratação, o administrador aprova/reprova a indicação, e o Assegurado e o Indicado recebem notificações push com o resultado.
* **Fluxo de Administração:** Administrador acessa o painel administrativo, aprova/reprova indicações, gerencia usuários e seguros, e gera relatórios.
* **Fluxo de Cadastro de Assegurado:** Novo usuário se cadastra no sistema e fornece as informações necessárias para a contratação de um seguro.
* **Fluxo de Cadastro de Indicado:**  O indicado recebe um convite e pode se cadastrar fornecendo seus dados.

