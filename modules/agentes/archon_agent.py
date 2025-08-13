import os
from ia_executor import executar_prompt_ia, IAExecutionError

class ArchonAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def consult_supervisor(self, query: str, context: str) -> str:
        """
        Permite que o supervisor consulte o Archon AI para refinar artefatos ou obter insights.
        O Archon AI atua como um especialista que refina o conteúdo do painel de pré-visualização.
        """
        if not self.api_key:
            raise IAExecutionError("API Key não configurada para o Archon Agent.")

        prompt = (
            f"Você é o Archon AI, um assistente de engenharia de software especialista e de classe mundial. "
            f"Sua função é auxiliar o supervisor humano a refinar artefatos e fornecer insights técnicos. "
            f"Seja conciso, objetivo e direto ao ponto. Use o contexto fornecido para responder à consulta do supervisor.\n\n"
            f"**Contexto do Artefato Atual:**\n"
            f"```markdown\n{context}\n```\n\n"
            f"**Consulta do Supervisor:**\n"
            f"```\n{query}\n```\n\n"
            f"Com base no contexto e na consulta, refine o artefato ou responda à pergunta do supervisor. "
            f"Se a consulta for um pedido de refinamento, forneça o artefato refinado. "
            f"Se for uma pergunta, responda diretamente. Não inclua explicações adicionais ou formatação além do conteúdo solicitado."
        )

        try:
            refined_content = executar_prompt_ia(prompt, api_key=self.api_key)
            return refined_content
        except IAExecutionError as e:
            raise IAExecutionError(f"Falha na consulta ao Archon Agent: {e}")
        except Exception as e:
            raise IAExecutionError(f"Erro inesperado no Archon Agent: {e}")
