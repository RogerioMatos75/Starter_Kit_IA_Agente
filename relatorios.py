from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# --- CONFIGURAÇÃO DE CAMINHOS ABSOLUTOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def exportar_log_txt(logs, output_path):
    """
    Gera um relatório de log em formato .txt simples e legível.
    """
    # Garante que o caminho de saída seja absoluto, se não for já
    if not os.path.isabs(output_path):
        output_path = os.path.join(BASE_DIR, output_path)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("Diário de Execução - Projeto Archon AI\n")
        f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        if not logs:
            f.write("Nenhum registro de log encontrado ainda.\n")
            return
        for log in reversed(logs):
            f.write(f"Etapa: {log.get('etapa', '-')}\n")
            f.write(f"Tarefa: {log.get('tarefa', '-')}\n")
            f.write(f"Status: {log.get('status', '-')}\n")
            f.write(f"Decisão: {log.get('decisao', '-')}\n")
            f.write(f"Data/Hora: {datetime.fromisoformat(log.get('data_hora')).strftime('%d/%m/%Y %H:%M')}\n")
            f.write(f"Observação: {log.get('observacao', '-')}\n")
            f.write("-"*40 + "\n")
    print(f"[RELATÓRIO] Log em TXT gerado com sucesso em: {output_path}")

def gerar_log_pdf(logs, output_path):
    """
    Gera um relatório de log em formato PDF.
    """
    if not os.path.isabs(output_path):
        output_path = os.path.join(BASE_DIR, output_path)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Diário de Execução - Projeto Archon AI", styles['h1']))
    story.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    if not logs:
        story.append(Paragraph("Nenhum registro de log encontrado ainda.", styles['Normal']))
    else:
        for log in reversed(logs):
            story.append(Paragraph(f"<b>Etapa:</b> {log.get('etapa', '-')}", styles['Normal']))
            story.append(Paragraph(f"<b>Tarefa:</b> {log.get('tarefa', '-')}", styles['Normal']))
            story.append(Paragraph(f"<b>Status:</b> {log.get('status', '-')}", styles['Normal']))
            story.append(Paragraph(f"<b>Decisão:</b> {log.get('decisao', '-')}", styles['Normal']))
            story.append(Paragraph(f"<b>Data/Hora:</b> {datetime.fromisoformat(log.get('data_hora')).strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
            story.append(Paragraph(f"<b>Observação:</b> {log.get('observacao', '-')}", styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))
            story.append(Paragraph("-"*40, styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))
    
    try:
        doc.build(story)
        print(f"[RELATÓRIO] Log em PDF gerado com sucesso em: {output_path}")
    except Exception as e:
        print(f"[ERRO] Falha ao gerar PDF em {output_path}: {e}")