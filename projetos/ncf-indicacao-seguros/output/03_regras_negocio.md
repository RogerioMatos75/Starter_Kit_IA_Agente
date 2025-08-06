## Regras de Negócio

* **Indicação:**  Um cliente (Indicação) pode indicar um novo cliente (Indicado) para a NCF Seguros.
* **Aprovação:** A indicação precisa ser aprovada pela NCF Seguros para que o desconto seja concedido. A aprovação envolve a validação dos dados do indicado e a efetiva contratação de um seguro.
* **Desconto:**  Tanto o cliente que indicou (Indicação) quanto o cliente indicado (Indicado) receberão um desconto no seguro. O valor do desconto será definido pela NCF Seguros e pode variar.
* **Notificações:**  Após a aprovação da indicação, tanto a Indicação quanto o Indicado receberão notificações push:
    * **Indicação:** Parabéns pela indicação aprovada!
    * **Indicado:**  Você foi indicado por [Nome da Indicação]! Um consultor entrará em contato em breve.
* **Consultor:** Um consultor da NCF Seguros entrará em contato com o Indicado após a aprovação da indicação para dar andamento ao processo de contratação do seguro.
* **Limite de Indicações:**  Pode haver um limite de indicações por cliente Indicação em um determinado período de tempo (ex: 3 indicações por mês).
* **Cadastro:** O Indicado precisa se cadastrar na plataforma da NCF Seguros para que a indicação seja processada.
* **Dados da Indicação:**  O sistema deve registrar os dados da Indicação (nome, CPF, código de indicação) associados à indicação do Indicado.


## Restrições

* **Validação de Dados:** Todos os dados fornecidos pelo cliente Indicação e pelo cliente Indicado precisam ser validados antes da aprovação da indicação.
* **Segurança:**  O sistema deve garantir a segurança dos dados dos clientes, seguindo as legislações de proteção de dados vigentes (ex: LGPD).
* **Integrações:**  O sistema deve se integrar com os sistemas internos da NCF Seguros (ex: sistema de cadastro de clientes, sistema de emissão de seguros).
* **Escalabilidade:** O sistema deve ser escalável para lidar com um grande número de indicações.


## Exceções

* **Indicação Rejeitada:** Se a indicação for rejeitada, tanto o cliente Indicação quanto o Indicado devem receber uma notificação explicando o motivo da rejeição.
* **Dados Incompletos:**  Se os dados fornecidos pelo Indicado estiverem incompletos, o sistema deve solicitar as informações faltantes antes de processar a indicação.
* **Erro no Processamento:** Se houver algum erro no processamento da indicação, o sistema deve registrar o erro e notificar o administrador do sistema.
* **Indicado já Cliente:** Se o Indicado já for cliente da NCF Seguros, a indicação poderá ser processada de forma diferente, como atribuindo um desconto adicional.


## Decisões

* **Plataforma:**  A aplicação será desenvolvida para dispositivos móveis (Android e iOS).
* **Tecnologia:**  A tecnologia utilizada para o desenvolvimento da aplicação será definida em um documento separado.
* **Gestão de Descontos:** A gestão de descontos será feita pelo sistema, podendo ser configurada pelo administrador.
* **Comunicação com o Consultor:** A comunicação do Indicado com o consultor será inicialmente via telefone/e-mail.
* **Integração com CRM:** A integração com o CRM da NCF Seguros será avaliada e implementada futuramente.

