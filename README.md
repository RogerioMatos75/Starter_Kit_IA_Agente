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

## ✅ A Solução: Uma Arquitetura Supervisionada de 4 Camadas

1.  **🎓 Fine-Tuning Conceitual:** Em vez de treinar um modelo, criamos uma **base de conhecimento** com arquivos `.md` que definem o domínio, a arquitetura e as regras do projeto. Isso serve como o "cérebro" contextual da IA.
2.  **🛠️ Orquestrador FSM (Finite State Machine):** Uma Máquina de Estados Finitos garante que o projeto seja executado em uma sequência lógica (`planejamento → arquitetura → backend...`). O fluxo **pausa para validação humana** a cada etapa, evitando erros em cascata.
3.  **📋 Engenharia de Prompt Avançada:** Os prompts são gerados dinamicamente, usando a base de conhecimento para dar instruções precisas e contextualizadas à IA, em vez de comandos genéricos.
4.  **🧩 Memória Persistente:** Um diário de execução (`diario_execucao.json`) registra cada passo, decisão e resultado. Isso garante **rastreabilidade, auditoria e a capacidade de retomar o trabalho** de onde parou.

---

Este repositório contém o "Starter Kit" completo, com um backend em Python (Flask) e um frontend interativo para você começar a construir seus próprios projetos com IA de forma governada.

## Arquitetura e Stack Tecnológica

O projeto é dividido em dois componentes principais que trabalham em conjunto:

### 1. Core (Backend & Painel)
- **Linguagem:** Python
- **Framework:** Flask
- **Lógica Principal:** O `fsm_orquestrador.py` gerencia o fluxo do projeto como uma Máquina de Estados Finitos (FSM), garantindo que cada etapa seja executada em sequência.
- **Interface:** O painel de controle (`dashboard.html`) é construído com HTML, TailwindCSS e Vanilla JavaScript (`main.js`), comunicando-se com o backend via API REST.


## Documentação Completa

Para um mergulho profundo no projeto, a próxima etapa é criar a documentação detalhada. Sugiro a seguinte estrutura dentro de uma pasta `/docs`:

- **`01-visao-geral.md`**: Entenda o problema que o Archon resolve e a nossa arquitetura de 4 camadas.
- **`02-instalacao.md`**: Passo a passo para configurar e rodar o projeto em seu ambiente local (Python, Node.js, .env).
- **`03-arquitetura.md`**: Uma análise aprofundada dos principais arquivos (`app.py`, `fsm_orquestrador.py`, etc.) e como eles se conectam.
- **`04-workflow.md`**: Aprenda a editar o `workflow.json` para criar seus próprios agentes e fluxos de trabalho.
- **`05-contribuindo.md`**: Diretrizes para quem deseja contribuir com o projeto.

---

## 📚 Documentação Detalhada

Acesse a documentação completa do projeto para detalhes, exemplos e guias práticos:

- [Visão Geral](docs/01-visao-geral.md)
- [Instalação](docs/02-instalacao.md)
- [Arquitetura](docs/03-arquitetura.md)
- [Workflow](docs/04-workflow.md)
- [Contribuindo](docs/05-contribuindo.md)

---

## ⚙️ Instalação e Configuração

**### Pré-requisitos**
- Python 3.9 ou superior

**### 1. Configuração do Ambiente Python**

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

**### 2. Variáveis de Ambiente**

1.  **Crie o arquivo `.env`:** Se ele não existir, renomeie o arquivo `.env.example` para `.env`.
2.  **Adicione suas chaves:** Preencha o arquivo `.env` com suas chaves de API (GEMINI_API_KEY, STRIPE_SECRET_KEY, etc.).

