# 06_autenticacao_backend.md

## Autenticação Backend para o Projeto NCF-Teste (Archon)

### Método de Autenticação: JWT (JSON Web Tokens)

### Fluxo de Autenticação:

1. **Registro:** O usuário fornece credenciais (e-mail e senha) para criar uma conta.  A senha deve ser criptografada usando um algoritmo de hash seguro (ex: bcrypt, Argon2).
2. **Login:** O usuário fornece suas credenciais. O backend verifica se as credenciais são válidas comparando a senha fornecida com a senha hash armazenada.
3. **Geração de JWT:** Se as credenciais forem válidas, o backend gera um JWT contendo informações do usuário (ID, nome, tipo de usuário - administrador, segurado, etc.) e outras informações relevantes.  O JWT deve ser assinado com uma chave secreta segura, mantida em segredo no servidor.
4. **Resposta ao Cliente:** O JWT é retornado ao cliente como parte da resposta de login.
5. **Autenticação subsequente:** Em todas as solicitações subsequentes, o cliente inclui o JWT no cabeçalho de autorização (`Authorization: Bearer <token>`).
6. **Validação do JWT:** O backend valida o JWT a cada solicitação, verificando a assinatura, a expiração e a integridade do token.  Se o token for válido, o usuário é autenticado.
7. **Refresh Token (opcional):** Um refresh token pode ser implementado para permitir que o usuário permaneça autenticado por um período mais longo sem precisar fazer login novamente a cada vez.  Este token seria usado para gerar novos JWTs quando o JWT original expirar.

### Tecnologias/Bibliotecas:

* **Linguagem de Programação:**  Node.js com Express.js (ou Python com Django/Flask, dependendo da escolha da equipe)
* **Biblioteca JWT:**  jsonwebtoken (Node.js), PyJWT (Python)
* **Armazenamento de dados:**  PostgreSQL ou MongoDB (ou outra solução de banco de dados apropriada).
* **Criptografia de senha:** bcrypt (Node.js e Python) ou Argon2 (Node.js e Python).


### Considerações de Segurança:

* **Chave secreta segura:** A chave secreta usada para assinar os JWTs deve ser mantida em segredo e nunca deve ser exposta no código-fonte ou em qualquer outro lugar acessível a terceiros. Utilize variáveis de ambiente para armazená-la.
* **Validação rigorosa do JWT:**  Implementar uma validação completa do JWT em cada solicitação para evitar ataques de falsificação.
* **Tempo de vida curto do JWT:**  Configurar um tempo de vida curto para os JWTs para minimizar o impacto de um token comprometido.
* **HTTPS:**  Utilizar HTTPS para garantir que todas as comunicações entre o cliente e o servidor estejam criptografadas.
* **Proteção contra ataques de força bruta:** Implementar mecanismos de proteção contra ataques de força bruta para impedir tentativas de login repetidas com credenciais inválidas.
* **Limite de tentativas de login:** Implementar um limite de tentativas de login, bloqueando o usuário temporariamente após um número excessivo de tentativas falhas.
* **Entrada sanitizada:** Sanitizar todas as entradas do usuário para prevenir ataques de injeção (SQL injection, XSS, etc.).
* **Auditoria de segurança:** Registrar todas as tentativas de login, incluindo sucesso e falha, para fins de auditoria e monitoramento.
* **Refresh Token seguro:** Se utilizado, o refresh token deve ser armazenado com segurança, preferencialmente com um mecanismo de renovação e revogação. Considerar o uso de um token com tempo de vida mais longo e uma chave de autenticação separada do acesso ao token.
* **Proteção contra CSRF:** Implementar medidas para proteger contra ataques CSRF (Cross-Site Request Forgery).


