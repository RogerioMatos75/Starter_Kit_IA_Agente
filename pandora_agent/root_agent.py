import os
from dotenv import load_dotenv
from google_adk.agents import Agent
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

DOCUMENTOS = [
    "documentacao/plano_base.md",
    "documentacao/arquitetura_tecnica.md",
    "documentacao/regras_negocio.md",
    "documentacao/fluxos_usuario.md",
    "documentacao/backlog_mvp.md"
]

def carregar_conhecimento():
    memoria = []
    script_dir = os.path.dirname(__file__)
    for doc in DOCUMENTOS:
        try:
            doc_path = os.path.join(script_dir, "..", doc)
            with open(doc_path, "r", encoding="utf-8") as f:
                memoria.append(f"## {doc}\n{f.read()}\n")
        except FileNotFoundError:
            print(f"AVISO: Arquivo de documentação não encontrado: '{doc_path}'")
    return "\n".join(memoria)

class PandoraAgent(Agent):
    def __init__(self, api_key, contexto):
        super().__init__()
        if not api_key:
            raise ValueError("API_KEY do Google não foi encontrada. Verifique seu arquivo .env.")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")
        self.contexto = contexto
        self.system_prompt = f"""Você é a Pandora, uma IA especialista.
        Sua memória conceitual é a seguinte:\n{self.contexto}
        Responda às perguntas com base estritamente nesta memória.
        Se a resposta não estiver na sua memória, diga 'Não tenho informações sobre isso.'"""
        print("\n🔮 Pandora inicializada com base no contexto fornecido.\n")

    def do_process(self, prompt: str) -> str:
        print(f"\nRecebido prompt: {prompt}")
        response = self.model.generate_content(
            self.system_prompt + "\n\nPergunta do usuário: " + prompt
        )
        print(f"Resposta gerada: {response.text}")
        return response.text

    def supervisionar_etapa(self, etapa: str, artefato: str) -> str:
        """
        Analisa o artefato da etapa, sugere melhorias e aguarda confirmação do usuário para prosseguir.
        """
        prompt_supervisao = (
            f"Você é uma agente supervisora de qualidade e ciclo de desenvolvimento.\n"
            f"Analise a etapa '{etapa}' e o seguinte artefato de código/documentação:\n{artefato}\n"
            "- Liste pontos positivos e negativos.\n"
            "- Sugira melhorias técnicas e de arquitetura.\n"
            "- Pergunte ao usuário: 'Deseja prosseguir para a próxima etapa? (sim/não)'\n"
            "Se não houver informações suficientes, peça mais detalhes ao usuário.\n"
        )
        response = self.model.generate_content(self.system_prompt + "\n" + prompt_supervisao)
        print(f"\n[SUPERVISÃO] Análise da etapa '{etapa}':\n{response.text}")
        return response.text

def root_agent():
    print("🔥 Carregando PandoraAgent como root_agent via ADK...")
    memoria_conceitual = carregar_conhecimento()
    return PandoraAgent(api_key=API_KEY, contexto=memoria_conceitual)
