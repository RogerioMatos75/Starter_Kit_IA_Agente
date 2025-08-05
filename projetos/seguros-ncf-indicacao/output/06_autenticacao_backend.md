# 06_autenticacao_backend.md

### Fluxo de Autenticação

1. **Registro:** O usuário fornece um endereço de email, senha e outros dados relevantes (nome, telefone, etc.). A senha é criptografada usando um algoritmo de hash seguro (ex: bcrypt) antes de ser armazenada no banco de dados. Um email de verificação pode ser enviado para confirmar o endereço de email.

2. **Login:** O usuário fornece seu endereço de email e senha. O sistema verifica se o email existe no banco de dados.  Se existir, a senha fornecida é comparada com a senha criptografada armazenada, utilizando o mesmo algoritmo de hash usado no registro. Se a comparação for bem-sucedida, um token JWT (JSON Web Token) é gerado e retornado ao cliente.

3. **Autenticação com JWT:** Em todas as requisições subsequentes, o cliente inclui o token JWT no cabeçalho da requisição. O backend valida o token, verificando sua assinatura e expiração. Se o token for válido, o usuário é autenticado.

4. **Recuperação de Senha:** O usuário fornece seu endereço de email. O sistema verifica se o email existe no banco de dados. Se existir, um link de redefinição de senha é enviado para o endereço de email fornecido. O link contém um token temporário que permite ao usuário redefinir sua senha.

5. **Logout:** O cliente envia uma requisição de logout. O token JWT é invalidado no backend (por exemplo, adicionando-o a uma lista negra).


### Tecnologias/Bibliotecas

* **JWT (JSON Web Tokens):** Para autenticação sem estado, garantindo segurança e facilidade de implementação.
* **bcrypt:** Para o hash seguro de senhas, protegendo-as contra ataques de força bruta.
* **Node.js com Express.js (ou framework similar):** Para o backend.
* **Passport.js (ou similar):** Framework de autenticação para simplificar a implementação de estratégias de autenticação.
* **Banco de dados relacional (ex: PostgreSQL, MySQL) ou NoSQL (ex: MongoDB):** Para armazenar informações de usuários.


### Considerações de Segurança

* **Hashing de senhas:** Usar um algoritmo de hash seguro e robusto como bcrypt, com um custo computacional alto para dificultar ataques de força bruta.  Nunca armazenar senhas em texto plano.
* **Proteção contra CSRF (Cross-Site Request Forgery):** Implementar tokens CSRF para proteger contra ataques CSRF.
* **Validação de entrada:** Validar todas as entradas do usuário para prevenir injeção de SQL e outras vulnerabilidades.
* **HTTPS:** Usar HTTPS para garantir a comunicação segura entre o cliente e o servidor.
* **Limitação de tentativas de login:** Implementar um mecanismo para bloquear contas após várias tentativas de login incorretas.
* **Gestão de tokens JWT:** Implementar mecanismos para revogar tokens e gerenciar sua expiração.
* **Auditoria:** Registrar todas as tentativas de login, incluindo as bem-sucedidas e as malsucedidas, para fins de auditoria e detecção de intrusão.
* **Proteção contra ataques DDoS:** Implementar medidas para mitigar ataques de negação de serviço distribuído.
* **Atualizações de segurança:** Manter todas as dependências de software atualizadas com as últimas correções de segurança.
