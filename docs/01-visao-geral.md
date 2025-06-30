# Visão Geral e Filosofia do Archon AI

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

Com esta base, o Archon AI estabelece um paradigma onde a velocidade da IA é combinada com o rigor da engenharia de software tradicional.