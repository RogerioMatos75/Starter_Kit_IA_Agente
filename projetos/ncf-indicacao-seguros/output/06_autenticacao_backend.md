# 06_autenticacao_backend.md

### Fluxo de Autenticação

1. **Registro:** O usuário fornece suas informações (nome, email, senha, etc.). A senha é criptografada usando um algoritmo de hash seguro (como bcrypt) antes de ser armazenada no banco de dados. Um token de confirmação de email pode ser enviado para validar o endereço de email.

2. **Login:** O usuário insere seu email e senha. O sistema verifica se o email existe no banco de dados. Se existir, a senha fornecida é comparada com a senha hash armazenada. Se corresponderem, um token JWT (JSON Web Token) é gerado e retornado ao cliente.

3. **Autenticação JWT:** Para todas as requisições subsequentes, o cliente inclui o token JWT no cabeçalho da requisição. O backend valida o token para verificar a identidade do usuário e a validade do token.

4. **Recuperação de Senha:** O usuário fornece seu email. O sistema verifica se o email existe no banco de dados. Se existir, um link de redefinição de senha é enviado para o email do usuário. O link contém um token único que permite ao usuário redefinir sua senha.

5. **Logout:** O cliente envia uma requisição de logout. O token JWT é invalidado no servidor (opcional, dependendo da implementação do JWT).


### Tecnologias/Bibliotecas

* **JWT (JSON Web Tokens):** Para autenticação sem estado.  Permite a validação do usuário sem consultas constantes ao banco de dados.
* **bcrypt:** Para criptografia segura de senhas.
* **Passport.js (ou similar):** Uma biblioteca de autenticação para Node.js que simplifica a implementação de diferentes estratégias de autenticação, incluindo JWT.  Alternativas incluem bibliotecas similares em outras linguagens (ex: Spring Security para Java).
* **Banco de dados relacional (ex: PostgreSQL, MySQL):** Para armazenar informações do usuário de forma segura e eficiente.


### Considerações de Segurança

* **Hashing de senhas:** Utilizar um algoritmo de hashing seguro e lento (como bcrypt) para proteger as senhas contra ataques de força bruta.  Nunca armazenar senhas em texto plano.
* **Proteção contra CSRF (Cross-Site Request Forgery):** Implementar medidas de proteção contra ataques CSRF, como tokens CSRF ou verificação de referer.
* **Validação de entrada:** Validar todas as entradas do usuário para prevenir injeção de código e outras vulnerabilidades.
* **HTTPS:** Utilizar HTTPS para todas as comunicações entre o cliente e o servidor para proteger as informações contra interceptação.
* **Limitação de tentativas de login:** Implementar um mecanismo de limitação de tentativas de login para evitar ataques de força bruta.
* **Gerenciamento de sessão seguro:**  Implementar mecanismos para gerenciar adequadamente as sessões, considerando timeout e logout automático.
* **Auditoria:** Registrar todas as tentativas de login e outras ações sensíveis para fins de monitoramento e segurança.
* **Segurança do armazenamento de dados:** Utilizar práticas adequadas de segurança para o armazenamento dos dados, incluindo criptografia e controle de acesso.
* **Atualizações de segurança:** Manter todas as bibliotecas e dependências atualizadas para corrigir vulnerabilidades conhecidas.
