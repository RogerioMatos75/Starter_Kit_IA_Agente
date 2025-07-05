# Autenticação Backend

## Objetivo

Implementar um sistema de autenticação seguro e eficiente para usuários (clientes) e administradores, utilizando JSON Web Tokens (JWT).

## Tecnologias

* **jsonwebtoken:** Para geração e validação de JWTs.
* **bcrypt:** Para hashing de senhas.

## Endpoints Necessários

* **POST /api/auth/register:**  Endpoint para registro de novos usuários (clientes e administradores - com distinção de roles).
* **POST /api/auth/login:** Endpoint para login de usuários existentes.  Retorna um JWT.
* **GET /api/users/me:** Endpoint protegido por JWT que retorna informações do usuário logado (apenas com dados relevantes para o frontend).

## Regras de Negócio

* As senhas devem ser armazenadas com hash utilizando bcrypt.
* Os JWTs devem conter informações sobre o usuário, incluindo seu ID e role (usuário ou administrador).
* Os endpoints protegidos devem exigir um JWT válido.
* Um administrador terá permissões para acessar o painel administrativo e gerenciar indicações.
* Um cliente terá permissões para indicar amigos e visualizar seu desconto.
* O tempo de vida do JWT deve ser configurado adequadamente.