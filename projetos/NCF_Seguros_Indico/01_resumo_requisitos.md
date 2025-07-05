## Resumo do Domínio - NCFSegurosIndico

Este documento resume o domínio do projeto NCFSegurosIndico, um Progressive Web App (PWA) para indicação de seguros com sistema de gameficação.

**Objetivo Principal:** Desenvolver um PWA que permita aos clientes existentes da NCF Seguros indicarem novos clientes, recompensando-os com descontos progressivos em suas apólices.

**Atores Principais:**

* **Cliente Existente (Indicação):** Usuário do aplicativo que indica novos clientes.
* **Novo Cliente (Indicado):** Pessoa indicada pelo cliente existente para contratar um seguro.
* **Administrador NCF Seguros:** Usuário com acesso ao painel administrativo para monitorar indicações, confirmar contratações e gerenciar descontos.

**Entidades Principais:**

* **Usuário:** Representa um cliente existente da NCF Seguros com informações de login e descontos acumulados.
* **Indicação:** Registra uma indicação feita por um cliente, incluindo informações do cliente que indicou e do cliente indicado.
* **Desconto:** Representa o desconto aplicado na apólice do cliente existente, progressivamente acumulado com cada indicação válida.
* **Notificação:**  Mensagem enviada para clientes e administradores via push notificações.

**Fluxo de Trabalho Principal:**

1. O cliente existente acessa o aplicativo NCFSegurosIndico e indica um novo cliente através de um formulário.
2. O novo cliente realiza a contratação do seguro.
3. A administração confirma a contratação.
4. O cliente existente recebe um desconto progressivo em sua apólice.
5. Clientes e administradores recebem notificações sobre o status das indicações e descontos.

**Tecnologias:**

* **Frontend:** React
* **Backend:** Node.js, Express
* **Banco de Dados:** PostgreSQL
* **Notificações Push:** Firebase Cloud Messaging (FCM)
* **Autenticação:** JWT

**Funcionalidades do MVP:**

* Formulário de indicação.
* Painel administrativo para monitoramento e gestão.
* Sistema de login com JWT.
* Sistema de descontos progressivos.
* Notificações push para clientes e administradores.

**Funcionalidades Excluídas do MVP:**

* Relatórios detalhados.
* Integração com sistema CRM da seguradora.
