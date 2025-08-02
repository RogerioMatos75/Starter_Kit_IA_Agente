from ia_executor import executar_prompt_ia, IAExecutionError

def enrich_artifact(original_content, system_type, stage_name, prompt_positivo, prompt_negativo):
    """
    Usa um agente de IA para enriquecer o conteúdo de um artefato de projeto.

    Ele recebe o conteúdo original, o tipo de sistema, a etapa e os prompts base
    (positivo e negativo) e gera uma seção complementar com instruções detalhadas
    para a próxima fase de desenvolvimento.

    Args:
        original_content (str): O conteúdo do manifesto original.
        system_type (str): O tipo de sistema (ex: 'SaaS').
        stage_name (str): O nome da etapa (ex: 'Análise de Requisitos').
        prompt_positivo (str): A instrução positiva base do arquivo de regras.
        prompt_negativo (str): A instrução negativa base do arquivo de regras.

    Returns:
        str: O conteúdo original concatenado com a seção de instruções gerada pela IA,
             ou o conteúdo original com uma mensagem de erro se a IA falhar.
    """
    # Monta o prompt para o agente de enriquecimento
    enrichment_prompt = f"""Você é um especialista em arquitetura de software para sistemas '{system_type}'.
Sua tarefa é enriquecer o seguinte documento, que é um artefato da etapa '{stage_name}' de um projeto.

**Documento Original:**
---
{original_content}
---

**Sua Missão:**
Com base no documento acima, gere uma seção complementar chamada 'Instruções para o Agente de Desenvolvimento'.
Esta seção deve conter um 'Prompt Complementar', 'Instruções Positivas' e 'Instruções Negativas' para guiar a próxima fase de desenvolvimento, seguindo as diretrizes abaixo.

**Diretrizes para a Geração:**

*   **Prompt Complementar:** Crie um parágrafo que resuma o objetivo principal deste artefato e o conecte com a próxima fase de desenvolvimento, levando em conta que este é um sistema do tipo '{system_type}'.
*   **Instruções Positivas (O que FAZER):** Use a seguinte instrução como base e expanda-a se necessário, aplicando-a ao contexto do 'Documento Original'.
    *   Base: "{prompt_positivo}"
*   **Instruções Negativas (O que EVITAR):** Use a seguinte instrução como base e expanda-a se necessário, aplicando-a ao contexto do 'Documento Original'.
    *   Base: "{prompt_negativo}"

Formate a saída EXATAMENTE como no exemplo abaixo, sem adicionar nenhuma outra explicação ou texto introdutório.

**Formato de Saída Esperado:**

<br>
<hr>
<br>

### 🧠 Instruções para o Agente de Desenvolvimento

**📝 Prompt Complementar:**
(Parágrafo gerado pela IA)

**👍 Instruções Positivas:**
(Instrução positiva gerada/adaptada pela IA)

**👎 Instruções Negativas:**
(Instrução negativa gerada/adaptada pela IA)
"""

    try:
        print(f"[Enrichment Agent] Chamando IA para enriquecer o artefato da etapa: '{stage_name}'...")
        complementary_section = executar_prompt_ia(enrichment_prompt)
        print(f"[Enrichment Agent] Seção complementar gerada com sucesso.")
        
        # Concatena o conteúdo original com a nova seção gerada
        enriched_content = f"{original_content}\n{complementary_section}"
        return enriched_content

    except IAExecutionError as e:
        print(f"[ERRO no Enrichment Agent] Falha ao executar a IA: {e}")
        error_message = f"""<br><hr><br>
### 🧠 Instruções para o Agente de Desenvolvimento

**Erro na Geração:**
Ocorreu uma falha ao tentar gerar as instruções complementares para este artefato.
Detalhes: {e}
"""
        return f"{original_content}\n{error_message}"
