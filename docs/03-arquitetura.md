# Arquitetura do Sistema Archon AI

O Archon AI é construído sobre uma arquitetura híbrida e supervisionada, projetada para combinar a robustez de um backend Python com a flexibilidade de um frontend moderno, mantendo o controle humano como peça central do processo.

## Visão Geral da Arquitetura

O fluxo de interação principal pode ser visualizado da seguinte forma:

```
[ Usuário ] <--> [ Navegador (Dashboard) ]
     ^                    |
     | (Ações via API)    | (Renderiza UI)
     v                    v
[ app.py (Flask) ] <--> [ fsm_orquestrador.py ]
     |                        |         ^
     | (Executa Ação)         | (Gera Prompt) | (Lê Workflow)
     |                        v         |
     |                  [ ia_executor.py ] --> [ API Externa (Gemini) ]
     |                        |
     | (Salva Artefatos)      | (Lê Contexto)
     v                        v
[ Sistema de Arquivos ]  [ guia_projeto.py ]
(projetos/, logs/, cache/)   (lê output/)
```

## Componentes Principais (Backend)

O coração do sistema reside no backend Python, que orquestra todo o ciclo de vida do projeto.

### `app.py` - O Servidor Web e Gateway de API
*   **Função:** É a porta de entrada para todas as interações do usuário. Construído com **Flask**, ele tem duas responsabilidades principais:
    1.  **Servir a Interface:** Renderiza o painel de controle (`dashboard.html`) e a landing page.
    2.  **Expor a API REST:** Fornece os endpoints que o frontend consome para interagir com o sistema.
*   **Endpoints Chave:**
    *   `/api/status`: Fornece o estado atual completo do orquestrador (timeline, preview, ações possíveis).
    *   `/api/start`: Inicia um novo projeto com um nome específico.
    *   `/api/action`: Processa as ações do supervisor (aprovar, repetir, voltar).
    *   `/api/reset`: Reinicia o estado do projeto, limpando logs e artefatos.
    *   `/upload`: Gerencia o upload dos arquivos da base de conhecimento.

### `fsm_orquestrador.py` - O Cérebro da Operação
*   **Função:** Este é o componente mais crítico. Implementa uma **Máquina de Estados Finitos (FSM)** que garante a execução sequencial e controlada do projeto.
*   **Responsabilidades:**
    *   Lê o `workflow.json` para saber a ordem e os detalhes de cada etapa.
    *   Mantém o estado atual do projeto (ex: `current_step_index`).
    *   Processa as decisões do usuário (`process_action`) para avançar, repetir ou retroceder no fluxo.
    *   Orquestra a geração de prompts, a execução da IA e o salvamento dos resultados.
    *   Gerencia a persistência do estado através de logs e checkpoints.

### `workflow.json` - O Blueprint do Projeto
*   **Função:** É um arquivo de configuração que define todo o fluxo de trabalho. Ele desacopla a lógica do orquestrador das etapas específicas de um projeto.
*   **Estrutura:** Consiste em uma lista de "estados", onde cada estado define:
    *   `nome`: O nome da etapa (ex: "Backend: API de Autenticação").
    *   `tipo`: A categoria da tarefa (ex: `backend`, `documentacao`).
    *   `artefato_gerado`: O nome do arquivo que será criado nesta etapa.
    *   `guia`: O arquivo da base de conhecimento (`.md`) que servirá de contexto.
    *   `descricao`: A instrução principal para a IA.

### `ia_executor.py` - O Comunicador com a IA
*   **Função:** Um módulo isolado cuja única responsabilidade é se comunicar com a API do Google Gemini.
*   **Lógica:** Recebe um prompt, envia para a IA, e retorna a resposta em texto. Ele abstrai os detalhes da chamada de API, mantendo o orquestrador focado em sua lógica de fluxo.

### `guia_projeto.py` - O Leitor da Base de Conhecimento
*   **Função:** Um módulo auxiliar que lê e extrai conteúdo dos arquivos `.md` da pasta `output/`.
*   **Lógica:** A função `extrair_secoes` é usada para carregar apenas as partes relevantes de um documento de contexto, garantindo que o prompt enviado à IA seja focado e preciso.

