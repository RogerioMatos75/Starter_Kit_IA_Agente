# 06_autenticacao_backend.md

## Sugestão de Autenticação Backend para o Projeto NCF-Teste (Archon)

### Método de Autenticação: JWT (JSON Web Token)

### Fluxo de Autenticação:

1. **Registro:** O usuário fornece suas credenciais (email e senha) para criar uma conta. A senha é criptografada usando um algoritmo de hash seguro (ex: bcrypt) antes de ser armazenada no banco de dados.
2. **Login:** O usuário envia seu email e senha para o backend.
3. **Validação:** O backend verifica se o email existe e se a senha fornecida corresponde à senha hash armazenada.
4. **Geração do JWT:** Se as credenciais forem válidas, o backend gera um JWT contendo informações do usuário (ID, email, tipo de usuário - administrador, segurado, etc.).  Este token é assinado com uma chave secreta.
5. **Retorno do JWT:** O JWT é retornado ao cliente (aplicativo mobile ou web).
6. **Autenticação subsequente:** Em requisições subsequentes, o cliente inclui o JWT no cabeçalho da requisição (ex: `Authorization: Bearer <token>`).
7. **Validação do JWT:** O backend valida o JWT verificando a assinatura e a expiração. Se o token for válido, o usuário é autenticado.


### Tecnologias/Bibliotecas:

* **Linguagem de Programação Backend:**  Node.js com Express.js (sugestão), ou Python com Django/Flask.
* **Biblioteca JWT:** jsonwebtoken (Node.js), PyJWT (Python).
* **Banco de Dados:** PostgreSQL ou MySQL (sugestão).
* **Algoritmo de Hash:** bcrypt.


### Considerações de Segurança:

* **Armazenamento de senhas:** Nunca armazenar senhas em texto plano. Usar sempre um algoritmo de hash unidirecional e salting para garantir que mesmo que o banco de dados seja comprometido, as senhas não possam ser recuperadas.
* **Chave secreta JWT:** Manter a chave secreta em um ambiente seguro e nunca expô-la no código-fonte.  Utilizar variáveis de ambiente para gerenciar a chave.
* **Validação de entrada:** Implementar validação rigorosa de todas as entradas do usuário para prevenir injeção de SQL e outros ataques.
* **Tempo de vida do token:** Definir um tempo de vida razoável para os tokens JWT e implementar mecanismos de refresh token para permitir que o usuário permaneça autenticado por um período mais longo, sem precisar logar novamente a cada requisição.
* **HTTPS:** Utilizar HTTPS para todas as comunicações entre o cliente e o servidor.
* **Proteção contra ataques CSRF (Cross-Site Request Forgery):** Implementar mecanismos de proteção CSRF, como tokens CSRF ou o uso de métodos HTTP adequados.
* **Rate Limiting:** Implementar rate limiting para prevenir ataques de força bruta.
* **Logging e Monitoramento:** Implementar logging detalhado para monitorar atividades e detectar possíveis ameaças.
* **Auditoria:** Registrar todas as tentativas de login, incluindo sucesso e falha, com timestamps e endereços IP.


