# Instalação e Configuração

Este guia detalha o passo a passo para configurar e rodar o projeto Archon AI em seu ambiente de desenvolvimento local. O projeto possui uma arquitetura híbrida, com um backend em Python (Flask) e uma animação de frontend em Node.js (Next.js).

## Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados em sua máquina:

-   **Python:** Versão 3.9 ou superior.
-   **Node.js:** Versão 18 ou superior (que inclui o `npm`, o gerenciador de pacotes do Node).

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

## Passo 2: Configuração da Animação (Node.js)

A animação de fundo `Pulse-Trace` é um projeto Next.js independente. Para que o painel principal possa exibi-la, precisamos "construir" o projeto para gerar os arquivos estáticos (HTML, CSS, JS).

1.  **Navegue até a pasta da animação:**
    A partir da raiz do projeto, entre na pasta do `Pulse-Trace`.
    ```bash
    cd static/Pulse-Trace
    ```

2.  **Instale as dependências do Node.js:**
    Este comando lê o arquivo `package.json` e baixa todas as bibliotecas necessárias para a pasta `node_modules`.
    ```bash
    npm install
    ```

3.  **Construa o projeto para produção:**
    Este comando executa o processo de build do Next.js, otimizando e empacotando os arquivos para uso.
    ```bash
    npm run build
    ```
    *Ao final, ele criará uma pasta `out` dentro de `static/Pulse-Trace`. O painel principal do Archon AI já está configurado para carregar a animação a partir desta pasta.*

## Passo 3: Variáveis de Ambiente

Informações sensíveis, como chaves de API, são gerenciadas através de um arquivo `.env`.

1.  **Crie o arquivo `.env`:** Na raiz do projeto, localize o arquivo `.env.example`. Faça uma cópia dele e renomeie-a para `.env`.
2.  **Adicione suas chaves:** Abra o arquivo `.env` e preencha as variáveis com suas chaves de API (ex: `GEMINI_API_KEY`, etc.).

## Passo 4: Executando o Projeto

Com tudo configurado, você pode iniciar a aplicação.

1.  **Volte para a pasta raiz do projeto** (se você ainda estiver na pasta `Pulse-Trace`):
    ```bash
    cd ../..
    ```
2.  **Inicie o servidor Flask:**
    ```bash
    flask run
    ```
3.  **Acesse o painel:** Abra seu navegador e acesse o endereço fornecido pelo Flask (geralmente `http://127.0.0.1:5000`).

Pronto! O Archon AI está rodando localmente na sua máquina.