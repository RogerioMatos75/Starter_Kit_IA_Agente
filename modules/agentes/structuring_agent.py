# /modules/agentes/structuring_agent.py

from ia_executor import executar_prompt_ia, IAExecutionError

def structure_idea(raw_idea: str) -> str:
    """
    Recebe uma ideia de projeto bruta do usuário e a transforma em um texto estruturado,
    ideal para ser usado como um prompt de alta qualidade para a próxima etapa de IA.

    Args:
        raw_idea: O texto livre fornecido pelo usuário.

    Returns:
        Um texto estruturado e bem formatado.
    """
    
    prompt_especializado = f'''
    Você é um Analista de Negócios Sênior e especialista em engenharia de requisitos.
    Sua tarefa é pegar uma ideia de projeto, muitas vezes vaga ou informal, e estruturá-la de forma clara e organizada.
    O objetivo é preparar este texto para que outro especialista de IA possa usá-lo para criar uma proposta técnica detalhada.

    **NÃO** crie a proposta final. Apenas organize a ideia inicial.

    **Ideia Bruta do Cliente:**
    ---
    {raw_idea}
    ---

    **Sua Tarefa:**
    Analise a ideia acima e reescreva-a no seguinte formato estruturado. Seja conciso e extraia a essência de cada tópico. Se uma informação não estiver presente, deixe o tópico com um "A ser definido".

    **Formato de Saída (Use exatamente este layout):**

    **1. Título Provisório do Projeto:**
    [Sugira um nome claro e curto para o projeto]

    **2. Problema a ser Resolvido:**
    [Descreva em uma ou duas frases o principal problema que o projeto visa solucionar]

    **3. Objetivo Principal:**
    [Descreva em uma frase o resultado final desejado do projeto]

    **4. Público-Alvo:**
    [Identifique para quem este projeto se destina]

    **5. Funcionalidades Essenciais (MVP - Mínimo Produto Viável):**
    - [Funcionalidade 1]
    - [Funcionalidade 2]
    - [Funcionalidade 3]
    - ...

    **6. Requisitos Não-Funcionais (Se mencionados):**
    - [Ex: Precisa ser rápido, seguro, funcionar em celulares, etc.]

    **7. Informações Adicionais Relevantes:**
    [Qualquer outro detalhe importante mencionado pelo cliente]

    **Instrução Final:** Gere APENAS o texto estruturado acima. Não adicione saudações, explicações ou qualquer texto fora do formato solicitado.
    '''

    try:
        print("[Agente Estruturador] Estruturando a ideia bruta...")
        structured_text = executar_prompt_ia(prompt_especializado)
        print("[Agente Estruturador] Ideia estruturada com sucesso.")
        return structured_text
    except IAExecutionError as e:
        print(f"[Agente Estruturador] Erro ao estruturar ideia: {e}")
        return f"Ocorreu um erro ao tentar estruturar a ideia: {e}"
