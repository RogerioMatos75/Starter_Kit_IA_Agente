from datetime import datetime
import os

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
