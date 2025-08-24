# 06_autenticacao_backend.md

### Fluxo de Autenticação

1. **Registro:** O usuário fornece suas informações (nome, email, senha, etc.). A senha é criptografada usando um algoritmo de hash seguro (como bcrypt) antes de ser armazenada no banco de dados.  Um email de confirmação pode ser enviado para validação da conta.

2. **Login:** O usuário insere seu email e senha. O sistema recupera a senha hash do banco de dados e compara com a hash da senha fornecida pelo usuário. Se corresponderem, um token JWT (JSON Web Token) é gerado e retornado ao cliente.

3. **Autenticação com JWT:**  Para cada requisição subsequente, o cliente envia o token JWT no cabeçalho da requisição (ex: `Authorization: Bearer <token>`). O backend verifica a validade e assinatura do token. Se válido, o usuário é autenticado.

4. **Recuperação de Senha:** O usuário fornece seu email. O sistema gera um token de recuperação de senha e envia um email com um link para redefinir a senha.  O link contém o token, que é usado para verificar a identidade do usuário e permitir que ele defina uma nova senha.

5. **Logout:** O cliente envia uma requisição de logout, invalidando o token JWT atual.

### Tecnologias/Bibliotecas

* **JWT (JSON Web Tokens):** Para autenticação sem estado e gerenciamento de sessões.
* **bcrypt:** Para hashing de senhas, garantindo que as senhas armazenadas não sejam facilmente recuperáveis, mesmo em caso de violação de dados.
* **Passport.js (ou similar):** Uma biblioteca Node.js para autenticação, simplificando a implementação de estratégias de autenticação como JWT.  Alternativas incluem bibliotecas específicas para o framework escolhido (ex: Spring Security para Java).
* **Banco de dados relacional (ex: PostgreSQL, MySQL) ou NoSQL (ex: MongoDB):** Para armazenar informações de usuários e senhas com segurança.

### Considerações de Segurança

* **Hashing de senhas:** Utilizar um algoritmo de hash seguro e lento (como bcrypt) para proteger as senhas contra ataques de força bruta.  Nunca armazenar senhas em texto plano.
* **Proteção contra CSRF (Cross-Site Request Forgery):** Implementar tokens CSRF para evitar ataques CSRF, principalmente em formulários de autenticação e outras ações sensíveis.
* **Validação de entrada:** Validar todos os dados de entrada do usuário para prevenir injeção de SQL e outros ataques.
* **HTTPS:** Usar HTTPS para criptografar a comunicação entre o cliente e o servidor, protegendo as informações de autenticação.
* **Limitação de tentativas de login:** Implementar um mecanismo para bloquear contas após várias tentativas de login incorretas, para mitigar ataques de força bruta.
* **Gerenciamento de tokens JWT:**  Definir tempo de expiração para os tokens JWT, e implementar mecanismos de revogação de tokens em caso de necessidade (ex: logout, suspeita de comprometimento).
* **Proteção contra injeção:**  Sanitizar e validar todas as entradas do usuário para proteger contra injeção de código (SQL injection, XSS).
* **Auditoria:** Registrar todas as tentativas de login, sucesso ou falha, para fins de monitoramento e detecção de intrusões.
* **Segurança de armazenamento de dados:** Utilizar práticas seguras para o armazenamento de dados sensíveis, incluindo criptografia em repouso e controle de acesso.
