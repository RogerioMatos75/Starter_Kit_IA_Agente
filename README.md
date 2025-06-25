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

## 📁 Estrutura de Diretórios

starter_kit_ia_agente/ 

├── main.py # Gera estudo de domínio (Fine-Tuning conceitual)  
├── executar_funcionalidade.py # Executor generativo com prompt  
├── memoria_conceitual.py # Gera prompts baseados no domínio salvo   
├── registrador_tarefas.py # Registro de progresso + exportação PDF   
├── prompts.py # Lista de prompts parametrizados   
├── output/ # Geração do Fine-Tuning Conceitual   
│ ├── plano_base.md   
│ ├── arquitetura_tecnica.md   
│ ├── regras_negocio.md   
│ ├── fluxos_usuario.md   
│ └── backlog_mvp.md   
├── logs/   
│ ├── diario_execucao.json # Histórico completo   
│ └── log_execucao.pdf # Exportação legível   
| └── proximo_estado.json # Último estado concluído   
├── app.py                    # 🚀 Servidor web e API (Flask)
├── fsm_orquestrador.py       # 🧠 Core: O orquestrador FSM
├── valida_output.py          # ✅ Core: Validador da base de conhecimento
├── guia_projeto.py           # 📚 Helper: Módulo para ler a base de conhecimento
├── templates/                # 🎨 Frontend: Arquivos HTML
│   └── index.html
├── static/                   # 🎨 Frontend: Arquivos JS, CSS
│   └── js/
│       └── main.js 
├── projetos/     # <-- Aqui ficam os códigos gerados   
│   ├── mvp1/   
│   └── saas2/   
├── runtime.txt         # opcional, mas recomendado   
├── Procfile            # opcional, mas recomendado   
├── Dockerfile         # opcional, mas recomendado   
├── .gitignore          # Ignora arquivos desnecessários no Git
└── requirements.txt   
yaml
Sempre exibir os detalhes

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

1. Fine-Tuning Conceitual	  ✅        Feito	Plano carregado e contextualizado
2. Agente de Execução		    ✅        Feito	IA com autonomia, FSM e modularidade
3. Engenharia de Prompt		  ✅        Feito	Prompts claros e dinâmicos
4. Memória de Execução		  ✅        Feito	Registro e continuidade automática

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
Criado por Rogerio Matos com suporte do ChatGPT / Gemini
---
"Deixe de ser um programador refém da IA. Torne-se o arquiteto que comanda todo o ciclo."
---

# 🛠️ Contribuindo para o Projeto
<!--
[PROMPT_SUGGESTION]Como podemos adicionar uma visualização dos logs (`diario_execucao.json`) na interface?[/PROMPT_SUGGESTION]
[PROMPT_SUGGESTION]Explique em detalhes como o método `_load_progress` no `fsm_orquestrador.py` funciona.[/PROMPT_SUGGESTION]
-->
