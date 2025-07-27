# 02_arquitetura_tecnica.md

## Arquitetura

Será utilizada uma arquitetura de microsserviços para garantir escalabilidade, manutenibilidade e flexibilidade.  Os microsserviços principais serão:

* **Serviço de Usuário:** Gerenciamento de usuários (Indicadores e Indicados), autenticação e autorização.
* **Serviço de Seguro:**  Catálogo de seguros e informações relevantes.  Potencial integração com API externa de seguradoras.
* **Serviço de Indicação:** Gerenciamento de indicações, cálculo de descontos e rastreio.
* **Serviço de Notificação:**  Envio de notificações push (Android e iOS).
* **Serviço de Gamificação:**  Sistema de pontos e recompensas para indicadores.
* **Gateway API:**  Ponto único de entrada para todos os microsserviços, gerenciamento de rotas e segurança.


## Tecnologias

* **Frontend:** React Native (para desenvolvimento cross-platform - Android e iOS), podendo ser considerado Flutter como alternativa.
* **Backend:** Node.js com Express.js (para agilidade e escalabilidade).  Alternativas: Python com Flask/Django ou Go.
* **Banco de Dados:** PostgreSQL (para relacionamentos complexos e escalabilidade). Alternativa: MongoDB (NoSQL para maior flexibilidade, se necessário).
* **Mensageria:** RabbitMQ ou Kafka (para comunicação assíncrona entre microsserviços).
* **Cloud Provider:** AWS, Google Cloud Platform ou Azure (para hospedagem e escalabilidade).
* **Notificações Push:** Firebase Cloud Messaging (FCM) ou APNs (Apple Push Notification service).


## Integrações

* **API de Seguradoras:** Integração com APIs de seguradoras para obtenção de informações de seguros e processamento de descontos (a definir com o cliente).
* **Serviços de Pagamento:** Integração com gateways de pagamento para processamento de pagamentos (a definir com o cliente).


## Fluxos Principais

**1. Fluxo de Indicação:**

1. O Indicador acessa o aplicativo e seleciona um seguro para indicar.
2. O Indicador insere os dados do Indicado (nome, telefone, email).
3. O serviço de Usuário valida os dados do Indicador e do Indicado.
4. O serviço de Indicação cria um registro de indicação.
5. O serviço de Notificação envia uma notificação push ao Indicado com os detalhes da indicação e do Indicador.
6. O Indicado pode acessar o aplicativo e visualizar a indicação.

**2. Fluxo de Aprovação e Recompensa:**

1. O Indicado realiza a contratação do seguro.
2. A seguradora confirma a contratação (via integração com a API da seguradora).
3. O serviço de Indicação atualiza o status da indicação para "Aprovada".
4. O serviço de Gamificação atualiza os pontos do Indicador.
5. O serviço de Notificação envia uma notificação push ao Indicador confirmando a indicação aprovada e o desconto para o Indicado.

**3. Fluxo de Gerenciamento de Indicações:**

1. O Indicador acessa o aplicativo e visualiza suas indicações (em andamento, aprovadas, recusadas).
2. O serviço de Indicação retorna as informações das indicações.

**4. Fluxo de Resgate de Desconto:**

1. O Indicado acessa o aplicativo e visualiza o desconto disponível.
2. O Indicado utiliza o código do desconto no processo de contratação do seguro na plataforma da seguradora (via integração).

**Observações:** Todos os fluxos devem incluir tratamento de erros e logs adequados.  A segurança da aplicação deve ser priorizada com medidas de autenticação e autorização robustas.
