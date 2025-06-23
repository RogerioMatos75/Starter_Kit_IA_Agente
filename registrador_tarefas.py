import datetime
import os
import json
from fpdf import FPDF
from datetime import datetime

def registrar_log(titulo, mensagem, pasta="logs"):
    data = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"{titulo}_{data}.txt"
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, nome_arquivo)

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(f"{mensagem}\n")
    print(f"📝 Log salvo em: {caminho}")

LOG_PATH = os.path.join("logs", "diario_execucao.json")
PDF_PATH = os.path.join("logs", "log_execucao.pdf")

def exportar_log_para_pdf():
    if not os.path.exists(LOG_PATH):
        print("Arquivo de log não encontrado.")
        return
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        logs = json.load(f)
    if not logs:
        print("Nenhum registro encontrado no log.")
        return
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Histórico de Execução do Projeto", ln=True, align="C")
    pdf.ln(5)
    for entry in logs:
        pdf.set_font("Arial", style="B", size=11)
        pdf.cell(0, 8, f"Etapa: {entry['etapa']}", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 8, f"Status: {entry['status']} | Decisão: {entry['decisao']} | Data/Hora: {entry['data_hora']}", ln=True)
        if entry.get("observacao"):
            pdf.multi_cell(0, 8, f"Observação: {entry['observacao']}")
        pdf.ln(2)
        pdf.cell(0, 0, "-"*60, ln=True)
        pdf.ln(2)
    pdf.output(PDF_PATH)
    print(f"PDF gerado em: {PDF_PATH}")

if __name__ == "__main__":
    exportar_log_para_pdf()
