# 06_autenticacao_backend.md

## Modelo de Autenticação Backend para NCF-Indico-Seguros

### Método de Autenticação: JWT (JSON Web Token)

### Fluxo de Autenticação:

1. **Cadastro:** O usuário cria uma conta fornecendo informações necessárias (e-mail, senha, etc.). A senha é armazenada criptografada (utilizando bcrypt ou similar).
2. **Login:** O usuário fornece seu e-mail e senha. O backend verifica a senha contra a hash armazenada.
3. **Geração do JWT:** Se a autenticação for bem-sucedida, o backend gera um JWT contendo informações do usuário (ID, tipo de usuário, etc.). O token é assinado com uma chave secreta.
4. **Resposta ao Cliente:** O JWT é retornado ao cliente.
5. **Autenticação em Requisições Subsequentes:** O cliente inclui o JWT no cabeçalho `Authorization: Bearer <token>` em todas as requisições subsequentes.
6. **Validação do JWT:** O backend valida o JWT em cada requisição, verificando a assinatura, a expiração e outras claims.

### Tecnologias/Bibliotecas:

* **Backend (exemplo com Node.js):**  `jsonwebtoken`, `bcrypt`
* **Backend (exemplo com Python):** `PyJWT`, `bcrypt`
* **Backend (exemplo com Java):** `jjwt`, `BCrypt`


### Considerações de Segurança:

* **Armazenamento de Senhas:**  Utilizar sempre algoritmos de hash seguros e com sal (ex: bcrypt, Argon2). Nunca armazenar senhas em texto plano.
* **Segurança do JWT:** Utilizar uma chave secreta forte e segura, armazenada de forma protegida (variáveis de ambiente ou serviços de segredo).  Definir tempo de expiração curto para o JWT. Considerar a utilização de tokens de refresh para evitar a necessidade de login frequente.
* **Proteção contra Ataques:** Implementar medidas para mitigar ataques como brute-force (limitação de tentativas de login), injeção de SQL e cross-site scripting (XSS).
* **HTTPS:** Todas as comunicações entre o cliente e o backend devem ser feitas via HTTPS.
* **Validação de Dados de Entrada:**  Validar todos os dados recebidos do cliente para prevenir vulnerabilidades.
* **Auditoria:** Implementar logs de acesso e auditoria para monitorar atividades do sistema.
* **Autorização:** Implementar um sistema de autorização baseado em roles para controlar o acesso aos recursos do sistema.  O JWT pode conter claims que indicam o papel do usuário.


