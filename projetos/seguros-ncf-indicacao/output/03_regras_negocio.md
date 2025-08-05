## Regras de Negócio

* **Indicação:** Um cliente (Indicande) pode indicar amigos e parentes para contratar um seguro NCF.
* **Aprovação:** A indicação só será considerada válida após a aprovação da solicitação de seguro do indicado.
* **Desconto:** O Indicande receberá um desconto pré-definido no seu seguro após a aprovação da indicação. O valor do desconto será definido pela empresa e poderá variar.
* **Notificações:** Após a aprovação da indicação, o Indicande receberá uma notificação push parabenizando-o. O indicado receberá uma notificação push informando quem o indicou e que um consultor entrará em contato.
* **Consultor:** Um consultor entrará em contato com o indicado após a aprovação da sua solicitação de seguro.
* **Cadastro:** O Indicande e o Indicado devem estar devidamente cadastrados no sistema.
* **Limite de Indicações:**  Deverá ser definido um limite máximo de indicações por Indicande em um determinado período (ex: mês).
* **Dados da Indicação:** O sistema deve registrar os dados da indicação, incluindo o Indicande, o Indicado e a data da aprovação.
* **Relatórios:** O sistema deve gerar relatórios sobre as indicações, incluindo o número de indicações, o valor dos descontos concedidos e o número de seguros contratados por meio de indicações.


## Restrições

* **Validação de Dados:** O sistema deve validar os dados fornecidos pelo Indicande e pelo Indicado para garantir a precisão das informações.
* **Integração com Sistemas Externos:** O sistema deve se integrar com os sistemas de cadastro de clientes e de processamento de seguros.
* **Segurança:** O sistema deve garantir a segurança das informações dos clientes.
* **Escalabilidade:** O sistema deve ser escalável para suportar um grande número de usuários e indicações.


## Exceções

* **Indicação Inválida:** Se a indicação for inválida (ex: dados incorretos, indicado já cliente), o sistema deve notificar o Indicande e o Indicado.
* **Rejeição da Solicitação:** Se a solicitação de seguro do indicado for rejeitada, a indicação não será considerada válida e o Indicande não receberá o desconto.
* **Falha na Notificação:**  Em caso de falha no envio da notificação push, o sistema deve registrar a falha e tentar novamente posteriormente.  Um mecanismo de notificação alternativa (e-mail, SMS) deve ser considerado.
* **Fraude:**  O sistema deve incluir mecanismos para detectar e prevenir fraudes relacionadas a indicações.


## Decisões

* **Plataforma:** Definir a plataforma de desenvolvimento do aplicativo (nativo, híbrido, web).
* **Tecnologia:** Escolher as tecnologias para o desenvolvimento do aplicativo e da parte administrativa.
* **Desconto:** Definir o valor e a periodicidade do desconto para o Indicande.
* **Limite de Indicações:** Definir o limite máximo de indicações por Indicande em um determinado período.
* **Integrações:** Definir quais sistemas externos serão integrados ao sistema.
* **Metodologia de Desenvolvimento:** Escolher a metodologia de desenvolvimento ágil a ser utilizada.
