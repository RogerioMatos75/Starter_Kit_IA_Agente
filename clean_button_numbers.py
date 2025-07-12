#!/usr/bin/env python3
"""
Script para remover números de linha dos botões no dashboard.html
"""

import re

def clean_button_numbers():
    """Remove números indesejados dos botões de navegação"""
    
    with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Padrões para limpar
    patterns = [
        # Remove números seguidos de espaços antes de onclick
        (r'(\s+)(\d+)(\s+onclick=)', r'\1\3'),
        
        # Remove números seguidos de espaços antes de class
        (r'(\s+)(\d+)(\s+class=)', r'\1\3'),
        
        # Remove números seguidos de espaços antes de > 
        (r'(\s+)(\d+)(\s+>)', r'\1\3'),
        
        # Remove números seguidos de espaços antes de ← Etapa Anterior
        (r'(\s+)(\d+)(\s+← Etapa Anterior)', r'\1\3'),
        
        # Remove números seguidos de espaços antes de Próxima Etapa
        (r'(\s+)(\d+)(\s+Próxima Etapa)', r'\1\3'),
        
        # Remove números seguidos de espaços antes de </button>
        (r'(\s+)(\d+)(\s+</button>)', r'\1\3'),
    ]
    
    # Aplicar limpeza
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    # Limpeza adicional para casos específicos
    # Remove linhas que são apenas números
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Se a linha contém apenas espaços e um número, pular
        if re.match(r'^\s*\d+\s*$', line):
            continue
        cleaned_lines.append(line)
    
    content = '\n'.join(cleaned_lines)
    
    # Salvar arquivo limpo
    with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Números removidos dos botões!")

if __name__ == "__main__":
    clean_button_numbers()
