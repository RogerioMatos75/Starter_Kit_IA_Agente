# Objetivo

Desenvolver um Progressive Web App (PWA) para a NCF Seguros que permita a indicação de seguros por parte dos clientes existentes, incentivando-os através de um sistema de gameficação baseado em descontos progressivos.

# Visão Geral

O aplicativo "NCFSegurosIndico" será um PWA que permitirá aos usuários da NCF Seguros indicarem amigos e familiares para contratação de seguros.  A cada indicação válida e posterior contratação, o usuário receberá um desconto progressivo em sua apólice, até um limite máximo.  Um painel administrativo permitirá que a NCF Seguros acompanhe as indicações, confirme as contratações e gerencie os descontos. O aplicativo utilizará notificações push para manter tanto os usuários quanto a administração informados sobre o status das indicações.

# Público-Alvo

Clientes existentes da NCF Seguros e o departamento administrativo da empresa.

# Escopo

O escopo deste projeto inclui o desenvolvimento completo do PWA, incluindo:

* **Frontend:** Desenvolvimento da interface do usuário utilizando React, incluindo formulário de indicação, painel administrativo, sistema de login e notificações push.
* **Backend:** Desenvolvimento da API RESTful utilizando Node.js e Express para gerenciar as indicações, usuários, descontos e notificações push.  Inclui integração com o Firebase Cloud Messaging (FCM).
* **Banco de Dados:** Utilização do PostgreSQL para armazenamento persistente de dados de usuários, indicações e descontos.
* **Sistema de Notificações Push:** Implementação de notificações push para usuários e administradores via FCM.
* **Autenticação:** Implementação de um sistema de autenticação seguro utilizando JWT (JSON Web Tokens).
* **Testes:** Implementação de testes unitários, de integração e end-to-end para garantir a qualidade do código.
* **Deploy:** Deploy do aplicativo em uma plataforma como Netlify, Vercel ou Firebase Hosting.

**Funcionalidades Excluídas do MVP:**  Relatórios detalhados, integração com o sistema CRM da seguradora. Estas serão consideradas em iterações futuras.