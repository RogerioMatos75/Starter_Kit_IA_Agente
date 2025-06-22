# Executor de tarefas do agente
from pandora_agent.root_agent import root_agent

def executar_prompt(prompt):
    agente = root_agent()
    resposta = agente.do_process(prompt)
    print(f"🔍 Resposta da IA: {resposta}")

# Teste local
if __name__ == "__main__":
    executar_prompt("Qual é o próximo passo para iniciar o MVP?")
