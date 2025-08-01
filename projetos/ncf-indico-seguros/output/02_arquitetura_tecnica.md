# 02_arquitetura_tecnica.md

## Arquitetura

O sistema NCF-Indico-Seguros será arquitetado utilizando uma abordagem de microsserviços, permitindo escalabilidade e manutenção independente de cada componente.  Os microsserviços se comunicarão através de uma API RESTful.  Um gateway de API será utilizado para roteamento e gerenciamento de requisições.  A arquitetura será baseada em nuvem (ex: AWS, Google Cloud ou Azure), garantindo alta disponibilidade e escalabilidade.

## Tecnologias

* **Frontend (Mobile):** React Native (para desenvolvimento cross-platform iOS e Android), permitindo o compartilhamento de código e reduzindo o tempo de desenvolvimento.
* **Backend:** Node.js com Express.js (para construção da API RESTful), oferecendo performance e escalabilidade.
* **Banco de Dados:** PostgreSQL (para armazenamento de dados relacionais), escolhido por sua robustez, escalabilidade e compatibilidade com o ecossistema.  Será utilizada uma abordagem de banco de dados separado para cada microsserviço, promovendo independência e isolamento de falhas.
* **Mensageria:** RabbitMQ ou Kafka (para comunicação assíncrona entre microsserviços), garantindo desacoplamento e melhor performance.
* **Notificações Push:** Firebase Cloud Messaging (FCM) ou AWS SNS (para envio de notificações push para usuários iOS e Android).
* **Gestão de APIs:** Kong ou Apigee (para gerenciamento e monitoramento da API).
* **Testes:** Jest e Cypress (para testes unitários e de integração).
* **Infraestrutura:**  Plataforma em nuvem (AWS, Google Cloud ou Azure) com serviços de containerização (Kubernetes) e balanceamento de carga.

## Integrações

* **Integração com sistema legado da NCF:**  Será necessário um estudo detalhado da arquitetura atual da NCF para definir a melhor estratégia de integração.  APIs RESTful serão utilizadas preferencialmente.
* **Integração com gateway de pagamento (se aplicável):**  Escolha da solução dependerá das necessidades específicas da NCF.  A integração será feita através de APIs.

## Fluxos Principais

**1. Fluxo de Cadastro e Login:**

O usuário acessa o aplicativo e realiza o cadastro ou login via API. As credenciais são validadas e um token JWT é gerado para autenticação em requisições subsequentes.

**2. Fluxo de Criação de Indicação:**

O usuário autenticado cria uma indicação através da API, informando os dados do indicado.  Um ID único é gerado para a indicação e o status é definido como "pendente".  Uma notificação push é enviada para o indicado.

**3. Fluxo de Notificação Push:**

O sistema envia notificações push utilizando FCM ou AWS SNS para informar sobre novas indicações ou status das mesmas.

**4. Fluxo de Gerenciamento do Sistema (Administrador):**

O administrador acessa um painel web (desenvolvido com React ou similar) para monitorar o desempenho do programa, gerar relatórios e administrar o sistema.  Este painel interage com a API backend para obter os dados necessários.

**5. Fluxo de Aplicação de Desconto:**

Após a aprovação da indicação, o sistema aplica o desconto correspondente às apólices do usuário que indicou e do usuário indicado.  Este fluxo envolve integração com o sistema de gestão de apólices da NCF.

**6. Fluxo de Visualização de Informações:**

Usuários e administradores podem visualizar informações relevantes através da API, acessando dados como status da indicação, informações da apólice, etc.
