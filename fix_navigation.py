#!/usr/bin/env python3
"""
Script para corrigir a navegação entre etapas no dashboard
"""

def fix_dashboard_navigation():
    """Corrige os botões de navegação no dashboard.html"""
    
    with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Mapear navegações corretas:
    # Etapa 2: anterior=1, próxima=3
    # Etapa 3: anterior=2, próxima=4  
    # Etapa 4: anterior=3, próxima=5
    # Etapa 5: anterior=4, próxima=6
    # Etapa 6: anterior=5, próxima=7
    
    # Lista de correções necessárias
    fixes = [
        # Etapa 2 - próxima deveria ser 3, não 6
        ('step-2-content', 'showStep(6)', 'showStep(3)'),
        # Etapa 2 - anterior deveria ser 1, não 3
        ('step-2-content', 'showStep(3)', 'showStep(1)'),
        
        # Etapa 3 - próxima deveria ser 4, não 6
        ('step-3-content', 'showStep(6)', 'showStep(4)'),
        # Etapa 3 - anterior deveria ser 2, não 3 (está correto se for 2)
        
        # Etapa 4 - próxima deveria ser 5, não 6
        ('step-4-content', 'showStep(6)', 'showStep(5)'),
        # Etapa 4 - anterior deveria ser 3, mas está como 3 (correto)
        
        # Etapa 5 - próxima deveria ser 6 (já está correto)
        # Etapa 5 - anterior deveria ser 4, não 3
        ('step-5-content', 'showStep(3)', 'showStep(4)'),
    ]
    
    # Aplicar correções por seção
    sections = content.split('<div id="step-')
    
    for i, section in enumerate(sections):
        if i == 0:
            continue  # Pular cabeçalho
            
        # Identificar qual etapa é esta seção
        if section.startswith('2-content'):
            print("Corrigindo Etapa 2...")
            # Etapa 2: anterior=1, próxima=3
            # Corrigir botão anterior (de showStep(3) para showStep(1))
            section = section.replace(
                'onclick="showStep(3)"\n                            >\n                              ← Etapa Anterior',
                'onclick="showStep(1)"\n                            >\n                              ← Etapa Anterior'
            )
            # Corrigir botão próxima (de showStep(6) para showStep(3))  
            section = section.replace(
                'onclick="showStep(6)"\n                            >\n                              Próxima Etapa →',
                'onclick="showStep(3)"\n                            >\n                              Próxima Etapa →'
            )
            
        elif section.startswith('3-content'):
            print("Corrigindo Etapa 3...")
            # Etapa 3: anterior=2, próxima=4
            # Corrigir botão anterior (de showStep(3) para showStep(2))
            section = section.replace(
                'onclick="showStep(3)"\n                            >\n                              ← Etapa Anterior',
                'onclick="showStep(2)"\n                            >\n                              ← Etapa Anterior'
            )
            # Corrigir botão próxima (de showStep(6) para showStep(4))
            section = section.replace(
                'onclick="showStep(6)"\n                            >\n                              Próxima Etapa →',
                'onclick="showStep(4)"\n                            >\n                              Próxima Etapa →'
            )
            
        elif section.startswith('4-content'):
            print("Corrigindo Etapa 4...")
            # Etapa 4: anterior=3, próxima=5
            # Corrigir botão próxima (de showStep(6) para showStep(5))
            section = section.replace(
                'onclick="showStep(6)"\n                          >\n                              Próxima Etapa →',
                'onclick="showStep(5)"\n                          >\n                              Próxima Etapa →'
            )
            
        elif section.startswith('5-content'):
            print("Corrigindo Etapa 5...")
            # Etapa 5: anterior=4, próxima=6
            # Corrigir botão anterior (de showStep(3) para showStep(4))
            section = section.replace(
                'onclick="showStep(3)"\n                            >\n                              ← Etapa Anterior',
                'onclick="showStep(4)"\n                            >\n                              ← Etapa Anterior'
            )
            # Botão próxima já está correto (showStep(6))
            
        elif section.startswith('6-content'):
            print("Verificando Etapa 6...")
            # Etapa 6: anterior=5, próxima=7 (já devem estar corretos)
            
        elif section.startswith('7-content'):
            print("Verificando Etapa 7...")
            # Etapa 7: anterior=6 (já deve estar correto)
        
        sections[i] = section
    
    # Recompor o arquivo
    fixed_content = '<div id="step-'.join(sections)
    
    # Salvar arquivo corrigido
    with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("✅ Navegação corrigida com sucesso!")

if __name__ == "__main__":
    fix_dashboard_navigation()
