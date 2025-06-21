"""# 💡 Starter Kit - Workflow Híbrido de IA Supervisionável

Este projeto apresenta um **Starter Kit para um workflow de desenvolvimento com Inteligência Artificial que é confiável, supervisionável e rastreável**. O objetivo é superar as limitações comuns encontradas em abordagens de "Vibe Code" ou ao usar assistentes de IA de forma isolada, como alucinações, modificações inesperadas e perda de contexto, especialmente em projetos complexos.

Utilizamos uma arquitetura em camadas para gerar, planejar e executar projetos (MVPs, Micro-SaaS, protótipos) de forma mais controlada e eficiente.

## 🤔 Quando Utilizar este Starter Kit?

Este workflow é particularmente útil em cenários onde a supervisão, controle e um entendimento profundo do contexto do projeto pela IA são cruciais. A tabela abaixo sugere como aplicar as camadas da arquitetura em diferentes situações:

| Situação                               | Ação Ideal                                                                 | Camadas Envolvidas                     |
| :------------------------------------- | :------------------------------------------------------------------------- | :------------------------------------- |
| 🧪 MVP novo com estrutura clara        | Focar na execução controlada e geração de prompts eficazes.                | Agente FSM + Engenharia de Prompt      |
| 📈 Produto recorrente ou complexo    | Utilizar todas as camadas para máximo contexto e especialização.           | Todas (Fine-Tuning Conceitual + Agente FSM + Engenharia de Prompt + Memória) |
| 🤖 Agente de IA parece "perdido"      | Melhorar a clareza e detalhe das instruções dadas à IA.                    | Reforçar Engenharia de Prompt          |
| 🐞 IA modificando código legado      | Criar uma base de conhecimento sólida sobre o código existente.            | Fine-Tuning Conceitual (com foco no legado) |
| ⚙️ Projeto que precisa evoluir       | Garantir que a IA possa planejar e lembrar de interações passadas.         | Agente FSM + Memória Persistente       |

---

## 🚀 Como Começar/Usar

Siga os passos abaixo para configurar e executar este Starter Kit:

**1. Pré-requisitos:**

*   **Python:** Certifique-se de ter o Python instalado (versão 3.8 ou superior recomendada).
*   **Pip:** O gerenciador de pacotes Pip geralmente vem com a instalação do Python.

**2. Clone o Repositório (Se aplicável):**

Se você ainda não o fez, clone este repositório para a sua máquina local:
```bash
git clone <url-do-repositorio>
cd <nome-do-repositorio>
```

**3. Instale as Dependências:**

Este projeto utiliza um arquivo `requirements.txt` para listar suas dependências. Instale-as com o seguinte comando no seu terminal, a partir da raiz do projeto:
```bash
pip install -r requirements.txt
```

**4. Principais Comandos de Execução:**

*   **Gerar Estudo de Domínio (Fine-Tuning Conceitual):**
    Este comando inicializa o processo, criando os arquivos base de conhecimento em `output/`.
    ```bash
    python main.py
    ```

*   **Executar uma Funcionalidade Específica:**
    Para que o agente de IA desenvolva ou processe uma funcionalidade particular (ex: `login_usuario`).
    ```bash
    python executar_funcionalidade.py --func nome_da_funcionalidade
    ```
    Substitua `nome_da_funcionalidade` pelo alvo desejado.

*   **Orquestrar o Workflow com FSM (Máquina de Estados):**
    Para executar o processo completo de forma sequencial e supervisionada, etapa por etapa.
    ```bash
    python fsm_orquestrador.py
    ```
    O sistema irá pausar entre as etapas principais, aguardando sua confirmação para continuar.

**5. Entendendo os Resultados:**

*   **Base de Conhecimento:** Verifique a pasta `output/` para os documentos gerados pelo `main.py`.
*   **Logs de Execução:** A pasta `logs/` conterá o `diario_execucao.json` com o histórico detalhado e, possivelmente, um `log_execucao.pdf`.

Com estes passos, você estará pronto para explorar e utilizar o workflow híbrido de IA.

---

## 🧰 Ferramentas Sugeridas

A tabela abaixo lista algumas ferramentas que podem ser utilizadas para implementar cada camada da arquitetura proposta:

| Camada                 | Ferramentas Sugeridas                                       |
| :--------------------- | :---------------------------------------------------------- |
| Fine-Tuning Conceitual | DeepSeek, Ollama + QLoRA, OpenAI + datasets JSONL           |
| Agente de IA / FSM     | CrewAI, LangGraph, AutoGen, OpenDevin, Python com `transitions` |
| Engenharia de Prompt   | Typst (documentação), Markdown modular, PromptLayer         |

---

## 🏗️ Arquitetura Híbrida Supervisionável

Este workflow é composto por camadas distintas que trabalham em conjunto para garantir um desenvolvimento com IA mais controlado e eficaz. Abaixo, detalhamos cada componente da arquitetura:

### 1. 🎓 Fine-Tuning Conceitual

**O que é?**
Em vez de um fine-tuning tradicional que exige grandes datasets e re-treinamento de modelos, o "Fine-Tuning Conceitual" simula um treinamento especializado da IA. Isso é feito através da geração de documentos detalhados que servem como base de conhecimento para o projeto.

**Como funciona?**
Utilizam-se pesquisas com IAs generativas (ex: Gemini, Claude, ChatGPT) para criar um conjunto de artefatos que definem o escopo e a estrutura do projeto:
*   **Estudo de Domínio:** Compreensão aprofundada do problema a ser resolvido.
*   **Arquitetura Técnica:** Definição das tecnologias, plataformas e design do sistema.
*   **Regras de Negócio:** Lógica e restrições específicas do projeto.
*   **Fluxos de Usuário:** Jornada do usuário e interações com o sistema.
*   **Backlog de Funcionalidades:** Lista priorizada de features a serem desenvolvidas.

Esses documentos (geralmente em `output/`) alimentam as etapas subsequentes, garantindo que o agente de IA opere com um contexto rico e específico do projeto, como se tivesse sido "treinado" nele.

**Exemplo de Estrutura dos Artefatos do Fine-Tuning Conceitual:**

Os arquivos gerados nesta etapa (localizados em `output/`) podem seguir a seguinte estrutura:
```
output/
├── plano_base.md
├── arquitetura_tecnica.md        <-- estrutura por camadas, tech stack
├── regras_negocio.md             <-- decisões de negócio e domínio
├── fluxos_usuario.md             <-- experiência e lógica de navegação
└── backlog_mvp.md                <-- features mínimas para validação
```

### 2. 🛠️ Agente FSM (Finite State Machine)

**O que é?**
Um Agente de IA orquestrado por uma Máquina de Estados Finitos (FSM). Isso significa que o processo de desenvolvimento é dividido em etapas claras, e o agente só avança para a próxima etapa após a conclusão (e, opcionalmente, aprovação manual) da etapa atual.

**Como funciona?**
O FSM define um fluxo de trabalho estruturado (ex: `planejamento → arquitetura → backend → frontend → testes → deploy`).
*   Cada estado representa uma fase do projeto.
*   O agente de IA (construído com ferramentas como CrewAI, LangGraph, AutoGen, etc.) executa tarefas específicas dentro de cada estado.
*   A transição entre estados é controlada, prevenindo que a IA execute ações fora de ordem ou cometa erros em cascata.
*   O `fsm_orquestrador.py` exemplifica esse controle, permitindo pausas para validação humana.

### 3. 📋 Engenharia de Prompt Avançada

**O que é?**
A prática de criar prompts (comandos) altamente detalhados, estruturados e contextualizados para guiar a IA na execução de cada tarefa.

**Como funciona?**
Em vez de prompts genéricos, esta camada foca em:
*   **Precisão:** Instruções claras sobre o que a IA deve fazer, qual formato de saída esperar, etc.
*   **Contextualização:** Incorporar informações do "Fine-Tuning Conceitual" e do estado atual do FSM nos prompts.
*   **Modularidade e Reusabilidade:** Organizar prompts em arquivos gerenciáveis (ex: `prompts.py`) para que possam ser facilmente adaptados e reutilizados.
*   O `memoria_conceitual.py` ajuda a gerar prompts enriquecidos com o conhecimento do projeto.

### 4. 🧩 Memória Persistente

**O que é?**
Um sistema para registrar o progresso, as decisões e os resultados de cada etapa executada pelo agente de IA. Essencialmente, dá ao sistema uma "memória" de longo prazo.

**Como funciona?**
*   **Registro de Tarefas:** Cada ação do agente, seu status (concluído, falhou, em andamento) e os resultados são salvos (ex: em `logs/diario_execucao.json`).
*   **Estado Contínuo:** O sistema sabe qual foi a última etapa concluída, permitindo retomar o trabalho de onde parou (`proximo_estado.json`).
*   **Auditoria e Rastreabilidade:** Cria um histórico detalhado do desenvolvimento, útil para depuração, análise e relatórios (ex: `logs/log_execucao.pdf`).
*   O `registrador_tarefas.py` é responsável por essa funcionalidade.

Esta arquitetura de múltiplas camadas visa transformar o uso de IAs generativas em um processo robusto, transparente e gerenciável.

---

<!--
A seção "Estrutura Sugerida do Fine-Tuning Conceitual (via Prompt/Plano)" foi integrada
acima, dentro da descrição da camada "Fine-Tuning Conceitual".
-->

---

## 🚀 Como Funciona na Prática (Workflow Detalhado)

O workflow deste starter kit combina as camadas da arquitetura da seguinte maneira:

### 1. Geração da Base de Conhecimento (Fine-Tuning Conceitual)

Primeiro, estabelecemos o "conhecimento" fundamental do projeto.

*   **Ação:** Execute o script `main.py`:
    ```bash
    python main.py
    ```
*   **Resultado:** São gerados arquivos na pasta `output/` (como `plano_base.md`, `arquitetura_tecnica.md`, etc.). Estes documentos constroem o "Fine-Tuning Conceitual".
*   **Propósito:** Estes documentos simulam um "fine-tuning" da IA, fornecendo um contexto detalhado sobre o domínio, arquitetura, regras de negócio e funcionalidades do projeto. Eles são a fonte da verdade para as etapas seguintes.

### 2. Especialização e Preparação de Prompts (Engenharia de Prompt)

Com a base de conhecimento criada:

*   O módulo `memoria_conceitual.py` lê esses arquivos de `output/`.
*   Ele prepara o contexto para ser injetado nos prompts que serão enviados ao agente de IA.
*   Isso garante que a IA opere com informações específicas do projeto, aumentando a relevância e precisão de suas respostas, sem necessidade de re-treinamento de um modelo.

### 3. Execução de Funcionalidades com o Agente IA

Para desenvolver uma funcionalidade específica (ex: `login_usuario`):

*   **Ação:** Execute o script `executar_funcionalidade.py` especificando a funcionalidade:
    ```bash
    python executar_funcionalidade.py --func login_usuario
    ```
*   **Processo:**
    1.  O sistema utiliza o `memoria_conceitual.py` para carregar o contexto relevante.
    2.  Um prompt detalhado e contextualizado é gerado (conforme a Engenharia de Prompt Avançada).
    3.  O agente de IA (ex: `agente/executor_agente.py`) é acionado para processar o prompt e gerar o código ou a solução para a funcionalidade solicitada.
*   **Resultado:** Código ou artefatos da funcionalidade são criados, baseados no plano original e no conhecimento especializado.

### 4. Orquestração com Máquina de Estados Finitos (FSM) e Supervisão

Para projetos maiores ou que exigem um controle passo a passo mais rigoroso, o `fsm_orquestrador.py` entra em ação.

*   **O que é?** O FSM (Finite State Machine) define um fluxo de trabalho com etapas sequenciais (estados), por exemplo:
    ```mermaid
    stateDiagram
        [*] --> Planejamento
        Planejamento --> Arquitetura
        Arquitetura --> Backend
        Backend --> Frontend
        Frontend --> Testes
        Testes --> Deploy
        Deploy --> [*]
    ```
*   **Ação:** Execute o orquestrador:
    ```bash
    python fsm_orquestrador.py
    ```
*   **Processo:**
    1.  O orquestrador avança estado por estado.
    2.  Em cada estado, uma tarefa específica é atribuída ao agente de IA (utilizando prompts avançados).
    3.  **Ponto de Controle:** O sistema pausa após a conclusão de cada etapa FSM (ex: após o `BACKEND`), permitindo uma revisão manual antes de prosseguir:
        ```
        ⏸️ Pausado após etapa 'BACKEND'. Pressione [Enter] para continuar para a próxima...
        ```
*   **Benefícios do FSM:** Previsibilidade, controle de fluxo, depuração facilitada, ideal para MVPs/backlogs, e integração com agentes/prompts.

### 5. Registro e Memória Persistente

Ao longo de todo o processo, a camada de Memória Persistente garante rastreabilidade e continuidade.

*   **Log Detalhado:** Todas as execuções, status de tarefas e respostas do agente são salvas em `logs/diario_execucao.json`.
    ```json
    [
      {
        "etapa": "planejamento",
        "tarefa": "definir objetivos do MVP",
        "status": "concluída",
        "resposta_agente": "Objetivos definidos com base em..."
      },
      {
        "etapa": "backend",
        "tarefa": "implementar base de autenticação",
        "status": "em execução",
        "iniciado_em": "2025-06-21T20:45:00"
      }
    ]
    ```
*   **Exportação:** Um resumo legível é frequentemente exportado para `logs/log_execucao.pdf`.
*   **Retomada:** O sistema pode ser configurado para lembrar do último estado concluído (o arquivo `proximo_estado.json` foi mencionado como um componente para isso), permitindo retomar o trabalho.
*   **Componente Chave:** O `registrador_tarefas.py` gerencia esses registros.

Este fluxo integrado transforma o desenvolvimento com IA de uma atividade de "caixa preta" para um processo engenheirado, supervisionável e iterativo. Você não depende de um "super prompt" único, a IA mantém o contexto, e todo o processo é modular e escalável.

---

### ✨ Exemplo de Prompt para Estudo de Domínio (Pré-Fine-Tuning Conceitual)

Para iniciar a fase de "Fine-Tuning Conceitual" e gerar os documentos base do seu projeto, você pode adaptar o seguinte prompt para usar com uma IA generativa:

```bash
Atue como um Arquiteto de Software e analista de negócios.
Preciso de um estudo técnico completo para criar um [Seu Projeto Aqui].
Liste todas as funcionalidades necessárias para um sistema moderno, dividindo em:

1. Funcionalidades principais
2. Funcionalidades administrativas
3. Integrações externas (pagamentos, frete, etc.)
4. Tecnologias recomendadas para cada parte
5. Boas práticas para segurança e escalabilidade

Adicione exemplos reais e destaque as decisões técnicas mais comuns no mercado atual.

	- Estudo de domínio
	- Arquitetura técnica
	- Regras de negócio
	- Fluxos de usuário
	- Backlog de funcionalidades
```

---

## 📁 Estrutura de Diretórios

A estrutura de arquivos e diretórios do projeto é organizada da seguinte forma:

```tree
.
├── .github/                    # Configurações do GitHub (ex: Actions para CI/CD)
│   └── workflows/
│       └── python.yml
├── LICENSE                     # Licença do projeto
├── README.md                   # Este arquivo
├── requirements.txt            # Dependências Python do projeto
├── main.py                     # Script principal para gerar o estudo de domínio (Fine-Tuning Conceitual)
├── executar_funcionalidade.py  # Script para executar uma funcionalidade específica com o agente IA
├── memoria_conceitual.py       # Módulo para carregar o contexto do projeto e gerar prompts dinâmicos
├── fsm_orquestrador.py         # Orquestrador da Máquina de Estados Finitos para controlar o fluxo
├── registrador_tarefas.py      # Módulo para registrar o progresso e gerar logs
├── prompts.py                  # Arquivo centralizando os modelos de prompts
├── agente/                     # Componentes do agente de IA
│   ├── base_agente.py
│   └── executor_agente.py
├── output/                     # Arquivos gerados pelo Fine-Tuning Conceitual
│   ├── plano_base.md
│   ├── arquitetura_tecnica.md
│   ├── regras_negocio.md
│   ├── fluxos_usuario.md
│   └── backlog_mvp.md
└── logs/                       # Logs de execução e registros de tarefas
    ├── diario_execucao.json
    └── log_execucao.pdf
```

---

<!-- Seção removida: O conteúdo principal de "Memória Persistente entre ciclos de execução"
     foi integrado na seção de Arquitetura (explicação da camada) e
     na seção "Como Funciona na Prática" (exemplo de JSON e menção a logs).
     A tabela de status das camadas tornou-se redundante com a nova estrutura. -->

## 📦 Estrutura para Versionamento (Exemplo GitHub)

Este projeto está organizado de forma a facilitar o versionamento em plataformas como o GitHub, incluindo boas práticas como a automação de CI/CD.

**✅ Estrutura de Repositório Sugerida:**

A listagem abaixo mostra os principais arquivos e diretórios já presentes ou recomendados para um repositório bem estruturado:
```tree
.
├── .github/
│   └── workflows/
│       └── python.yml      # Workflow de CI (Integração Contínua)
├── LICENSE                 # Arquivo de licença do projeto
├── README.md               # Documentação principal (este arquivo)
├── requirements.txt        # Dependências Python
├── main.py                 # Script principal
├── agente/                 # Código do(s) agente(s) de IA
├── output/                 # Resultados do Fine-Tuning Conceitual
├── logs/                   # Logs de execução
└── ...                     # Outros arquivos e pastas do projeto
```

**🔄 Workflow Automático (CI/CD com GitHub Actions):**

Um arquivo .yml dentro de .github/workflows/ que:
Instala dependências (pip install)
Roda testes automatizados (se existirem)
Verifica se o código está funcionando antes do commit virar bug na produção

🧠 Vantagens:

Profissionalismo: Quem entra no seu repositório vê que ele já está preparado para produção.
Automação: Evita erros ao fazer push no Git.
Pronto pro GitHub Pages (se for app web).
Fácil de colaborar com outras pessoas (ou IAs) de forma organizada.

---

Criado por Rogerio Matos com suporte do ChatGPT / Gemini

"Deixe de ser um programador refém da IA. Torne-se o arquiteto que comanda todo o ciclo."
