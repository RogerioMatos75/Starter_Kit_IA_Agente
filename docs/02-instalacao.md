# Instalação e Configuração

Este guia detalha o passo a passo para configurar e rodar o projeto Archon AI em seu ambiente de desenvolvimento local.

## Pré-requisitos

Antes de começar, garanta que você tenha o seguinte software instalado em sua máquina:

-   **Python:** Versão 3.9 ou superior.

## Passo 1: Configuração do Backend (Python)

O core do Archon AI é uma aplicação Flask. A melhor prática é rodá-la dentro de um ambiente virtual para isolar as dependências.

1.  **Clone o repositório** (se ainda não o fez) e navegue até a pasta raiz do projeto.

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # 1. Crie a pasta do ambiente virtual (ex: 'venv')
    python -m venv venv

    # 2. Ative o ambiente
    # No Windows (PowerShell/CMD):
    .\venv\Scripts\activate

    # No macOS/Linux (bash/zsh):
    source venv/bin/activate
    ```
    *Você saberá que o ambiente está ativo pois o nome dele (ex: `(venv)`) aparecerá no início do seu prompt de terminal.*

3.  **Instale as dependências do Python:**
    Com o ambiente virtual ativo, instale todas as bibliotecas necessárias a partir do arquivo `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

## Passo 2: Variáveis de Ambiente

Informações sensíveis, como chaves de API, são gerenciadas através de um arquivo `.env`.

1.  **Crie o arquivo `.env`:** Na raiz do projeto, localize o arquivo `.env.example`. Faça uma cópia dele e renomeie-a para `.env`.
2.  **Adicione suas chaves:** Abra o arquivo `.env` e preencha as variáveis com suas chaves de API (ex: `GEMINI_API_KEY`, `STRIPE_SECRET_KEY`, etc.).

## Passo 3: Executando o Projeto

Com tudo configurado, você pode iniciar a aplicação de duas formas:

### 1. Iniciando o Servidor Web (Painel de Controle)

Para acessar a interface visual do Archon AI:

```bash
flask run
```

*Acesse o painel em seu navegador (geralmente `http://127.0.0.1:5000`).*

### 2. Executando o Agente CLI (Linha de Comando)

Para usar o agente diretamente via linha de comando, por exemplo, para que ele execute um projeto gerado pelo Archon:

```bash
python main.py --project_path "./projetos/NomeDoSeuProjeto"
```

*Substitua `./projetos/NomeDoSeuProjeto` pelo caminho real da pasta do projeto que você deseja que o agente processe. O agente buscará o `Gemini.md` dentro dessa pasta para iniciar sua missão.*

Pronto! O Archon AI está rodando localmente na sua máquina.