## Regras de Negócio
* Cada cliente que indicar um amigo ou parente para um seguro NCF recebe um desconto.
* A indicação só gera desconto após a aprovação do indicado.
* Após a aprovação, o cliente que indicou recebe um push de parabéns.
* Após a aprovação, o indicado recebe um push com os dados do cliente que o indicou e a informação de que um consultor entrará em contato.

## Requisitos Funcionais
* Cadastro de usuários (Administrador, Assegurado).
* Sistema de indicação com envio de convites.
* Gerenciamento de descontos para clientes que indicaram.
* Processo de aprovação de indicações.
* Envio de notificações push (para o cliente que indicou e para o indicado).
* Tela administrativa para monitoramento de indicações e aprovações.
* Tela do Assegurado para visualizar suas indicações e descontos.
* Tela de convite para o indicado com dados do cliente que o indicou.
* Relatórios de indicações e descontos.

## Requisitos Não Funcionais
* Alta disponibilidade e escalabilidade do sistema.
* Segurança dos dados dos usuários, seguindo as normas de privacidade e proteção de dados.
* Interface intuitiva e fácil de usar para todos os tipos de usuários.
* Performance rápida e eficiente em todas as funcionalidades.
* Sistema robusto e tolerante a falhas.
* Compatibilidade com diferentes dispositivos móveis (Android e iOS).
* Integração com sistema de envio de notificações push.

## Personas de Usuário
* **Administrador:** Usuário com acesso total ao sistema, responsável por monitorar indicações, aprovações e gerar relatórios.
* **Assegurado:** Cliente que utiliza o sistema para indicar amigos e visualizar seus descontos.
* **Indicado:** Pessoa indicada por um Assegurado para adquirir um seguro NCF.

## Fluxos de Usuário
* **Fluxo de Indicação:** Assegurado acessa o sistema, indica um amigo, envia o convite. O indicado recebe o convite, se cadastra e sua indicação é analisada. Aprovado, o Assegurado e o Indicado recebem notificações push.
* **Fluxo Administrativo:** Administrador acessa o sistema, monitora indicações, aprova ou rejeita indicações, gera relatórios.
* **Fluxo de Visualização de Descontos:** Assegurado acessa o sistema e visualiza seus descontos acumulados por indicações aprovadas.

