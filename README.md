# 💡 Starter Kit - Workflow Híbrido de 3 Camadas com IA

Este projeto implementa uma arquitetura de desenvolvimento com IA confiável e supervisionável, superando os limites do "Vibe Code" com editores autônomos e sem rastreabilidade. Aqui utilizamos uma combinação de três camadas para gerar, planejar e executar projetos como MVPs, Micro-SaaS ou protótipos.

---

💻 **Vibe Code e IAs no Desenvolvimento Moderno**

🧠 De Super Prompts a Soluções Reais

🚫 Problema:

Assistentes de código como Copilot, Cursor, Trae e outros cometem:
- Alucinações
- Modificações inesperadas
- Perda de contexto
- Erros em código complexo

✅ Solução Estratégica:

**Workflow Híbrido de Três Camadas**
1. 🎓 *Fine-Tuning:* Torna o modelo especializado no seu código.
2. 🛠️ *Agente de IA:* Executa planos passo a passo com memória de estado.
3. 📋 *Engenharia de Prompt:* Orientação clara e precisa para cada tarefa.

🎯 Resultado:

Menos erros. Mais produtividade. Total controle.

---

💡 Dicas de Ouro para Projetos Futuros com as 3 Camadas:

	Situação						Ação Ideal
	
🧪 MVP novo com estrutura clara		Use Etapa 2 + 3
📈 Produto recorrente ou complexo	Use todas (1 + 2 + 3)
🤖 Agente sem rumo					Reforce a engenharia de prompt (Etapa 3)
🐞 IA quebrando código antigo		Use Fine-Tuning com histórico de código (Etapa 1)
⚙️ Projeto que precisa evoluir		Agente com memória + planejamento (Etapa 2)

🧰 Ferramentas que você pode usar:

Camada						Ferramentas Sugeridas
Fine-Tuning					DeepSeek, Ollama + QLoRA, OpenAI + datasets JSONL
Agente de IA				CrewAI, LangGraph, AutoGen, OpenDevin, Python com FSM
Engenharia de Prompt		Typst (documentação), markdown modular, PromptLayer

---

✅ Prompt Ideal para Estudo de Domínio (pré-Fine-Tuning)
Você pode usar algo como:


Atue como um Arquiteto de Software e analista de negócios. 
Preciso de um estudo técnico completo para criar um projeto a ser definido. 
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

Preciso que voce separe todas essas informações nesses 5 arquivos para a implementação de futuros projetos MVPs

plano_base.md
arquitetura_tecnica.md
regras_negocio.md
fluxos_usuario.md
backlog_mvp.md

---

## 🧠 Arquitetura Híbrida de 3 Camadas

1. **🎓 Fine-Tuning Conceitual**
   - Simula um treinamento conceitual da IA usando pesquisas generativas (ex: Gemini, Claude, ChatGPT) para gerar:
     - Estudo de domínio
     - Arquitetura técnica
     - Regras de negócio
     - Fluxos de usuário
     - Backlog de funcionalidades

2. **🛠️ Agente FSM (Finite State Machine)**
   - Máquina de Estados controlando a ordem de execução das etapas:
     - `planejamento → arquitetura → backend → frontend → testes → deploy → finalizado`
   - Cada etapa executa uma tarefa específica via agente IA
   - Confirmação manual após cada etapa evita erros em cascata

3. **📋 Engenharia de Prompt Avançada**
   - Para cada tarefa, comandos detalhados são enviados ao executor generativo
   - Prompts organizados, precisos e reutilizáveis via `prompts.py`
   
4. **🧩 Memória Persistente entre ciclos de execução**

   - Memória Persistente entre ciclos de execução — é fundamental para evitar alucinações, perda de contexto e garantir rastreabilidade em projetos com IA e agentes autônomos.

Sem essa camada, IDEs e agentes de codificação podem:

Esquecer decisões anteriores,
Repetir erros,
Perder o “fio da meada” do projeto,
Gerar código incoerente ou fora do escopo.
Com a memória persistente (como o diario_execucao.json e logs detalhados), o sistema:

Sabe exatamente onde parou,
Pode retomar, revisar ou replanejar sem perder histórico,
Garante que cada etapa é baseada em decisões e contexto reais, não em “alucinações” do modelo.

---

📦 Estrutura Sugerida do Fine-Tuning Conceitual (via Prompt/Plano)

output/
├── plano_base.md
├── arquitetura_tecnica.md        <-- estrutura por camadas, tech stack
├── regras_negocio.md             <-- decisões de negócio e domínio
├── fluxos_usuario.md             <-- experiência e lógica de navegação
└── backlog_mvp.md                <-- features mínimas para validação

---

# **🎓 Fine-Tuning Conceitual**

Fluxo Completo com Fine-Tuning Conceitual:

1. Fase de Estudo (Você faz a “Pesquisa com IA”)
Você dispara o estudo com:

```bash
python main.py
```
Isso gera:

plano_base.md
arquitetura_tecnica.md
regras_negocio.md
fluxos_usuario.md
backlog_mvp.md

💡 Esses arquivos simulam um treinamento personalizado, porque contêm todo o “know-how” do projeto — como se fossem embeddings ou tokens treinados.

2. Fase de Especialização (Sem Re-Treinar!)
O módulo memoria_conceitual.py:

