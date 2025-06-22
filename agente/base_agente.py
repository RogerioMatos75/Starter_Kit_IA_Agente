# Base do agente FSM
class BaseAgente:
    def __init__(self, nome="Agente", descricao=""):
        self.nome = nome
        self.descricao = descricao

    def responder(self, entrada: str) -> str:
        raise NotImplementedError("Este método deve ser sobrescrito pelo agente específico.")
