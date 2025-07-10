#!/usr/bin/env python3
"""
Script de inicialização do servidor Archon AI
Este script inicia o servidor Flask com as configurações adequadas.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_requirements():
    """Verifica se as dependências estão instaladas"""
    try:
        import flask
        import flask_cors
        import google.generativeai
        print("✅ Dependências principais encontradas")
        return True
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        print("Execute: pip install -r requirements.txt")
        return False

def check_environment():
    """Verifica variáveis de ambiente necessárias"""
    env_vars = {
        'GEMINI_API_KEY': 'Chave da API do Google Gemini (opcional)',
        'FLASK_SECRET_KEY': 'Chave secreta do Flask (opcional)',
        'STRIPE_SECRET_KEY': 'Chave secreta do Stripe (opcional)',
        'STRIPE_PUBLIC_KEY': 'Chave pública do Stripe (opcional)'
    }
    
    print("\n🔍 Verificando variáveis de ambiente:")
    for var, description in env_vars.items():
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: Configurada")
        else:
            print(f"⚠️  {var}: Não configurada ({description})")
    
    # Verifica se existe arquivo .env
    env_file = Path('.env')
    if env_file.exists():
        print("✅ Arquivo .env encontrado")
    else:
        print("ℹ️  Arquivo .env não encontrado (opcional)")

def start_server():
    """Inicia o servidor Flask"""
    print("\n🚀 Iniciando servidor Archon AI...")
    print("📍 URL: http://localhost:5001")
    print("🔗 Dashboard: http://localhost:5001/dashboard")
    print("\n💡 Para parar o servidor, pressione Ctrl+C\n")
    
    try:
        # Inicia o servidor Flask
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor interrompido pelo usuário")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao iniciar o servidor: {e}")
        return False
    except FileNotFoundError:
        print("\n❌ Arquivo app.py não encontrado")
        return False
    
    return True

def main():
    """Função principal"""
    print("=" * 60)
    print("🤖 ARCHON AI - INICIALIZADOR DO SERVIDOR")
    print("=" * 60)
    
    # Verifica se estamos no diretório correto
    if not Path('app.py').exists():
        print("❌ Arquivo app.py não encontrado no diretório atual")
        print("Certifique-se de estar no diretório raiz do projeto Archon AI")
        return False
    
    # Verifica dependências
    if not check_requirements():
        return False
    
    # Verifica ambiente
    check_environment()
    
    # Pergunta se o usuário quer continuar
    print("\n" + "=" * 60)
    response = input("Deseja iniciar o servidor? (s/N): ").lower().strip()
    
    if response in ['s', 'sim', 'y', 'yes']:
        return start_server()
    else:
        print("👋 Operação cancelada pelo usuário")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
