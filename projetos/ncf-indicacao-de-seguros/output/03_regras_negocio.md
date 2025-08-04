## Regras de Negócio

* **Indicação:** Um cliente (indicação) pode indicar outro cliente (indicado) para um seguro.
* **Aprovação:** A indicação precisa ser aprovada para gerar o desconto para o cliente que indicou e para o indicado.
* **Desconto:**  Tanto o cliente que indicou quanto o indicado receberão um desconto (a ser definido) na contratação do seguro após aprovação da indicação.
* **Notificação:**  Após aprovação da indicação, o cliente que indicou receberá um push de notificação parabenizando-o pela indicação.
* **Notificação Indicado:** Após aprovação da indicação, o cliente indicado receberá um push de notificação contendo os dados do cliente que o indicou e informando que um consultor entrará em contato.
* **Consultor:** Um consultor entrará em contato com o cliente indicado após a aprovação da indicação.
* **Administrador:** Um administrador terá acesso a um painel administrativo para monitorar as indicações, aprovações e descontos gerados.
* **Cadastro:** Tanto o cliente que indica quanto o indicado precisam estar cadastrados no sistema.
* **Dados Pessoais:** As informações pessoais dos clientes devem ser protegidas e mantidas em conformidade com as leis de privacidade de dados.

## Restrições

* **Limite de Indicações:**  Deverá ser definido um limite máximo de indicações por cliente (indicação).
* **Tipos de Seguros:**  Inicialmente, o sistema deve suportar apenas um tipo de seguro ou um conjunto pré-definido de seguros.  Expansão para novos seguros deverá ser considerada posteriormente.
* **Desconto Máximo:**  Será definido um valor máximo de desconto aplicável.
* **Aprovação Manual:** A aprovação da indicação poderá ser manual, caso haja necessidade de validação por parte do administrador.


## Exceções

* **Indicação Rejeitada:** Se a indicação for rejeitada, nenhum desconto será aplicado e os clientes serão notificados apropriadamente. A razão da rejeição deverá ser registrada.
* **Falha na Notificação:** Em caso de falha na entrega das notificações push, um mecanismo de re-tentativa deve ser implementado.  O administrador deve ser notificado sobre falhas persistentes.
* **Dados Incompletos:** Se o cliente indicado não possuir os dados completos necessários, a indicação deverá ser pendente até que os dados sejam completados.
* **Indicação Duplicada:** Caso um mesmo cliente seja indicado por múltiplos clientes, apenas a primeira indicação aprovada será considerada.


## Decisões

* **Plataforma:** A plataforma de desenvolvimento do aplicativo será definida posteriormente.
* **Integração com sistema de seguros:** A integração com o sistema de seguros existente será planejada e implementada em fases.
* **Tipos de Notificações:** O design e conteúdo das notificações push serão definidos em conjunto com a equipe de UX/UI.
* **Sistema de Pontuação:** A possibilidade de implementação de um sistema de pontuação para clientes que indicam será avaliada em um futuro próximo.