Com o ambiente configurado, você está pronto para seguir o **Fluxo de Trabalho Oficial**.

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
    stripe listen --forward-to http://127.0.0.1:5001/webhook
    ```
3.  O comando acima fornecerá uma **chave secreta de webhook** (`whsec_...`). Adicione-a ao seu arquivo `.env`.
4.  Acesse a `landing.html` no navegador, inicie a compra e use os cartões de teste do Stripe para finalizar o pagamento. Você verá os logs da confirmação no terminal do Flask.

---

## ☁️ Deploy em Produção com Render

Para que sua landing page e o backend fiquem acessíveis na internet, o projeto está configurado para deploy na plataforma **Render**, uma solução PaaS (Platform as a Service) moderna e fácil de usar.

O arquivo `render.yaml` na raiz do projeto define a "infraestrutura como código", instruindo o Render a:
- Usar Python 3.11.
- Instalar as dependências do `requirements.txt`.
- Iniciar a aplicação usando **Gunicorn**, um servidor WSGI robusto para produção (substituindo o servidor de desenvolvimento do Flask).
- Carregar as variáveis de ambiente (suas chaves do Stripe) de um grupo seguro.

Para fazer o deploy, basta conectar sua conta do Render ao repositório no GitHub e criar um "New Blueprint Instance". O Render cuidará do resto.

---

## 🚀 Fluxo de Trabalho Oficial

Siga estes passos para executar um projeto com o framework.

### Etapa 1: Criar a Base de Conhecimento

Crie ou gere os seguintes arquivos na pasta `output/`. Eles são o "cérebro" do seu projeto.

```
output/
├── plano_base.md
├── arquitetura_tecnica.md
├── regras_negocio.md
├── fluxos_usuario.md
└── backlog_mvp.md
```

> **Dica:** Você pode usar uma IA generativa para criar a primeira versão desses arquivos. Use um prompt como este e solicite que a IA gere os arquivos com as seções necessárias:

>
> *"Atue como um Arquiteto de Software e analista de negócios. Preciso de um estudo técnico completo para um [Seu Projeto]. Separe as informações nos seguintes arquivos: `plano_base.md` ('# Objetivo', '# Visão Geral', '# Público-Alvo', '# Escopo'), `arquitetura_tecnica.md` ('# Arquitetura', '# Tecnologias', '# Integrações', '# Fluxos Principais'), `regras_negocio.md` ('# Regras de Negócio', '# Restrições', '# Exceções', '# Decisões'), `fluxos_usuario.md` ('# Fluxos de Usuário', '# Navegação', '# Interações') e `backlog_mvp.md` ('# Funcionalidades', '# Critérios de Aceitação', '# Priorização')."
> *

### Etapa 2: Validar a Base de Conhecimento

Antes de executar, rode o script de validação para garantir que a base de conhecimento está completa e bem-estruturada.

```bash
python valida_output.py
```

Este script funciona como um "portão de qualidade" (quality gate), evitando que o orquestrador inicie com informações ausentes ou malformadas.

### Etapa 3: Executar o Painel de Controle Web
Inicie a aplicação web, que serve como o painel de controle interativo do projeto.

```bash
python app.py
```
Após executar o comando, acesse http://127.0.0.1:5001 no seu navegador. O painel de controle irá:

1-Guiar você através de cada etapa do projeto.
2-Exibir o resultado gerado pela IA a cada passo.
3-Permitir que você aprove, repita, volte ou pause o fluxo com botões interativos.
4-Gerenciar os artefatos de código na pasta projetos/.
5-Registrar todo o progresso e decisões em logs/diario_execucao.json.

### 🛠️ Ferramentas Recomendadas (Opcional)

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

tests/test_fsm.py::test_initial_state        PASSED      [ 16%]
tests/test_fsm.py::test_setup_project        PASSED      [ 33%]
tests/test_fsm.py::test_action_approve       PASSED      [ 50%]
tests/test_fsm.py::test_action_back          PASSED      [ 66%]
tests/test_fsm.py::test_action_repeat        PASSED      [ 83%]
tests/test_fsm.py::test_reset_project        PASSED      [100%]

*================= 6 passed in 7.64s ==================*

Isso garante que novas alterações não quebrem funcionalidades existentes, mantendo a base de código sempre saudável.


---

## 📁 Estrutura de Diretórios

starter_kit_ia_agente/   
├── .github/    
└── workflows/    
└── python.yml      # Pipeline de Integração Contínua (CI)    
├── cache/                  # Cache de resultados da IA para acelerar repetições    
├── documentos_base/        # Templates .md para a base de conhecimento    
├── logs/                   # Logs de execução e checkpoints do FSM    
├── output/                 # Base de conhecimento (.md) do projeto atual    
├── projetos/               # Artefatos e código gerados pela IA para cada projeto    
├── static/                 # Arquivos estáticos (CSS, JS, Imagens)    
│       ├── assets/    
│       └── js/    
│           ├── landing.js      # Lógica da Landing Page e popup de pagamento    
│           └── main.js         # Lógica do Painel de Controle (Dashboard)             
├── templates/              # Templates HTML do Flask    
│   ├── dashboard.html      # O painel de controle do supervisor    
│   ├── landing.html        # A página de vendas do produto    
│   ├── success.html        # Página de sucesso pós-pagamento    
│   └── cancel.html         # Página de cancelamento de pagamento    
├── tests/                  # Testes automatizados (pytest)    
├── .env                    # Arquivo para variáveis de ambiente (chaves secretas)    
├── .gitignore              # Arquivos e pastas a serem ignorados pelo Git    
├── app.py                  # 🚀 Servidor web (Flask), API e lógica de webhooks    
├── fsm_orquestrador.py     # 🧠 Core: O orquestrador da Máquina de Estados Finitos    
├── guia_projeto.py         # Helper para ler a base de conhecimento    
├── ia_executor.py          # Módulo que interage com a API da IA (Gemini)    
├── render.yaml             # Configuração de deploy para a plataforma Render    
├── requirements.txt        # Dependências do projeto Python    
├── valida_output.py        # Validador da base de conhecimento    
└── workflow.json           # Define as etapas e prompts do projeto    

---

# **🧩 Memória Persistente entre ciclos de execução

🧩 Implementar a “Memória Persistente” entre ciclos de execução 

Ou seja: fazer com que o sistema “lembre” de tudo que já fez — e possa continuar, replanejar ou revisar sem perder o fio da meada.

🧠 Por que isso é crucial?
Atualmente:

A IA gera um plano com Fine-Tuning Conceitual ✅
Um Agente executa a funcionalidade com contexto ✅
O FSM controla a ordem das etapas ✅

Mas falta um mecanismo automático de “checkpoint” e rastreabilidade.

📌 O que entra agora: Camada 4 - Memória Persistente e Registro de Tarefas

🔧 Componentes a implementar:

Recurso							      Função

diario_execucao.json			Armazena todas as execuções de tarefas por data, agente e estado atual
log_mvp.md						    Registra decisões, falhas, insights e progresso por etapa do FSM
proximo_estado.json				Armazena qual foi o último estado concluído (permite retomar do ponto)

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

Camada						          Status		Descrição

1. Fine-Tuning Conceitual	    ✅        Feito	Plano carregado e contextualizado
2. Agente de Execução		    ✅        Feito	IA com autonomia, FSM e modularidade
3. Engenharia de Prompt		    ✅        Feito	Prompts claros e dinâmicos
4. Memória de Execução		    ✅        Feito	Registro e continuidade automática

---

📦 Versão GitHub — o que seria?

É uma versão preparada para você subir direto pro GitHub, com:

✅ Estrutura padrão de repositório:

starter_kit_ia_agente/

├── .github/   
│   └── workflows/    
│       └── python.yml      ← CI automatizado (testes e validação de código)   
├── README.md               ← Já gerado   
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

🚀 Fluxo Oficial de Projeto com IA Supervisível
🧠 ETAPA 1 — FINE-TUNING CONCEITUAL (Base de Conhecimento)
```bash
python main.py
```
📂 Gera:

plano_base.md
arquitetura_tecnica.md
regras_negocio.md
fluxos_usuario.md
backlog_mvp.md

Esses arquivos são o alicerce conceitual do projeto.

✅ ETAPA 2 — VALIDAÇÃO DO CONTEXTO
```bash
python valida_output.py
```

📌 Valida se todos os arquivos da base estão:

Presentes
Com conteúdo mínimo esperado
Estruturados corretamente

Garantia de qualidade antes de avançar para a execução.

🧭 ETAPA 3 — EXECUÇÃO DO FSM (Orquestração Modular com Supervisão)
```bash
python fsm_orquestrador.py
```

O que acontece:

📖 Carrega os arquivos .md como memória conceitual.

🧩 Executa o projeto passo a passo, com:

Geração automática dos prompts.
Execução das tarefas reais (ex: gerar arquivos, estruturar código).
Confirmação manual a cada etapa.
Registro completo da jornada em diario_execucao.json + .pdf.

🔁 Permite retomar de onde parou, em caso de pausa ou erro.

---

✅ FLUXO RESUMIDO
| Etapa               | Comando                     | Descrição                                      |
|---------------------|-----------------------------|------------------------------------------------|
| 1️⃣ Fine-Tuning     | python main.py              | Gera os arquivos conceituais                   |
| 2️⃣ Validação       | python valida_output.py     | Confere integridade dos arquivos               |
| 3️⃣ Execução FSM    | python fsm_orquestrador.py  | Inicia o projeto guiado por FSM com supervisão |

---

### Vamos detalhar para reforçar o entendimento:

# Linha do Tempo do Projeto:

Essa lista (Coleta de requisitos, Definição de arquitetura, Regras de negócio, Fluxos de usuário, Backlog MVP, Implementação do sistema) representa os estados da Máquina de Estados Finitos (FSM) do seu projeto. Eles são as etapas sequenciais que o agente de IA irá seguir, uma por uma.

# Painel de Pré-visualização do Resultado:

Cada vez que uma etapa é iniciada ou repetida, o sistema (através da função _run_current_step no fsm_orquestrador.py) gera um prompt específico para a IA (baseado nos seus arquivos output/*.md) e simula a execução dessa IA. O resultado dessa simulação (que atualmente é um código Python de exemplo com o prompt usado) é o que aparece nesse painel. É a sua chance de revisar o trabalho da IA.

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
2-Acesse o Painel: Abra o [http://127.0.0.1:5001/dashboard](http://127.0.0.1:5001/dashboard) no seu navegador.
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

Criado por Rogerio Matos com suporte do ChatGPT / Gemini

---

"Deixe de ser um programador refém da IA. Torne-se o arquiteto que comanda todo o ciclo."

---

## 🛠️ Contribuindo para o Projeto
