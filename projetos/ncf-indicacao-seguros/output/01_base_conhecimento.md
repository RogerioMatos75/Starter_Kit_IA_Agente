## Regras de Negócio

* Um usuário (assegurado) pode indicar um amigo/parente para adquirir um seguro.
* A indicação precisa ser aprovada para que o indicador receba o desconto.
* O desconto para o indicador é concedido após a aprovação da indicação e a efetivação da compra do seguro pelo indicado.
* O sistema deve registrar o histórico de indicações, incluindo status (pendente, aprovado, rejeitado).
* O administrador tem acesso a todos os dados do sistema e pode gerenciar as indicações.

## Requisitos Funcionais

* Cadastro de usuário (assegurado).
* Tela de indicação com formulário para inserir dados do indicado.
* Sistema de notificação push para indicador e indicado.
* Painel administrativo para gerenciamento de indicações, usuários e relatórios.
* Fluxo de aprovação de indicações pelo administrador.
* Visualização do histórico de indicações pelo usuário (assegurado).
* Integração com sistema de seguros para validação de dados e aplicação de descontos.
* Geração de relatórios sobre indicações.

## Requisitos Não Funcionais

* **Performance:** O sistema deve responder em até 2 segundos para todas as ações do usuário.
* **Segurança:** O sistema deve proteger as informações dos usuários contra acesso não autorizado.  Implementar autenticação segura e criptografia de dados.
* **Usabilidade:** O sistema deve ser intuitivo e fácil de usar para todos os tipos de usuários.  Design responsivo para diferentes dispositivos.
* **Escalabilidade:** O sistema deve ser capaz de lidar com um grande número de usuários e indicações simultaneamente.
* **Disponibilidade:** O sistema deve estar disponível 24 horas por dia, 7 dias por semana, com tempo de inatividade mínimo.
* **Manutenibilidade:** O sistema deve ser fácil de manter e atualizar.

## Personas de Usuário

* **Administrador:** Usuário com privilégios completos para gerenciar o sistema.
* **Assegurado:** Usuário que compra seguros e pode indicar amigos/parentes.
* **Indicado:** Usuário indicado por um assegurado para adquirir um seguro.

## Fluxos de Usuário

* **Fluxo de Indicação:** O Assegurado acessa a tela de indicação, preenche os dados do Indicado e envia o convite. O sistema envia um push para o Indicado e notifica o Assegurado. O administrador aprova ou rejeita a indicação. Se aprovada, o Assegurado recebe um push e o desconto é aplicado quando o Indicado efetiva a compra do seguro.
* **Fluxo do Administrador:** O Administrador acessa o painel administrativo para visualizar e gerenciar as indicações, usuários e relatórios.
* **Fluxo do Indicado:** O Indicado recebe um push com informações sobre a indicação e entra em contato com um consultor.
