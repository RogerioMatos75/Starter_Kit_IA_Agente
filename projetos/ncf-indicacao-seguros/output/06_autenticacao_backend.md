# 06_autenticacao_backend.md

### Fluxo de Autenticação

**Registro:**

1. O usuário fornece seu nome de usuário (e-mail), senha e outros dados relevantes (nome completo, telefone, etc.).
2. A senha é criptografada usando um algoritmo de hash unidirecional forte (ex: bcrypt).
3. Os dados do usuário são armazenados no banco de dados.
4. Um token de confirmação de e-mail é enviado para o endereço de e-mail do usuário.
5. O usuário clica no link de confirmação para ativar sua conta.

**Login:**

1. O usuário fornece seu nome de usuário (e-mail) e senha.
2. A senha fornecida é comparada com a senha hash armazenada no banco de dados.
3. Se a senha corresponder, um JWT (JSON Web Token) é gerado e retornado ao usuário.
4. O JWT contém informações sobre o usuário (ID, nome de usuário, tipo de usuário - administrador, segurado, etc.) e expira após um determinado período de tempo.

**Recuperação de Senha:**

1. O usuário fornece seu nome de usuário (e-mail).
2. Um e-mail com um link de redefinição de senha é enviado para o endereço de e-mail do usuário.
3. O link de redefinição contém um token único que expira após um determinado período de tempo.
4. O usuário é redirecionado para uma página onde pode definir uma nova senha.
5. A nova senha é criptografada e armazenada no banco de dados.


### Tecnologias/Bibliotecas

* **Autenticação:** JWT (JSON Web Tokens) para gerenciamento de sessão.
* **Hashing de Senhas:** bcrypt para criptografar senhas de forma segura.
* **Framework/Biblioteca de Autenticação:** Passport.js (Node.js) ou uma biblioteca equivalente para o framework escolhido (ex: Spring Security para Java).
* **Banco de Dados:** PostgreSQL ou MySQL para armazenar informações do usuário.


### Considerações de Segurança

* **Hashing de Senhas:** Utilizar um algoritmo de hash forte e unidirecional (bcrypt) com um custo de hashing adequado.  Armazenar apenas o hash e nunca a senha em texto plano.
* **Proteção contra ataques CSRF (Cross-Site Request Forgery):** Implementar tokens CSRF em todos os formulários que modificam o estado do servidor.
* **Validação de entrada:** Validar todas as entradas do usuário para prevenir injeções de SQL e outros ataques.
* **Limitação de tentativas de login:** Implementar um mecanismo para bloquear contas após várias tentativas de login inválidas.
* **HTTPS:** Utilizar HTTPS para todas as comunicações entre o cliente e o servidor.
* **Gerenciamento de Sessões:** Implementar um mecanismo seguro de gerenciamento de sessões, utilizando JWT com tempo de vida curto e mecanismos de refresh token.
* **Auditoria:** Registrar todas as tentativas de login, incluindo as bem-sucedidas e as malsucedidas.
* **Segurança de armazenamento de dados:** Proteger o banco de dados com as melhores práticas de segurança de banco de dados, incluindo controle de acesso, criptografia e backups regulares.
* **Gestão de vulnerabilidades:** Manter as bibliotecas e frameworks atualizados para corrigir vulnerabilidades conhecidas.

