<p align="center">
  <img src="static/assets/Bunner-Archon1.jpg" alt="Banner animado do Archon AI mostrando um pulso de atividade neural ou de dados.">
</p>

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0_(MVP)-blue)
![License](https://img.shields.io/badge/license-Proprietary-red)

# 🏛️ Archon AI: Governe seu Workflow de IA

**Archon AI** é um framework para orquestrar o desenvolvimento de software com IA de forma **confiável, rastreável e supervisionada**. Ele transforma a IA de um "copiloto imprevisível" em uma ferramenta de engenharia de software que segue um plano, respeita o contexto e permite a intervenção humana em pontos de controle.

O objetivo é simples: **deixar de ser um programador refém da IA e se tornar o arquiteto que comanda o ciclo de desenvolvimento.**

---

## 🚫 O Problema: O "Vibe Code"

Agentes de IA e assistentes de código autônomos, embora poderosos, frequentemente sofrem com:
- **Alucinações:** Inventam código ou funcionalidades.
- **Perda de Contexto:** Esquecem decisões importantes tomadas anteriormente.
- **Modificações Inesperadas:** Alteram arquivos sem um plano claro.
- **Falta de Rastreabilidade:** É impossível auditar *por que* uma decisão foi tomada.

Este framework foi criado para resolver esses problemas.

## ✅ A Solução: Uma Arquitetura Supervisionada e Orquestrada

O Archon AI atua como o **orquestrador principal**, preparando o terreno e gerando artefatos acionáveis para que **outros agentes de IA (como o Gemini CLI)** possam dar continuidade ao trabalho de forma autônoma e contextualizada. Isso é alcançado através de uma arquitetura de camadas:

1.  **🎓 Base de Conhecimento Contextual:** Utilizamos arquivos `.md` para definir o domínio, a arquitetura e as regras do projeto. Esta base de conhecimento serve como o "cérebro" contextual para a IA, garantindo que as decisões sejam tomadas com base em informações consistentes.
2.  **🛠️ Orquestrador FSM (Finite State Machine):** Uma Máquina de Estados Finitos garante que o projeto seja executado em uma sequência lógica (`planejamento → arquitetura → backend...`). O fluxo **pausa para validação humana** a cada etapa, evitando erros em cascata e permitindo a intervenção do supervisor.
3.  **📋 Engenharia de Prompt Avançada:** Prompts são gerados dinamicamente, utilizando a base de conhecimento para fornecer instruções precisas e contextualizadas à IA, em vez de comandos genéricos.
4.  **🧩 Geração de Roteiros para Agentes (`Gemini.md`):** Após cada etapa, o Archon gera um arquivo `Gemini.md` na pasta do projeto. Este arquivo atua como um **roteiro de execução** claro e estruturado para outros agentes de IA (como o Gemini CLI), contendo instruções sobre qual artefato analisar e quais ações tomar (criar arquivos, executar comandos, etc.).
5.  **📊 Memória Persistente e Rastreabilidade:** Um diário de execução (`diario_execucao.json`) registra cada passo, decisão e resultado. Isso garante **rastreabilidade, auditoria e a capacidade de retomar o trabalho** de onde parou, além de fornecer um histórico valioso para o aprendizado contínuo.

---

## 🚀 Fluxo de Trabalho Oficial

Siga estes passos para executar um projeto com o framework.

### Etapa 1: Gerar Base de Conhecimento

Descreva seu projeto para a IA gerar os documentos iniciais na pasta `projetos/`. Eles são o "cérebro" do seu projeto.

```
projetos/<nome-do-projeto>/base_conhecimento/
└── 01_base_conhecimento.md
```

> **Dica:** Você pode usar uma IA generativa para criar a primeira versão desses arquivos. Use um prompt como este e solicite que a IA gere os arquivos com as seções necessárias:


> *"Atue como um Arquiteto de Software e analista de negócios. Preciso de um estudo técnico completo para um [Seu Projeto]. 
Separe as informações nos seguintes arquivos: 

`plano_base.md` ('# Objetivo', '# Visão Geral', '# Público-Alvo', '# Escopo'),    
`arquitetura_tecnica.md` ('# Arquitetura', '# Tecnologias', '# Integrações', '# Fluxos Principais'),    
`regras_negocio.md` ('# Regras de Negócio', '# Restrições', '# Exceções', '# Decisões'),    
`fluxos_usuario.md` ('# Fluxos de Usuário', '# Navegação', '# Interações') e    
`backlog_mvp.md` ('# Funcionalidades', '# Critérios de Aceitação', '# Priorização')."    
`autenticação_backend.md` ('# sugestão de autenticação')

Com estas informações de pesquisa de mercado voce ja tem uma base solida para fazer o Upload do seu estudo para que o Archon -AI possa ter uma base de conhecimento completa do seu projeto.
> *

### Etapa 2: Validar a Base de Conhecimento

Após a geração, verifique se todos os documentos da base de conhecimento estão presentes e válidos. Se houver algum problema, revise a descrição do projeto na etapa anterior e gere novamente.

Status dos Documentos:
 Plano Base (Inválido)
 Arquitetura Técnica (Inválido)
 Regras de Negócio (Inválido)
 Fluxos de Usuário (Inválido)
 Backlog MVP (Inválido)
 Autenticação Backend (Inválido)

### Etapa 3: Nome do Projeto

Defina um identificador para seu projeto

Escolha um nome claro e descritivo para seu projeto. Este será usado para organizar arquivos e identificar o projeto no histórico. Use nomes como "E-commerce Digital", "Sistema de Gestão", "App Mobile Delivery", etc.


### Etapa 4: Linha do Tempo do Projeto

Acompanhe o progresso das etapas

A linha do tempo mostra o progresso do seu projeto através das diferentes fases de desenvolvimento. Cada etapa será automaticamente atualizada conforme o Archon AI progride.

Inicie o Projeto e a aplicação web, que serve como o painel de controle interativo da Linha do Tempo.


Após executar o comando, acesse http://127.0.0.1:5001 no seu navegador. O painel de controle irá:

1-Guiar você através de cada etapa do projeto.
2-Exibir o resultado gerado pela IA a cada passo.
3-Permitir que você aprove, repita, volte ou pause o fluxo com botões interativos.
4-Gerenciar os artefatos de código na pasta projetos/.
5-Registrar todo o progresso e decisões em logs/diario_execucao.json.

### Histórico de Execução

Visualize todas as ações e decisões

O histórico mantém um registro completo de todas as ações realizadas durante o desenvolvimento do projeto, incluindo aprovações, repetições, decisões do supervisor e observações importantes.

📊 Informações registradas:

• Etapas executadas e status
• Decisões do supervisor
• Data e hora das ações
• Observações e refinamentos

Agora voce tem um log de rastreamento feito pelo Archon AI para auditorias futuras.

### 🛠️ Ferramentas Recomendadas (Opcional)

### Pré-requisitos
- Python 3.9 ou superior

### 1. Configuração do Ambiente Python

1.  **Crie e ative um ambiente virtual:**
    ```bash
    # Crie o ambiente
    python -m venv venv
    
    # Ative no Windows
    .\venv\Scripts\activate
    
    # Ative no macOS/Linux
    source venv/bin/activate
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### 2. Variáveis de Ambiente

1.  **Crie o arquivo `.env`:** Se ele não existir, renomeie o arquivo `.env.example` para `.env`.
2.  **Adicione suas chaves:** Preencha o arquivo `.env` com suas chaves de API (GEMINI_API_KEY, STRIPE_SECRET_KEY, etc.).

### 3. Executando o Projeto

Com tudo configurado, você pode iniciar a aplicação de duas formas:

### 4. Iniciando o Servidor Web (Painel de Controle)

Para acessar a interface visual do Archon AI:

```bash
.\.venv\Scripts\python.exe app.py
```

#### Gemini CLI

Para prototipagem rápida de prompts e refinamento de artefatos diretamente do terminal, recomendamos a instalação do Gemini CLI.

1.  **Instale o `pipx`** (se ainda não tiver):
    ```bash
    python -m pip install --user pipx
    python -m pipx ensurepath
    ```
    *Lembre-se de reiniciar o terminal após este passo.*

2.  **Instale o Gemini CLI:**
    ```bash
    pipx install "google-generativeai[cli]"
    ```

3.  **Configure sua API Key:**
    ```bash
    gemini configure
    ```
4.  ***Direcione o Gemini CLI para o diretorio do seu projeto para que ele acompanhe a evolução dos artefatos criados a cada etapa supervisionada por você, e digite o seguinte comando:* 
    ```pws
    Gemini Leia o GEMINI.md
    ```

## Nova Funcionalidade: Geração de UI com Superdesign

Para acelerar a criação de interfaces de frontend de alta qualidade, o Archon AI pivotou de uma ponte customizada para o Figma para uma integração estratégica com o **Superdesign**, um poderoso agente de IA "Code-First" que opera diretamente no VS Code.

Esta abordagem permite que o Archon AI se concentre em sua principal força — a orquestração e governança do projeto — enquanto utiliza uma ferramenta especialista para a geração de UI. O Archon atua como um "Engenheiro de Prompt Sênior", guiando o desenvolvedor na criação de instruções perfeitas para o Superdesign.

### Instalação e Configuração do Superdesign

Para que o fluxo funcione, o ambiente do Superdesign precisa estar configurado corretamente no VS Code.

1.  **Clonar o Repositório do Superdesign:**
    ```bash
    git clone [https://github.com/superdesigndev/superdesign.git](https://github.com/superdesigndev/superdesign.git)
    ```

2.  **Abrir no VS Code:**
    Abra a pasta clonada (`superdesign`) no Visual Studio Code.

3.  **Instalar Dependências:**
    Abra um novo terminal dentro do VS Code e instale as dependências necessárias:
    ```bash
    npm install
    ```

4.  **Executar o Projeto:**
    Pressione `F5` no VS Code ou vá para o menu `Run > Start Debugging`. Isso iniciará uma nova janela do VS Code com a extensão Superdesign ativa e pronta para uso. É nesta **nova janela** que você irá trabalhar.

### Como Funciona a Integração com o Archon AI

O Archon AI agora possui um **"Construtor de Layout"** em seu painel web. Este construtor é a ponte entre a sua visão estratégica e a execução do Superdesign.

1.  **Acesse o Construtor de Layout no Painel Archon:**
    Durante a etapa de "Definição de Layout UI" do seu projeto no Archon, você encontrará o novo painel interativo.

2.  **Monte o Quebra-Cabeça da sua Interface:**
    Use o construtor para tomar decisões de alto nível sobre a arquitetura do seu frontend:
    * **Templates Prontos:** Carregue uma configuração pré-definida para acelerar o processo.
    * **Construtor de Layout:** Selecione, peça por peça, os componentes estruturais que você deseja (Header, Sidebar, Footer), com um preview dinâmico mostrando o resultado em tempo real.
    * **Componentes de Conteúdo:** Marque os componentes de UI que devem existir dentro da estrutura principal (Tabelas, Formulários, etc.).
    * **Diretrizes para o Agente:** Escolha o estilo visual (Tema) e outras opções técnicas.

3.  **Gere e Copie o Prompt Otimizado:**
    Enquanto você faz suas seleções, o Archon AI, na seção **"Prompt Gerado para Superdesign"**, escreve dinamicamente um prompt detalhado e estruturado. Este prompt traduz suas escolhas visuais em instruções claras que o Superdesign entende perfeitamente. Clique no botão **"Copiar"**.

4.  **Execute no Superdesign (VS Code):**
    * Vá para a janela do VS Code onde o Superdesign está rodando (a que abriu após você pressionar `F5`).
    * Abra a paleta de comandos (`Ctrl+Shift+P` ou `Cmd+Shift+P`).
    * Procure e selecione o comando `Super Design: Design with AI`.
    * Cole o prompt que você copiou do Archon AI na caixa de entrada.
    * O Superdesign iniciará seu fluxo de trabalho, seguindo as instruções para criar o layout, o tema e, finalmente, o código HTML.

Este fluxo de trabalho garante que, mesmo um desenvolvedor sem experiência em frontend, possa gerar interfaces complexas e visualmente coesas, mantendo a governança e a supervisão que são a marca registrada do Archon AI.

---

### ✅ Qualidade e Automação: Testes e CI/CD

Para garantir a estabilidade e a qualidade do Archon AI, o projeto vem com uma suíte de testes automatizados e um pipeline de integração contínua (CI).

#### Rodando os Testes Localmente

Utilizamos o `pytest` para os testes de unidade, que validam o comportamento do orquestrador principal (`fsm_orquestrador.py`).

Para executar os testes, basta rodar o seguinte comando na raiz do projeto:

```bash
pytest
```

O `pytest` encontrará e executará automaticamente todos os testes localizados na pasta `tests/`.

#### Integração Contínua (CI)

O repositório está configurado com o GitHub Actions (`.github/workflows/python.yml`). A cada `push` ou `pull request` para a branch `main`, o pipeline de CI é acionado para:

1.  Instalar todas as dependências.
2.  Rodar o script de validação da base de conhecimento (`valida_output.py`).
3.  Executar a suíte de testes completa com `pytest`.
   
collected 6 items

tests/test_fsm.py::test_initial_state       PASSED  [ 16%]    
tests/test_fsm.py::test_setup_project       PASSED  [ 33%]    
tests/test_fsm.py::test_action_approve      PASSED  [ 50%]    
tests/test_fsm.py::test_action_back         PASSED  [ 66%]    
tests/test_fsm.py::test_action_repeat       PASSED  [ 83%]    
tests/test_fsm.py::test_reset_project       PASSED  [100%]    

*================= 6 passed in 7.64s ==================*

Isso garante que novas alterações não quebrem funcionalidades existentes, mantendo a base de código sempre saudável.

## 📁 Estrutura de Diretórios

starter_kit_ia_agente/ 

  ├───.gitignore    
  ├───app.py    
  ├───auditoria_seguranca.py    
  ├───builder.config.json    
  ├───COMMIT_MSG.txt    
  ├───Dockerfile    
  ├───executar_funcionalidade.py    
  ├───fsm_orquestrador.py    
  ├───gerenciador_artefatos    
  ├───guia_projeto.py    
  ├───ia_executor.py    
  ├───LICENSE    
  ├───main.py    
  ├───memoria_conceitual.py    
  ├───prompt_templates.json    
  ├───prompts.py    
  ├───pytest.ini    
  ├───README.md    
  ├───registrador_tarefas.py    
  ├───relatorios.py    
  ├───requirements.txt    
  ├───runtime.txt    
  ├───valida_output.py    
  ├───vercel.json    
  ├───workflow.json    
  ├───__pycache__/    
  ├───.config/    
  ├───.github/    
  ├───.pytest_cache/    
  ├───agente/    
  ├───docs/    
  ├───projetos/    
  ├───static/    
  ├───templates/    
  ├───tests/    
  └───utils/    


---

# **🧩 Memória Persistente entre ciclos de execução

🧩 Implementar a “Memória Persistente” entre ciclos de execução 

Ou seja: fazer com que o sistema “lembre” de tudo que já fez — e possa continuar, replanejar ou revisar sem perder o fio da meada.

🧠 Por que isso é crucial?
Atualmente:

✅ A IA gera um plano com Fine-Tuning Conceitual    
✅ Um Agente executa a funcionalidade com contexto    
✅ O FSM controla a ordem das etapas    

Mas falta um mecanismo automático de “checkpoint” e rastreabilidade.

📌 O que entra agora: Camada 4 - Memória Persistente e Registro de Tarefas

🔧 Componentes a implementar:

Recurso								Função

diario_execucao.json				Armazena todas as execuções de tarefas por data, agente e estado atual
log_mvp.md							Registra decisões, falhas, insights e progresso por etapa do FSM
proximo_estado.json					Armazena qual foi o último estado concluído (permite retomar do ponto)

🛠 Exemplo de estrutura para diario_execucao.json
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

✅ Vantagens:

💾 Continuidade garantida: mesmo que o sistema feche, você retoma do ponto certo

🕵️ Auditoria automática: você pode ver onde a IA “decidiu” fazer algo

📊 Base para análise futura: pode transformar tudo isso em relatórios ou dashboards

⚙️ Com isso, você fecha:

Camada							Status		Descrição

1. Fine-Tuning Conceitual........✅	Feito....Plano carregado e contextualizado
2. Agente de Execução..............✅	Feito....IA com autonomia, FSM e modularidade
3. Engenharia de Prompt..........✅	Feito....Prompts claros e dinâmicos
4. Memória de Execução...........✅	Feito....Registro e continuidade automática

---

📦 Versão GitHub — o que seria?

É uma versão preparada para você subir direto pro GitHub, com:

✅ Estrutura padrão de repositório:

starter_kit_ia_agente/

├──.github/    
│    └─ workflows/    
│    └── python.yml    ←CI automatizado (testes e validação de código)    
├── README.md          ← Já gerado    
├── requirements.txt    
├── main.py    
├── agente/    
├── output/    
├── logs/    
└── ...

🔄 Workflow Automático (CI/CD com GitHub Actions):

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

✅ FLUXO RESUMIDO

| Etapa             | Comando                    | Descrição                                      |
|-------------------|----------------------------|------------------------------------------------|
| 1️⃣ Fine-Tuning     | python main.py             | Gera os arquivos conceituais                   |
| 2️⃣ Validação       | python valida_output.py    | Confere integridade dos arquivos               |
| 3️⃣ Execução FSM    | python fsm_orquestrador.py | Inicia o projeto guiado por FSM com supervisão |

---

### Vamos detalhar para reforçar o entendimento:

## Arquitetura e Stack Tecnológica

O projeto é construído sobre uma stack Python robusta:

-   **Linguagem:** Python
-   **Framework Web:** Flask
-   **Orquestração:** O `fsm_orquestrador.py` gerencia o fluxo do projeto como uma Máquina de Estados Finitos (FSM).
-   **Agente CLI:** O `agente/executor_agente.py` atua como um agente de linha de comando, lendo o `Gemini.md` e executando as ações necessárias.
-   **Interface:** O painel de controle (`dashboard.html`) é construído com HTML, TailwindCSS e Vanilla JavaScript (`main.js`), comunicando-se com o backend via API REST.

## 📚 Documentação Completa

Para um mergulho profundo no projeto, acesse a documentação detalhada:

-   **`01-visao-geral.md`**: Entenda o problema que o Archon resolve e a nossa arquitetura de orquestração de agentes.
-   **`02-instalacao.md`**: Passo a passo para configurar e rodar o projeto em seu ambiente local.
-   **`03-arquitetura.md`**: Uma análise aprofundada dos principais arquivos (`app.py`, `fsm_orquestrador.py`, `executor_agente.py`, etc.) e como eles se conectam.
-   **`04-workflow.md`**: Aprenda a editar o `workflow.json` para criar seus próprios fluxos de trabalho e como ele influencia a geração do `Gemini.md`.
-   **`05-contribuindo.md`**: Diretrizes para quem deseja contribuir com o projeto.
-   **`06-api-endpoints.md`**: Documentação completa dos endpoints da API REST.
-   **`07-deploy.md`**: Guia para deploy em produção (Render e Vercel) e configuração do Stripe.
-   **`08-auditoria-seguranca.md **: Histórico mantém um registro completo de todas as ações realizadas durante o desenvolvimento

---

# Linha do Tempo do Projeto:

Essa lista (Coleta de requisitos, Definição de arquitetura, Regras de negócio, Fluxos de usuário, Backlog MVP, Implementação do sistema) representa os estados da Máquina de Estados Finitos (FSM) do seu projeto. Eles são as etapas sequenciais que o agente de IA irá seguir, uma por uma.

# Painel de Pré-visualização do Resultado:

Cada vez que uma etapa é iniciada ou repetida, o sistema (através da função _run_current_step no fsm_orquestrador.py) gera um prompt específico para a IA (baseado nos seus arquivos em `projetos/<nome-do-projeto>/`) e simula a execução dessa IA. O resultado dessa simulação (que atualmente é um código Python de exemplo com o prompt usado) é o que aparece nesse painel. É a sua chance de revisar o trabalho da IA.

# Painel de Ações do Supervisor:

Os botões nesse painel são o seu controle total sobre o fluxo do projeto:
Aprovar: Você revisou o resultado da IA, está satisfeito, e quer que o projeto avance. Ao clicar em "Aprovar", o sistema registra essa etapa como concluída no log, e o FSM avança para a próxima etapa da linha do tempo, que será imediatamente executada e seu resultado aparecerá no painel de preview.
Repetir: Se o resultado da IA não foi o que você esperava, você pode clicar em "Repetir". O sistema irá re-executar a mesma etapa atual com o mesmo prompt, dando à IA uma nova chance de gerar um resultado melhor.
Voltar: Se você percebeu que um erro ou uma decisão errada foi tomada em uma etapa anterior, você pode usar "Voltar" para retroceder o FSM para uma etapa específica. Isso invalida o progresso das etapas subsequentes no log, permitindo que você refaça o caminho a partir daquele ponto.
Pausar: Permite que você pare a execução do orquestrador a qualquer momento, para fazer ajustes manuais nos arquivos, no código, ou simplesmente para continuar depois.

# Codificação e Progressão:

Quando você "Aprova" uma etapa, o executar_codigo_real é chamado, e ele salva o "código" gerado (que é o output da IA para aquela etapa) na pasta projetos/. A ideia é que, no futuro, essa "codificação" seja o código real de um microsserviço, um componente de frontend, um teste, etc.
O processo continua, etapa por etapa, até que a "Implementação do sistema" seja concluída. Uma vez que a última etapa é aprovada, o projeto é considerado finalizado.

# Conclusão

Foi Desenvolvido um sistema robusto que não apenas executa tarefas de forma automatizada, mas também permite que você, como engenheiro de software, mantenha o controle total sobre o processo. A IA é usada para acelerar e facilitar o trabalho, mas você tem a capacidade de supervisionar, intervir e corrigir o curso a qualquer momento.

Isso transforma o desenvolvimento de software com IA em um processo muito mais confiável e auditável. Você não está mais "vibrando" com a IA, mas sim orquestrando um fluxo de trabalho que combina a inteligência da máquina com a supervisão humana.

Em resumo, você transformou um processo linear e "cegamente" automatizado em um workflow híbrido, iterativo e supervisionado, onde a IA faz o trabalho pesado, mas você, o engenheiro, mantém o controle estratégico e a capacidade de intervir e corrigir o curso a qualquer momento.

É um sistema muito poderoso e bem pensado!

---

# 🏛️ Archon AI: Governe seu Workflow de IA

**Vamos Testar o Processo Completo**

Para garantir que tudo está funcionando como planejado, sugiro seguirmos este roteiro de teste:

1-Inicie o Servidor: Garanta que o servidor Flask esteja rodando (python app.py).
2-Acesse o Painel: Abra o [http://127.0.0.1:5000/] no seu navegador.
3-Download dos Templates: Clique no botão "Download Template de Documentos" para baixar o .zip com os arquivos base.
4-Upload da Base: Use o campo de upload para enviar os arquivos que você acabou de baixar (ou versões editadas deles, se preferir).
5-Nomeie o Projeto: Digite um nome para o projeto no campo correspondente (Ex: Teste-Completo-01).
6-Inicie o Projeto: Clique no botão "Iniciar Projeto".
7-Supervisão em Ação:
    *Observe o painel de pré-visualização carregar o resultado da primeira etapa.
    * Clique em "Aprovar" para avançar para a próxima etapa.
    * Verifique se a linha do tempo é atualizada e um novo resultado é carregado.
    * Teste os botões "Repetir" e "Voltar" para ver se o sistema se comporta como esperado.
8-Verifique os Artefatos: Enquanto o processo roda, verifique a pasta projetos/Teste-Completo-01/ no seu sistema de arquivos. Você deve ver os artefatos (.md, .py, etc.) sendo criados a cada etapa aprovada, junto com o README.md do projeto sendo atualizado.

---

## 🚀 Venda e Entrega Automatizada com Stripe


Além de ser um framework de desenvolvimento, o Archon AI vem preparado com uma **Landing Page (`landing.html`)** e um **backend de pagamentos** para que você possa vender e distribuir seu produto final.

A `landing.html` serve como sua vitrine digital, explicando o valor do seu projeto e guiando os usuários para a compra. O fluxo é totalmente automatizado:

1.  **CTA na Landing Page**: O usuário clica em um botão de compra.
2.  **Checkout Seguro**: Um popup solicita o e-mail do cliente e o redireciona para o ambiente de pagamento seguro do Stripe.
3.  **Confirmação de Pagamento**: Após o pagamento bem-sucedido, o Stripe envia uma notificação (webhook) para a rota `/webhook` da nossa aplicação.
4.  **Entrega Automatizada**: O backend verifica a notificação e dispara a ação final, como enviar um e-mail para o cliente com o link de acesso ao repositório privado do GitHub.

### Testando o Fluxo de Pagamento Localmente

Para testar todo o processo sem usar um cartão de crédito real, utilizamos a **Stripe CLI**:

1.  **Inicie o servidor Flask**:
    ```bash
    python app.py
    ```
2.  **Inicie o "ouvinte" do Stripe** em um segundo terminal. Ele irá encaminhar os eventos para o seu servidor local:
    ```bash
    stripe listen --forward-to http://127.0.0.1:5000/webhook
    ```
3.  O comando acima fornecerá uma **chave secreta de webhook** (`whsec_...`). Adicione-a ao seu arquivo `.env`.
4.  Acesse a `landing.html` no navegador, inicie a compra e use os cartões de teste do Stripe para finalizar o pagamento. Você verá os logs da confirmação no terminal do Flask.

---

## 🚀 Etapa 7: Deploy e Provisionamento

Esta etapa é onde seu projeto deixa de ser apenas código local e se torna uma aplicação real, acessível na internet. O painel de controle automatiza o processo de "deploy" (implantação) em plataformas de nuvem modernas.

### Entendendo os Serviços

-   **Vercel (Frontend):** A Vercel é usada para hospedar a parte visual da sua aplicação (o site ou painel com o qual o usuário interage). O processo de deploy envia todo o código do frontend para a Vercel, que o publica em uma URL pública.

-   **Supabase (Backend & Banco de Dados):** O Supabase fornece a infraestrutura de backend, incluindo o banco de dados, autenticação e armazenamento. O processo de deploy para o Supabase, chamado de "provisionamento", configura a estrutura do banco de dados na nuvem conforme definido pelo projeto.

-   **Stripe (Pagamentos):** O Stripe não é "implantado" da mesma forma. Ele é um serviço de pagamentos que você **integra** ao seu projeto. A configuração é feita adicionando as chaves de API do Stripe no seu arquivo `.env`, permitindo que sua aplicação (hospedada na Vercel) se comunique com o Stripe para processar pagamentos de forma segura.

### Pré-requisitos para o Deploy

Para que o deploy automatizado funcione, você precisa ter as ferramentas de linha de comando (CLI) da Vercel e do Supabase instaladas no seu sistema.

Abra seu terminal e instale-as globalmente usando `npm` (Node.js Package Manager):

```bash
# Instalar a CLI da Vercel
npm install -g vercel

# Instalar a CLI do Supabase
npm install -g supabase-cli
```

Após a instalação, você poderá usar a Etapa 7 no painel para inserir seus tokens de API e implantar seus projetos com um único clique.

---

## 🛠️ Contribuindo para o Projeto

Ficamos felizes com o seu interesse em contribuir para o Archon AI! Toda contribuição, desde a correção de um simples erro de digitação até a implementação de uma nova funcionalidade, é muito bem-vinda.

Este documento fornece diretrizes para garantir que o processo de contribuição seja o mais suave e eficaz possível para todos.

## Como Contribuir

Existem várias maneiras de contribuir com o projeto:

*   **Reportando Bugs:** Se você encontrar um comportamento inesperado ou um erro.
*   **Sugerindo Melhorias:** Se você tem uma ideia para uma nova funcionalidade ou uma melhoria em uma existente.
*   **Escrevendo Código:** Corrigindo um bug ou implementando uma nova funcionalidade.
*   **Melhorando a Documentação:** Se você encontrar algo que não está claro ou que poderia ser melhor explicado.

## Reportando Bugs

Bons relatórios de bugs são extremamente úteis. Antes de criar um novo relatório, por favor, verifique a [lista de issues](https://github.com/seu-usuario/seu-repositorio/issues) para ver se o problema já foi reportado.

Ao criar um novo relatório de bug, por favor, inclua o máximo de detalhes possível:

1.  **Use um título claro e descritivo.**
2.  **Descreva o problema:** Explique o que aconteceu e o que você esperava que acontecesse.
3.  **Passos para reproduzir:** Forneça um passo a passo detalhado de como reproduzir o bug.
4.  **Ambiente:** Inclua detalhes sobre o seu ambiente, como sistema operacional, versão do Python.
5.  **Logs ou Screenshots:** Se aplicável, adicione logs de erro do console ou screenshots que demonstrem o problema.

## Sugerindo Melhorias e Novas Funcionalidades

Adoramos receber novas ideias! Para sugerir uma melhoria ou uma nova funcionalidade, crie uma [nova issue](https://github.com/roger-rsk/Archon-AI-Starter-Kit/issues).

Por favor, inclua:

1.  **Um título claro e descritivo.**
2.  **Descrição do problema:** Explique o problema que sua sugestão resolve. Por que essa melhoria é necessária?
3.  **Solução proposta:** Descreva em detalhes como a funcionalidade deveria funcionar.
4.  **Alternativas consideradas:** Se você pensou em outras abordagens, mencione-as e explique por que a sua proposta é a melhor.

## Contribuindo com Código (Pull Requests)

Se você deseja corrigir um bug ou implementar uma nova funcionalidade, o processo é o seguinte:

1.  **Fork o Repositório:** Crie um fork do projeto para a sua conta do GitHub.

2.  **Clone o seu Fork:**
    ```bash
    git clone https://github.com/seu-usuario/Archon-AI-Starter-Kit.git
    cd Archon-AI-Starter-Kit
    ```

3.  **Crie uma Nova Branch:** Crie uma branch descritiva para suas alterações.
    ```bash
    # Para uma nova funcionalidade:
    git checkout -b feature/nome-da-funcionalidade

    # Para uma correção de bug:
    git checkout -b fix/descricao-do-bug
    ```

4.  **Faça suas Alterações:** Implemente o código, seguindo as convenções de estilo do projeto.

5.  **Execute os Testes:** Antes de enviar, certifique-se de que todos os testes estão passando.
    ```bash
    pytest
    ```

6.  **Faça o Commit das suas Alterações:** Use mensagens de commit claras e descritivas.
    ```bash
    git commit -m "feat: Adiciona funcionalidade X que faz Y"
    ```

7.  **Envie para o seu Fork:**
    ```bash
    git push origin feature/nome-da-funcionalidade
    ```

8.  **Abra um Pull Request (PR):** Vá para o repositório original no GitHub e abra um Pull Request da sua branch para a branch `main` do projeto principal.

    *   No PR, forneça uma descrição clara das alterações, vincule a issue relacionada (se houver) e explique o "porquê" e o "como" das suas mudanças.

---

## (PyInstaller) Como GerarArquivos Executáveis .exe?PyInstaller

Para transformar sua aplicação Python em um executável .exe para Windows (ou arquivos equivalentes para macOS/Linux), você precisa de uma ferramenta que "empacote" seu código, todas as suas dependências e o próprio interpretador Python em um único arquivo ou pasta.

A ferramenta mais popular e robusta para isso é o PyInstaller.

**Aqui está um guia passo a passo de como você faria isso:*

Passo 1: Instalar o PyInstaller
No seu ambiente virtual, rode o seguinte comando:
Bash
```
pip install pyinstaller
```
Passo 2: Preparar o Script de Entrada
O PyInstaller precisa de um único arquivo Python para usar como ponto de partida. Se você quer empacotar a lógica do seu `executor` (que chama a CLI), você teria um script principal para isso. Vamos chamá-lo de `run_archon_cli.py`.

Passo 3: Gerar o Executável
Abra o terminal na pasta do seu projeto e execute o comando do PyInstaller. A forma mais comum é:
Bash
```
pyinstaller --onefile run_archon_cli.py
```
`--onefile`: Este comando instrui o PyInstaller a agrupar tudo em um único arquivo .exe, o que é muito conveniente para a distribuição.

Se sua aplicação tiver uma interface gráfica (GUI), você pode adicionar a flag `--windowed` (ou `--noconsol`) para que o terminal preto não apareça quando o usuário executar o programa. Para uma ferramenta de linha de comando, você não usa essa flag.

Passo 4: Encontrar o .exe
Após o PyInstaller terminar o processo, ele criará algumas pastas. O seu arquivo executável final estará dentro da pasta dist. É este arquivo .exe que você distribuiria.

---

Agradecemos antecipadamente por sua contribuição!
Criado por Rogerio Matos com suporte do Google Developer

---

"Deixe de ser um programador refém da IA. Torne-se o arquiteto que comanda todo o ciclo."

---

Painel do Projeto
Monitore o Progresso, revise os resultados e gerencie as ações.

**Gerador de Propostas de Software**
# Estrutura para o Gerador de Propostas de Software
Orçamento com dados dos clientes para apresentação e refinamento das necessidadsespara o projet.

# Gerar Base de Conhecimento
Estrutura do Projeto
projetos/<nome-do-projeto>/

├── output\
│   ├── 01_base_conhecimento.md
│   ├── 02_arquitetura_tecnica.md
│   ├── 03_regras_negocio.md
│   ├── 04_fluxos_usuario.md
│   ├── 05_backlog_mvp.md
│   └── 06_autenticacao_backend.md
├── artefatos\
│   ├── 01_Análise_de_requisitos.md
│   ├── 02_Prototipação.md
│   ├── 03_Arquitetura_de_software.md
│   ├── 04_Desenvolvimento_backend.md
│   ├── 05_Desenvolvimento_frontend.md
│   ├── 06_Testes_e_validação.md
│   ├── 07_Deploy.md
│   └── 08_Monitoramento_e_melhoria_contínua.md
├── GEMINI.md
├── README.md
└── diario_execucao.json

## Validação da Base de Conhecimento
Etapas cobertas (Linha do Tempo do Projeto):

**Análise de requisitos**
**Prototipação**
**Arquitetura de software**
**Desenvolvimento backend**
**Desenvolvimento frontend**
**Testes e validação**
**Deploy**
**Monitoramento e melhoria contínua**
   
>> Etapa: Análise de Requisitos
+ Prompt Positivo:
   (o que a AI deve fazer)
- Prompt Negativo:
   (o que a AI deve evitar)

>> Etapa: Prototipação
+ Prompt Positivo:
- Prompt Negativo:

>> Apos "Aporovar e Iniciar o Projeto" Para cada tipo de sistema (SaaS, MicroSaaS, PWA, MVP, ERP) gerar os Prompts a AIArchon Painel de Pré-visualização do Resultado nos apresenta sua abordagem.

# Linha do Tempo do Projeto
## Painel de Pré-visualização do Resultado
Visualize o resultado da IA antes de aprovar:
- Resultado da IA para a etapa atual
- Prompt usado para gerar o resultado

## Painel de Ações do Supervisor
Controle total sobre o fluxo do projeto:
- Botões para Aprovar, Repetir, Voltar ou Pausar

## Codificação e Progressão
Após aprovação, o artefato gerado é salvo na pasta do projetos/<nome-do-projeto>/

## Conclusão
O Archon AI transforma o desenvolvimento de software com IA em um processo supervisionado e auditável, onde a IA faz o trabalho pesado, mas você mantém o controle estratégico e a capacidade de intervir e corrigir o curso a qualquer momento.

# Histórico de Execução
Visualize todas as ações e decisões:

 Informações registradas:
• Etapas executadas e status
• Decisões do supervisor
• Data e hora das ações
• Observações e refinamentos


# Definindo Layout UI
Defina a estrutura e os componentes da interface do usuário para a aplicação.

# Deploy e Provisionamento
O Archon AI vem preparado para deploy e provisionamento em plataformas de nuvem modernas, como Vercel e Supabase, além de integração com Stripe para pagamentos.

## Integração com Stripe
A integração com o Stripe permite que você venda e distribua seu produto final de forma automatizada, com uma landing page e um backend de pagamentos prontos para uso.

## Testando o Fluxo de Pagamento Localmente
Para testar o fluxo de pagamento sem usar um cartão de crédito real, utilize a Stripe CLI para simular eventos de pagamento e notificações.

## Integração com Supabase
O Supabase fornece a infraestrutura de backend, incluindo banco de dados, autenticação e armazenamento. O processo de deploy para o Supabase configura a estrutura do banco de dados na nuvem conforme definido pelo projeto.

## Integração com Vercel
A Vercel é usada para hospedar a parte visual da sua aplicação (o site ou painel com o qual o usuário interage). O processo de deploy envia todo o código do frontend para a Vercel, que o publica em uma URL pública.