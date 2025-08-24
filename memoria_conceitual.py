import os

DOCUMENTOS = [
    "documentacao/base_conhecimento.md",
    "documentacao/arquitetura_tecnica.md",
    "documentacao/regras_negocio.md",
    "documentacao/fluxos_usuario.md",
    "documentacao/backlog_mvp.md",
    "documentacao/autenticacao_backend.md"
]

def carregar_memoria():
    memoria = []
    for doc in DOCUMENTOS:
        try:
            with open(doc, "r", encoding="utf-8") as f:
                memoria.append(f"## {doc}\n{f.read()}\n")
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {doc}")
    return "\n".join(memoria)

# Nenhuma referência a agentes ou IA neste módulo.