## Componentes do Frontend e Integração

### `templates/dashboard.html` e `static/js/main.js`
*   **Função:** O painel de controle interativo do supervisor.
*   **Tecnologia:** HTML, TailwindCSS e **Vanilla JavaScript**.
*   **Lógica (`main.js`):**
    *   Ao carregar, busca o estado inicial do projeto via `/api/status`.
    *   Renderiza dinamicamente a linha do tempo, o painel de pré-visualização e as ações disponíveis.
    *   Captura os cliques nos botões e envia as ações correspondentes para a API do backend.

### `static/Pulse-Trace/` - A Animação de Fundo
*   **Arquitetura:** Adota uma abordagem de **"micro-frontend"**. É uma aplicação **Next.js (React)** completamente independente.
*   **Integração:**
    1.  O projeto Next.js é "construído" (`npm run build`) para gerar um conjunto de arquivos estáticos (HTML, CSS, JS) na pasta `out/`.
    2.  O `dashboard.html` simplesmente carrega o `index.html` gerado dentro de um `<iframe>`.
*   **Vantagem:** Esta abordagem desacopla a complexa animação do backend Python. Permite usar um ecossistema moderno (Node.js, React) para a UI sem sobrecarregar o servidor principal, que pode se concentrar na lógica de orquestração.

## Fluxo de Dados: A Jornada de uma Ação

Vamos traçar o que acontece quando o usuário clica em "Aprovar":

1.  **Ação do Usuário:** O clique no botão "Aprovar" é capturado pelo `main.js`.
2.  **Frontend (`main.js`):** Envia uma requisição `POST` para `/api/action` com o corpo `{"action": "approve"}`.
3.  **Backend (`app.py`):** A rota correspondente recebe a requisição e invoca `fsm.process_action('approve')`.
4.  **Orquestrador (`fsm_orquestrador.py`):**
    a. Registra a aprovação da etapa atual no `diario_execucao.json`.
    b. Avança o estado (`current_step_index++`).
    c. Chama `_run_current_step()` para iniciar a próxima etapa.
5.  **Execução da Etapa (`_run_current_step`):**
    a. Lê os detalhes da nova etapa no `workflow.json`.
    b. Usa `guia_projeto.py` para carregar o contexto do arquivo `.md` especificado no `guia`.
    c. Constrói um prompt detalhado e o envia para `executar_codigo_real`.
6.  **Executor (`executar_codigo_real`):**
    a. Verifica o cache. Se não houver, chama `ia_executor.py` para obter uma nova resposta da IA.
    b. Salva a resposta no arquivo de artefato definido (ex: `projetos/MeuProjeto/api_autenticacao.py`).
    c. Atualiza o `README.md` do projeto com o novo progresso.
    d. Retorna o conteúdo gerado.
7.  **Orquestrador:** Armazena o conteúdo retornado em `last_preview_content`.
8.  **Backend (`app.py`):** Envia o novo estado completo do FSM (com a timeline atualizada e o novo preview) como resposta JSON.
9.  **Frontend (`main.js`):** Recebe a resposta e atualiza a interface para refletir o novo estado, pronto para a próxima decisão do supervisor.

## Estrutura de Diretórios e Persistência

A forma como os arquivos são organizados é crucial para o funcionamento do sistema:

*   `output/`: **A Entrada.** Contém a base de conhecimento que define o projeto. É a fonte de verdade para o contexto da IA.
*   `projetos/`: **A Saída.** Armazena os artefatos finais gerados pela IA. Cada projeto é isolado em sua própria pasta.
*   `logs/`: **A Memória.**
    *   `diario_execucao.json`: Garante a **rastreabilidade** e **auditoria**, registrando cada ação e resultado.
    *   `proximo_estado.json`: Funciona como um **checkpoint**, permitindo que o sistema seja pausado e retomado.
*   `cache/`: **A Performance.** Guarda os resultados de execuções da IA para acelerar repetições e economizar chamadas de API.