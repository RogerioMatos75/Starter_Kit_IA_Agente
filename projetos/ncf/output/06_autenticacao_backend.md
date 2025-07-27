# 06_autenticacao_backend.md

## Sugestão de Autenticação Backend para o Projeto NCF

### Método de Autenticação: JWT (JSON Web Token)

### Fluxo de Autenticação:

1. **Registro:** O usuário fornece suas credenciais (e-mail e senha) para criar uma conta. A senha deve ser armazenada com hash usando um algoritmo seguro como bcrypt ou Argon2.  O sistema gera um ID único para o usuário.

2. **Login:** O usuário fornece seu e-mail e senha. O sistema verifica se o e-mail existe e compara o hash da senha fornecida com o hash armazenado no banco de dados.

3. **Geração do JWT:** Se as credenciais forem válidas, o sistema gera um JWT contendo informações do usuário (ID, tipo de usuário - administrador, segurado ou convidado, etc.) e uma assinatura digital.  A assinatura é gerada usando uma chave secreta mantida em segredo no servidor.

4. **Resposta ao Cliente:** O JWT gerado é retornado ao cliente como resposta ao login.

5. **Autenticação em Requisições Subsequentes:** O cliente inclui o JWT no cabeçalho de todas as requisições subsequentes ao backend (geralmente como `Authorization: Bearer <token>`).

6. **Validação do JWT:** O servidor valida o JWT em cada requisição, verificando a assinatura e a expiração do token. Se o JWT for válido, o servidor pode acessar as informações do usuário contidas no token para autorizar a requisição.

7. **Logout:** O cliente pode solicitar logout, invalidando o token no servidor (opcionalmente, listando o token como inválido em uma tabela de tokens inválidos para segurança adicional).

### Tecnologias/Bibliotecas:

* **Linguagem de programação backend:** Node.js com Express.js (ou similar, como Python com Django/Flask, ou Go com Gin/Echo).
* **Biblioteca JWT:** `jsonwebtoken` (Node.js), `PyJWT` (Python), ou equivalente para a linguagem escolhida.
* **Banco de dados:** PostgreSQL, MySQL ou MongoDB (recomenda-se PostgreSQL por sua segurança e robustez).
* **Biblioteca de Hash de Senha:** `bcrypt` ou `argon2` (disponíveis em diversas linguagens).

### Considerações de Segurança:

* **Armazenamento de Senhas:** Nunca armazene senhas em texto simples. Sempre utilize algoritmos de hash seguros com sal (salt) e rounds adequados.
* **Chave Secreta do JWT:** Mantenha a chave secreta do JWT em segredo absoluto e nunca a compartilhe no código-fonte ou em repositórios públicos. Utilize variáveis de ambiente para armazená-la.
* **Validação de entrada:** Sempre valide e sanitize todas as entradas do usuário para prevenir ataques de injeção (SQL injection, XSS, etc.).
* **Proteção contra ataques de força bruta:** Implemente mecanismos de proteção contra ataques de força bruta, como limitação de tentativas de login e bloqueio temporário de contas após várias tentativas falhas.
* **HTTPS:** Certifique-se de que toda a comunicação entre o cliente e o servidor seja feita através de HTTPS para proteger os dados em trânsito.
* **Token Revogação:** Implementar um mecanismo de revogação de tokens para casos de comprometimento ou logout. Um token pode ser invalidado através de uma lista de tokens inválidos no banco de dados, ou por meio de uma data de expiração curta e a emissão de um novo token a cada login.
* **Atualização Regular das Dependências:** Mantenha todas as dependências de software atualizadas para corrigir vulnerabilidades de segurança conhecidas.
* **Auditoria de Segurança:** Realize auditorias de segurança regulares para identificar e corrigir vulnerabilidades.


