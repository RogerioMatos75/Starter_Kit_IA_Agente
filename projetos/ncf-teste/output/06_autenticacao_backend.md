# 06_autenticacao_backend.md

## Autenticação Backend para o Projeto NCF-Teste (Archon)

### Método de Autenticação: JWT (JSON Web Tokens)

### Fluxo de Autenticação:

1. **Registro:** O usuário fornece suas credenciais (email e senha) para criar uma conta. A senha deve ser armazenada utilizando hashing com sal (ex: bcrypt).
2. **Login:** O usuário fornece seu email e senha. O backend valida as credenciais comparando a senha fornecida com o hash armazenado.
3. **Geração do JWT:** Se as credenciais forem válidas, o backend gera um JWT contendo informações do usuário (ID, nome, tipo de usuário - administrador, segurado, etc.).  O JWT deve ser assinado com uma chave secreta mantida em segredo.
4. **Envio do JWT:** O JWT é enviado ao cliente (frontend).
5. **Autenticação em Requisições Subsequentes:** O cliente inclui o JWT no header de todas as requisições subsequentes (ex: Authorization: Bearer <token>).
6. **Validação do JWT:** O backend valida o JWT a cada requisição verificando sua assinatura e expiração.  Se o JWT for válido, o usuário é autenticado.
7. **Logout:** O cliente deve enviar uma requisição de logout, invalidando o token.  Uma abordagem comum é adicionar uma lista de tokens revogados no backend para uma validação mais robusta.


### Tecnologias/Bibliotecas:

* **Linguagem de Programação:**  Node.js com Express.js (ou outra linguagem backend como Python com Django/Flask, Go com Gin/Echo, etc.)
* **Biblioteca JWT:**  jsonwebtoken (Node.js), PyJWT (Python), etc.
* **Hashing:** bcrypt (recomendado), Argon2.


### Considerações de Segurança:

* **Armazenamento de Senhas:** Nunca armazene senhas em texto plano. Utilize sempre um algoritmo de hashing seguro como bcrypt para armazenar hashes de senhas com sal.
* **Chave Secreta:** Mantenha a chave secreta usada para assinar os JWT em segredo absoluto. Não a comprometa no código fonte, utilize variáveis de ambiente.
* **Validação de Dados de Entrada:** Sempre valide e sanitize todos os dados recebidos do cliente antes de processá-los para prevenir ataques de injeção.
* **Proteção contra CSRF (Cross-Site Request Forgery):** Utilize tokens CSRF para prevenir ataques CSRF.
* **Limitação de Tentativas de Login:** Implemente um mecanismo de limitação de tentativas de login para proteger contra ataques de força bruta.
* **HTTPS:** Certifique-se de que o backend esteja configurado com HTTPS para proteger as comunicações.
* **Auditoria:** Registre todas as tentativas de login, incluindo sucesso e falha, para fins de auditoria e detecção de intrusões.
* **Atualizações de Segurança:** Mantenha todas as bibliotecas e dependências atualizadas para corrigir vulnerabilidades de segurança conhecidas.
* **Token de Refresco (Refresh Token):** Implementar um sistema de refresh token para permitir que os usuários permaneçam autenticados por um período mais longo sem precisar inserir as credenciais repetidamente.  Esse token deve ter um tempo de vida mais longo que o JWT.
* **JWT com Claims:** Utilizar claims no JWT para definir escopos e permissões, permitindo um controle de acesso mais granular.


