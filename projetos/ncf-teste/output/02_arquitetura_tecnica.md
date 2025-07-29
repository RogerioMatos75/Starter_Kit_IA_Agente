# 02_arquitetura_tecnica.md

## Arquitetura

Será utilizada uma arquitetura de microsserviços para garantir escalabilidade, manutenabilidade e flexibilidade.  Os microsserviços principais serão:

* **Serviço de Usuário:** Gerenciamento de usuários (Indicadores e Indicados), autenticação e autorização.
* **Serviço de Seguro:**  Gestão de informações de seguros, integração com APIs externas (se necessário).
* **Serviço de Indicação:**  Registro e gerenciamento de indicações, cálculo de descontos e recompensas.
* **Serviço de Notificação:**  Envio de notificações push (Android e iOS).
* **Gateway API:**  Ponto único de entrada para todos os microsserviços, roteamento de requisições e balanceamento de carga.


## Tecnologias

* **Frontend:** React Native (para desenvolvimento cross-platform, iOS e Android), podendo ser considerado Flutter como alternativa.
* **Backend:** Node.js com Express.js (para agilidade e escalabilidade).  Alternativas como Python com Django/Flask também podem ser consideradas.
* **Banco de Dados:** PostgreSQL (relacional, robusto e escalável). NoSQL (como MongoDB) pode ser considerado como complemento para dados não estruturados, dependendo da complexidade do sistema de gamificação.
* **Mensageria:** RabbitMQ ou Kafka para comunicação assíncrona entre microsserviços (para envio de notificações, por exemplo).
* **Cloud Provider:** AWS ou Google Cloud Platform (GCP), a escolha dependerá de critérios de custo e infraestrutura.
* **Notificações Push:** Firebase Cloud Messaging (FCM) ou serviço equivalente para iOS e Android.


## Integrações

* **API de Seguros (se necessário):** Integração com API de terceiros para consulta de informações de seguros e processamento de descontos.  A especificação da API dependerá do fornecedor escolhido.
* **Serviço de Pagamento (futuro):**  Integração com um serviço de pagamento para gerenciar o pagamento de mensalidades (considerado para futuras funcionalidades).


## Fluxos Principais

**Fluxo de Indicação de Seguro:**

1. O Indicador acessa o aplicativo e seleciona um seguro a ser indicado.
2. O Indicador insere os dados do Indicado (nome, contato).
3. O Serviço de Usuário verifica se o Indicado já existe. Se não, cria um novo usuário.
4. O Serviço de Indicação registra a nova indicação, vinculando o Indicador e o Indicado.
5. O Serviço de Notificação envia uma notificação push para o Indicado, com informações sobre a indicação.
6. O Indicado aceita a indicação e, após aprovação, o serviço de Seguro calcula o desconto.
7. O Serviço de Notificação envia uma notificação push ao Indicador confirmando a indicação e ao Indicado com as informações sobre o desconto e próxima etapa.

**Fluxo de Gerenciamento de Indicações:**

1. O Indicador acessa o aplicativo e visualiza suas indicações.
2. O Serviço de Indicação recupera as informações das indicações do usuário.
3. O aplicativo apresenta ao usuário um painel com suas indicações, status e recompensas.

**Fluxo de Resgate de Desconto:**

1. O Indicado acessa o aplicativo.
2. O Serviço de Indicação verifica as indicações aprovadas e o desconto disponível para o Indicado.
3. O aplicativo exibe o desconto disponível e o processo para resgate (fluxos de pagamento futuros).


