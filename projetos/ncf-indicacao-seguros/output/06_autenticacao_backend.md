# 06_autenticacao_backend.md

### Fluxo de Autenticação

**1. Registro:**

* O usuário fornece suas informações (nome, email, senha, etc.).
* A senha é criptografada usando um algoritmo de hash seguro (ex: bcrypt) antes de ser armazenada.
* Um token de verificação de email é gerado e enviado para o endereço fornecido.
* Após a verificação do email, o usuário pode acessar o sistema.

**2. Login:**

* O usuário fornece seu email e senha.
* A senha fornecida é comparada com o hash armazenado no banco de dados.
* Se a senha estiver correta, um JSON Web Token (JWT) é gerado e retornado ao cliente.
* O JWT contém informações sobre o usuário (ID, tipo de usuário, etc.) e um tempo de expiração.
* O cliente deve enviar o JWT em cada requisição subsequente para autenticação.

**3. Recuperação de Senha:**

* O usuário fornece seu email.
* Um token de recuperação de senha é gerado e enviado para o endereço fornecido.
* O usuário pode usar o token para redefinir sua senha.  A nova senha é então criptografada e armazenada.

**4. Logout:**

* O usuário solicita o logout.
* O JWT é invalidado (pode ser feito através de uma lista negra de tokens ou por tempo de expiração).


### Tecnologias/Bibliotecas

* **JWT (JSON Web Token):** Para autenticação e autorização.  Oferece uma maneira segura e eficiente de gerenciar a sessão do usuário.
* **bcrypt:** Para criptografar as senhas antes de armazená-las no banco de dados.
* **Passport.js (opcional):** Uma biblioteca Node.js que simplifica a implementação de diferentes estratégias de autenticação, incluindo JWT.  Facilita a integração com outras bibliotecas.
* **Biblioteca de autenticação específica do framework:**  A escolha dependerá do framework backend usado (ex: Spring Security para Java, ASP.NET Core Identity para .NET).


### Considerações de Segurança

* **Hashing de Senhas:** Utilizar um algoritmo de hash unidirecional robusto e lento (como bcrypt) para proteger as senhas contra ataques de força bruta.  Nunca armazenar senhas em texto simples.
* **Proteção contra CSRF (Cross-Site Request Forgery):** Implementar tokens CSRF para proteger contra ataques CSRF.  O token deve ser gerado de forma única para cada usuário e sessão.
* **Validação de entrada:** Validar todos os dados de entrada do usuário para prevenir injeções de código e outros ataques.
* **Limitação de tentativas de login:** Implementar um mecanismo de bloqueio de conta após várias tentativas de login incorretas.
* **HTTPS:** Usar HTTPS para proteger a comunicação entre o cliente e o servidor.
* **Gerenciamento de sessão seguro:** Implementar um mecanismo seguro de gerenciamento de sessão, incluindo o uso de cookies HTTPOnly e Secure.
* **Auditoria:** Registrar todas as tentativas de login e acesso ao sistema para fins de monitoramento e auditoria de segurança.
* **Atualizações de segurança:** Manter todas as bibliotecas e dependências atualizadas para corrigir vulnerabilidades conhecidas.
* **Proteção contra ataques DDoS:** Implementar medidas para mitigar ataques de negação de serviço distribuído.