Lê esses arquivos
Gera prompts automáticos com base neles
Alimenta o Agente (CrewAI, AutoGen, LangGraph...)

⚙️ Aqui acontece a “mágica” — a IA age com contexto especializado, sem você ter que ficar explicando tudo de novo.

3. Fase de Execução (MVP/SaaS na prática)

Você chama:

```bash
python executar_funcionalidade.py --func login_usuario
```
Ele:

Gera o prompt já adaptado
Dispara o agente
Cria o código (com base no plano original)

🤖 Resultado Final:

Você não depende de “Super Prompt”
A IA nunca perde o contexto
O processo é modular, escalável e controlável
Pode versionar tudo com Git!

---

# **🛠️ Agente FSM (Finite State Machine)**

🧠 O que é um Orquestrador FSM?

FSM = Finite State Machine → Máquina de Estados Finitos
Orquestrador FSM = Um controlador que define o fluxo exato de execução de um processo, com base em estados e transições controladas.

🎮 Analogia Rápida:
Pense num videogame:

Estado: Menu, Jogando, Pausado, Game Over

Transições: Start, Pause, Resume, Die

Você nunca pula do Menu direto para o Game Over.
Tudo segue um fluxo lógico e validado.

🔁 Aplicando ao seu projeto de IA:
O orquestrador FSM atua como um "GPS do Agente de IA":

	Ele sabe onde está
	Sabe para onde pode ir
	Sabe quando e como mudar de estado

🛠️ Exemplo prático no seu contexto:
Você quer que a IA execute seu MVP em etapas bem definidas, por exemplo:

[Planejamento] --> [Arquitetura Técnica] --> [Implementação Backend] --> [Frontend] --> [Testes] --> [Deploy]
Com um FSM, isso vira um gráfico de estados tipo:

stateDiagram
    [*] --> Planejamento
    Planejamento --> Arquitetura
    Arquitetura --> Backend
    Backend --> Frontend
    Frontend --> Testes
    Testes --> Deploy
    Deploy --> [*]
	
E cada vez que a IA completa um passo, o FSM libera o próximo.

🎯 Vantagens de usar FSM como orquestrador:

	Benefício						Descrição
✅ Previsibilidade					A IA só avança quando um passo anterior é concluído com sucesso
✅ Controle de Fluxo				Você pode interromper, repetir ou pular etapas com segurança
✅ Debug mais fácil					Se der erro, você sabe em que etapa o sistema parou
✅ Ideal para MVPs/Backlogs			MVP = sequência clara de features; FSM define o fluxo delas
✅ Integra com Agentes e Prompts	Cada estado pode acionar um prompt ou agente específico

🔧 Ferramentas para usar FSM com IA:

	Python puro com biblioteca transitions
	LangGraph (FSM + LLMs de forma visual)
	AutoGen com controle de tarefas baseado em step_id e state
	CrewAI com "task routing" baseado em status

---

# **📋 Engenharia de Prompt Avançada**

🔁 Execução FSM com Supervisão

```bash
python fsm_orquestrador.py
```
A cada etapa, o sistema irá pausar:

⏸️ Pausado após etapa 'BACKEND'. Pressione [Enter] para continuar para a próxima...
📄 Log Automatizado
Cada execução é salva em logs/diario_execucao.json

Também é exportada para logs/log_execucao.pdf

📌 Ideia Central
Este projeto transforma o uso de IAs generativas em um processo confiável:

Supervisão manual entre as etapas
Registro de progresso com histórico persistente
Separação entre pesquisa, execução e controle

Ideal para MVPs, SaaS modulares ou projetos acadêmicos que precisam de organização e rastreabilidade com IA.
"""
🔁 Resultado: Você transformou o Vibe Code em um fluxo confiável

		Histórico real de execução
		Rastreamento de decisões
		Capacidade de retomar de onde 

---


## 📁 Estrutura de Diretórios

starter_kit_ia_agente/
├── main.py # Gera estudo de domínio (Fine-Tuning conceitual)
├── executar_funcionalidade.py # Executor generativo com prompt
├── memoria_conceitual.py # Gera prompts baseados no domínio salvo
├── fsm_orquestrador.py # Controlador de FSM com pausa
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
├── output/
├── logs/
├── projetos/        # <-- Aqui ficam os códigos gerados
│   ├── mvp1/
│   └── saas2/
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

Recurso							Função

diario_execucao.json			Armazena todas as execuções de tarefas por data, agente e estado atual
log_mvp.md						Registra decisões, falhas, insights e progresso por etapa do FSM
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

Camada						Status		Descrição

1. Fine-Tuning Conceitual	✅ Feito	Plano carregado e contextualizado
2. Agente de Execução		✅ Feito	IA com autonomia, FSM e modularidade
3. Engenharia de Prompt		✅ Feito	Prompts claros e dinâmicos
4. Memória de Execução		✅ Feito	Registro e continuidade automática

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
Etapa	Comando	Descrição
1️⃣ Fine-Tuning	python main.py	Gera os arquivos conceituais
2️⃣ Validação	python valida_output.py	Confere integridade dos arquivos
3️⃣ Execução FSM	python fsm_orquestrador.py	Inicia o projeto guiado por FSM com supervisão


---

Criado por Rogerio Matos com suporte do ChatGPT / Gemini
---
"Deixe de ser um programador refém da IA. Torne-se o arquiteto que comanda todo o ciclo."
