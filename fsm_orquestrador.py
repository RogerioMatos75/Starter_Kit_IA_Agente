# Orquestrador FSM com pausa para confirmação

import time

class FSMOrquestrador:
    def __init__(self, estados):
        self.estados = estados
        self.estado_atual = 0

    def executar(self):
        for i, estado in enumerate(self.estados):
            print(f"Executando etapa {i+1}: {estado['nome']}")
            resultado = estado["acao"]()
            print(f"Resultado: {resultado}")
            input("Pressione Enter para prosseguir para o próximo estado...\n")

def exemplo_acao():
    return "Ação executada com sucesso!"

if __name__ == "__main__":
    fsm = FSMOrquestrador([
        {"nome": "Coleta de requisitos", "acao": exemplo_acao},
        {"nome": "Definição de arquitetura", "acao": exemplo_acao},
        {"nome": "Implementação do sistema", "acao": exemplo_acao},
    ])
    fsm.executar()
