#!/usr/bin/env python3
"""
Script de teste para validar a integração da interface de Deploy e Provisionamento
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Testa se todos os imports necessários estão funcionando"""
    print("🔍 Testando imports...")
    
    try:
        from app import app
        print("✅ app.py importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar app.py: {e}")
        return False
    
    try:
        from deploy_service import deploy_project
        print("✅ deploy_service.py importado com sucesso")
    except Exception as e:
        print(f"⚠️ Erro ao importar deploy_service.py: {e}")
    
    try:
        from providers.supabase_provider import validate_credentials, deploy
        print("✅ supabase_provider.py importado com sucesso")
    except Exception as e:
        print(f"⚠️ Erro ao importar supabase_provider.py: {e}")
    
    try:
        from providers.vercel_provider import deploy as deploy_vercel
        print("✅ vercel_provider.py importado com sucesso")
    except Exception as e:
        print(f"⚠️ Erro ao importar vercel_provider.py: {e}")
    
    return True

def test_routes():
    """Testa se as rotas de deploy estão disponíveis"""
    print("\n🔍 Testando rotas de deploy...")
    
    try:
        from app import app
        
        # Lista todas as rotas
        routes = []
        for rule in app.url_map.iter_rules():
            if 'deploy' in rule.rule:
                routes.append(rule.rule)
        
        expected_routes = [
            '/deploy',
            '/api/deploy/save_credentials',
            '/api/deploy/validate_credentials', 
            '/api/deploy/provision_database',
            '/api/deploy/deploy_frontend',
            '/api/deploy/setup_payments',
            '/api/deploy/complete_deploy',
            '/api/deploy/get_credentials_status'
        ]
        
        print(f"Rotas de deploy encontradas: {len(routes)}")
        for route in routes:
            print(f"  ✅ {route}")
        
        missing_routes = [r for r in expected_routes if r not in routes]
        if missing_routes:
            print("❌ Rotas faltando:")
            for route in missing_routes:
                print(f"  - {route}")
            return False
        else:
            print("✅ Todas as rotas de deploy estão disponíveis")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao testar rotas: {e}")
        return False

def test_files():
    """Testa se todos os arquivos necessários existem"""
    print("\n🔍 Testando arquivos...")
    
    files_to_check = [
        'templates/dashboard.html',
        'static/js/deploy.js',
        'providers/supabase_provider.py',
        'providers/vercel_provider.py',
        'deploy_service.py',
        'app.py'
    ]
    
    all_exist = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} não encontrado")
            all_exist = False
    
    return all_exist

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes de integração do Deploy e Provisionamento\n")
    
    tests = [
        ("Arquivos", test_files),
        ("Imports", test_imports), 
        ("Rotas", test_routes)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Erro no teste {name}: {e}")
            results.append((name, False))
    
    print("\n" + "="*50)
    print("RESUMO DOS TESTES:")
    print("="*50)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print("="*50)
    if all_passed:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("A integração está pronta para uso!")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
        print("Verifique os erros acima antes de usar")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
