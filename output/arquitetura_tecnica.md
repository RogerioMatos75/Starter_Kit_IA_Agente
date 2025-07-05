# Arquitetura

O aplicativo "NCFSegurosIndico" seguirá uma arquitetura cliente-servidor, com um frontend baseado em React e um backend baseado em Node.js com Express. A comunicação entre o frontend e o backend será feita através de uma API RESTful. O banco de dados relacional PostgreSQL será utilizado para armazenar informações persistentes.  O Firebase Cloud Messaging (FCM) será utilizado para o envio de notificações push.

# Tecnologias

* **Frontend:** React, React Router, CSS Modules (ou Styled-Components), Axios (ou Fetch API)
* **Backend:** Node.js, Express.js, PostgreSQL, bcrypt (para hashing de senhas), jsonwebtoken (para JWT), Firebase Admin SDK (para FCM)
* **Banco de Dados:** PostgreSQL
* **Notificações Push:** Firebase Cloud Messaging (FCM)
* **Testes:** Jest, React Testing Library, Cypress (opcional)
* **Deploy:** Netlify, Vercel ou Firebase Hosting

# Integrações

* **Firebase Cloud Messaging (FCM):** Para envio de notificações push.
* **PostgreSQL:** Para persistência de dados.

# Fluxos Principais

1. **Indicação:** O usuário acessa o aplicativo, preenche um formulário com os dados do amigo indicado e envia.
2. **Backend Processamento:** O backend valida os dados, cria uma nova indicação no banco de dados e envia uma notificação push para o administrador.
3. **Administração:** O administrador revisa a indicação no painel e confirma ou rejeita. Se confirmada, uma notificação push é enviada ao usuário.
4. **Contratação:** Se o indicado contratar o seguro, o administrador registra a contratação no sistema. O desconto do usuário que indicou é atualizado.
5. **Desconto:** O desconto é calculado baseado no número de indicações válidas e contratações.