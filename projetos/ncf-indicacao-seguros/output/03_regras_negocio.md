## Regras de Negócio

* **Indicação:** Um cliente (Indicador) pode indicar um amigo ou parente (Indicado) para se tornar cliente do NCF Seguros.
* **Aprovação:** A indicação precisa ser aprovada pelo sistema, considerando critérios de elegibilidade (a serem definidos em regras futuras, como idade, localização, etc.).
* **Desconto:** Após a aprovação da indicação e a efetivação da compra do seguro pelo Indicado, o Indicador receberá um desconto pré-definido em sua próxima renovação de seguro.  A porcentagem do desconto será definida pela administração.
* **Notificações:** O Indicador receberá uma notificação push ao ser aprovada a indicação. O Indicado receberá uma notificação push com os dados do Indicador e a informação de que um consultor entrará em contato.
* **Consultor:** Um consultor entrará em contato com o Indicado após a aprovação da indicação para concluir o processo de contratação do seguro.
* **Cadastro do Indicado:** O Indicado precisará fornecer informações para cadastro no sistema.
* **Limite de Indicações:** Poderá existir um limite máximo de indicações por Indicador em um período determinado (a ser definido).
* **Fraudes:** O sistema deve contemplar mecanismos para evitar fraudes, como validação de dados e monitoramento de padrões suspeitos.


## Restrições

* **Integração com sistemas externos:**  A integração com sistemas de pagamento e de validação de dados precisa ser considerada, impactando o tempo de desenvolvimento e possíveis pontos de falha.
* **Plataformas:** O aplicativo precisa ser compatível com as plataformas iOS e Android.
* **Escalabilidade:** O sistema deve ser escalável para atender a um número crescente de usuários e indicações.
* **Segurança de dados:** A segurança dos dados dos usuários é crucial e precisa ser priorizada.


## Exceções

* **Indicação rejeitada:** Se a indicação for rejeitada, tanto o Indicador quanto o Indicado receberão notificações explicando o motivo da rejeição.
* **Falha na notificação:** Caso haja falha na entrega das notificações push, um registro de erro deve ser gerado e um mecanismo de reenvio deve ser implementado.
* **Dados inválidos:** Caso o Indicado forneça dados inválidos durante o cadastro, o sistema deve alertá-lo e solicitar a correção das informações.
* **Indicado já cliente:** Se o Indicado já for cliente, o sistema deve identificar isso e realizar o tratamento adequado, podendo ou não creditar o desconto ao Indicador, de acordo com regra de negócio a ser definida.


## Decisões

* **Tecnologia:** Será utilizada uma tecnologia específica para o desenvolvimento do aplicativo e do backend (a ser definida).
* **Desconto:** O valor do desconto para o Indicador será definido pela administração e poderá ser alterado ao longo do tempo.
* **Limite de Indicações:** A implementação de um limite de indicações por Indicador será considerada em uma fase posterior do projeto.
* **Integrações:** As integrações necessárias com sistemas externos serão definidas e detalhadas em documentos separados.
