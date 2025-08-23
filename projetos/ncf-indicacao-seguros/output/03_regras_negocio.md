## Regras de Negócio

* **Indicação:** Um cliente (Indicação) pode indicar um amigo ou parente (Indicado) para contratar um seguro através do aplicativo.
* **Aprovação:** A indicação precisa ser aprovada pela NCF Indicação Seguros para que o cliente (Indicação) receba o desconto e o indicado receba as informações.  A aprovação se dará após a conclusão do processo de contratação do seguro pelo indicado.
* **Desconto:**  O cliente (Indicação) receberá um desconto pré-determinado no seu próximo seguro ou um benefício equivalente, após a aprovação da indicação e contratação do seguro pelo indicado. O valor do desconto deve ser definido e configurado no sistema.
* **Notificações:** O cliente (Indicação) receberá uma notificação push ao aprovar a indicação. O indicado receberá uma notificação push com informações do cliente que o indicou e a informação de que um consultor entrará em contato.
* **Cadastro:** O Indicado precisa realizar o cadastro completo no aplicativo para que a indicação seja validada e o processo de contratação do seguro possa ser iniciado.
* **Consultor:** Um consultor entrará em contato com o Indicado após a notificação push.
* **Limite de Indicações:** Definir se existirá um limite de indicações por cliente (Indicação) em um período de tempo determinado.
* **Tipos de Seguro:** Definir os tipos de seguros aplicáveis à promoção de indicações.
* **Registro de Indicações:** Todas as indicações, sua aprovação ou rejeição, e o desconto concedido devem ser registrados no sistema.

## Restrições

* O sistema deve garantir a segurança e privacidade dos dados dos clientes.
* O sistema deve ser escalável para suportar um grande número de usuários e indicações.
* A integração com o sistema de seguros da NCF deve ser estável e confiável.
* O sistema deve atender aos requisitos legais e regulatórios aplicáveis.

## Exceções

* **Indicação Rejeitada:** Se a indicação for rejeitada, o cliente (Indicação) não receberá o desconto e o indicado não receberá informações adicionais. Uma mensagem explicando a rejeição deve ser enviada.
* **Falha na Notificação:** Em caso de falha na entrega das notificações push, o sistema deve registrar a falha e tentar novamente posteriormente.
* **Cadastro Incompleto:** Se o Indicado não completar o cadastro, a indicação será considerada pendente até que o cadastro esteja completo.  
* **Erro no Processo de Contratação do Indicado:** Se o indicado não concluir a contratação do seguro, a indicação não será validada e o desconto não será concedido.


## Decisões

* **Sistema de Notificações:** Utilizar um sistema de notificações push confiável e escalável.
* **Integração com Sistema de Seguros:** Definir a forma de integração com o sistema de seguros existente da NCF.
* **Gestão de Descontos:** Implementar um sistema de gestão de descontos que permita definir e configurar os valores de desconto para diferentes tipos de seguros.
* **Gestão de Usuários:** Utilizar um sistema de autenticação e autorização robusto e seguro.
* **Plataforma de Desenvolvimento:** Definir a plataforma de desenvolvimento (ex: iOS, Android, Web).
* **Banco de Dados:** Definir o banco de dados a ser utilizado.

