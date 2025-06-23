# 💡 Starter Kit: Agente de IA com Workflow Supervisionado

Este projeto é um framework para orquestrar o desenvolvimento de software com IA de forma **confiável, rastreável e supervisionada**. Ele transforma a IA de um "copiloto imprevisível" em uma ferramenta de engenharia de software que segue um plano, respeita o contexto e permite a intervenção humana em pontos de controle.

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

Siga estes três passos para executar um projeto com o framework.

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

### Etapa 3: Executar o Orquestrador Supervisionado

Inicie o processo de desenvolvimento controlado pela Máquina de Estados Finitos.

```bash
python fsm_orquestrador.py
```

O orquestrador irá:
1.  Ler a base de conhecimento da pasta `output/`.
2.  Executar cada etapa do projeto em ordem.
3.  **Pausar a cada etapa**, permitindo que você aprove (`s`), repita (`r`), volte (`v`) ou pare (`p`) o fluxo.
4.  Gerar os artefatos de código na pasta `projetos/`.
5.  Registrar todo o progresso e decisões em `logs/diario_execucao.json`.

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

Criado por Rogerio Matos com suporte do ChatGPT / Gemini
---
"Deixe de ser um programador refém da IA. Torne-se o arquiteto que comanda todo o ciclo."
