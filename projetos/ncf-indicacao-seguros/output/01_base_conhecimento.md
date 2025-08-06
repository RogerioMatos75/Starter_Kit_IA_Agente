## Regras de Negócio

* Cada cliente que indicar um amigo ou parente que seja aprovado para um seguro receberá um desconto.
* O valor do desconto será definido pela empresa.
* O cliente que indica receberá um push notificando sobre a aprovação da indicação.
* O indicado receberá um push com os dados do cliente que o indicou e informando que um consultor entrará em contato.
* A aprovação do indicado será gerenciada pelo sistema.
* O sistema manterá um registro de todas as indicações, aprovações e descontos concedidos.

## Requisitos Funcionais

* Cadastro de clientes (Assegurados).
* Cadastro de indicações por clientes existentes.
* Sistema de aprovação de indicações.
* Emissão de push notifications para clientes que indicaram e para os indicados.
* Painel administrativo para gerenciamento de usuários, indicações e descontos.
* Consulta de informações de seguros para clientes (Assegurados).
* Gerenciamento de descontos para clientes que realizaram indicações.
* Relatórios de indicações e descontos.

## Requisitos Não Funcionais

* Alta disponibilidade do sistema.
* Segurança dos dados dos clientes (criptografia, autenticação e autorização).
* Interface intuitiva e fácil de usar para todas as personas.
* Performance adequada para o processamento de grandes volumes de dados e transações.
* Escalabilidade para atender ao crescimento do número de usuários.
* Compatibilidade com dispositivos móveis (Android e iOS).
* Conformidade com as leis e regulamentos de privacidade de dados.

## Personas de Usuário

* **Administrador:** Responsável pela gestão do sistema, incluindo cadastros, relatórios e configurações.
* **Assegurado:** Cliente que utiliza o sistema para se cadastrar, realizar indicações e visualizar informações do seu seguro.
* **Indicado:** Pessoa indicada por um Assegurado para adquirir um seguro.

## Fluxos de Usuário

* **Assegurado indica um amigo:** O Assegurado acessa o sistema, preenche um formulário com os dados do amigo e envia a indicação.
* **Aprovação da indicação:** O Administrador aprova ou rejeita a indicação no painel administrativo.
* **Notificação de aprovação (Assegurado):** O Assegurado recebe uma notificação push informando sobre a aprovação da indicação.
* **Notificação de indicação (Indicado):** O Indicado recebe uma notificação push com os dados do Assegurado que o indicou e a informação de que um consultor entrará em contato.
* **Administrador monitora indicações:** O Administrador acompanha as indicações em andamento e aprova ou rejeita as novas solicitações.
* **Assegurado consulta informações:** O Assegurado pode acessar e consultar suas informações e o histórico de suas indicações.

