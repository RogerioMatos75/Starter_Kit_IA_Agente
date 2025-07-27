# 02_arquitetura_tecnica.md

## Arquitetura

Será utilizada uma arquitetura de microsserviços para garantir escalabilidade, manutenabilidade e flexibilidade.  Os microsserviços serão:

* **Serviço de Usuário:** Gerenciamento de usuários (Indicadores e Indicados), autenticação e autorização.
* **Serviço de Seguro:** Catálogo de seguros, informações sobre os seguros.  Possibilidade de integração com API externa de seguradoras.
* **Serviço de Indicação:**  Gerencia o processo de indicação, incluindo o registro, aprovação e acompanhamento.
* **Serviço de Notificação:** Envio de notificações push para Indicadores e Indicados.
* **Serviço de Gamificação:**  Gerencia o sistema de pontos e recompensas.
* **Serviço de Desconto:**  Gerencia a aplicação de descontos aos indicados.
* **Gateway de API:**  Ponto de entrada único para todos os microsserviços.


## Tecnologias

* **Frontend:** React Native (para aplicativo móvel multiplataforma) e React (para possível web app).
* **Backend:** Node.js com Express.js (por sua escalabilidade e grande comunidade).
* **Banco de Dados:** PostgreSQL (relacional, robusto e escalável) com Redis para cache.
* **Mensageria:** RabbitMQ (para comunicação assíncrona entre microsserviços).
* **Cloud:** AWS ou Google Cloud Platform (para hospedagem e escalabilidade).
* **Notificações Push:** Firebase Cloud Messaging (FCM) ou solução similar.


## Integrações

* **API de Seguradoras:** Integração com APIs de seguradoras para obter informações sobre os seguros e processar as indicações (se necessário).  A integração dependerá da escolha da(s) seguradora(s) parceira(s).
* **Serviço de Pagamento:**  Integração com um gateway de pagamento (ex: Stripe, PayPal) para o processamento de pagamentos (futura expansão).


## Fluxos Principais

**1. Fluxo de Indicação:**

1. O Indicador escolhe um seguro no aplicativo e indica um amigo (Indicado) fornecendo seus dados de contato.
2. O serviço de Usuário valida os dados do Indicador e do Indicado.
3. O serviço de Indicação registra a indicação.
4. O serviço de Notificação envia uma notificação push ao Indicado com informações sobre a indicação e o Indicador.
5. O Indicado pode acessar o aplicativo e visualizar a proposta.
6.  Após a aprovação do seguro pelo Indicado, o serviço de Indicação atualiza o status da indicação.
7. O serviço de Notificação envia uma notificação push ao Indicador confirmando a indicação bem-sucedida.
8. O serviço de Gamificação atribui pontos ao Indicador.


**2. Fluxo de Resgate de Desconto:**

1. Após a aprovação da indicação, o serviço de Desconto calcula o desconto para o Indicado.
2. O Indicado pode visualizar o desconto no aplicativo.
3. O Indicado utiliza o desconto ao adquirir o seguro.


**3. Fluxo de Gerenciamento de Indicações:**

1. O Indicador acessa sua conta no aplicativo.
2. O serviço de Usuário autentica o Indicador.
3. O serviço de Indicação retorna as informações sobre as indicações do Indicador (status, data, etc.).
4. O serviço de Gamificação retorna os pontos acumulados pelo Indicador.

**Observações:** Todos os serviços comunicam-se através da mensageria (RabbitMQ) para garantir a resiliência e a escalabilidade do sistema. A segurança será garantida através de autenticação robusta e controle de acesso em cada microsserviço.
