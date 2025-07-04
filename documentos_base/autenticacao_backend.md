# Autenticação Backend: API

## Objetivo
Definir os requisitos e a estrutura para a API de autenticação do backend.

## Tecnologias
*   **Linguagem:** Python
*   **Framework:** Flask
*   **Autenticação:** JWT (JSON Web Tokens)
*   **Banco de Dados (Exemplo):** SQLite (para prototipagem), PostgreSQL (para produção)

## Endpoints Necessários
*   `/api/auth/register` (POST): Registro de novos usuários.
*   `/api/auth/login` (POST): Autenticação de usuários existentes e emissão de JWT.
*   `/api/auth/refresh` (POST): Renovação de tokens JWT (opcional, para tokens de refresh).
*   `/api/auth/protected` (GET): Exemplo de rota protegida que requer um JWT válido.

## Regras de Negócio
*   Senhas devem ser armazenadas de forma segura (hashing com bcrypt, por exemplo).
*   E-mails de usuário devem ser únicos.
*   Tokens JWT devem ter um tempo de expiração.
*   Tratamento de erros claro para credenciais inválidas, usuários já existentes, etc.

## Estrutura de Dados (Exemplo)
### Usuário
*   `id` (UUID)
*   `email` (string, único)
*   `password_hash` (string)
*   `created_at` (datetime)

## Exemplo de Respostas (JSON)
### Sucesso no Login/Registro
```json
{
  "message": "Login bem-sucedido!",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "usuario@example.com"
  }
}
```
### Erro
```json
{
  "error": "Credenciais inválidas."
}
```
