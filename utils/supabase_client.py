"""
Módulo para inicializar e fornecer um cliente Supabase singleton.
"""

import os
import httpx # Adicionar esta importação
from supabase import create_client, Client

# Pega as credenciais do Supabase do ambiente
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_KEY")

# Cria o cliente Supabase
# A verificação de url e key é feita aqui para falhar rapidamente se não estiverem configuradas
if not url or not key:
    print("[ERRO CRÍTICO] As variáveis de ambiente SUPABASE_URL e SUPABASE_SERVICE_KEY são obrigatórias.")
    # Em um ambiente de produção, você pode querer lançar uma exceção aqui
    # raise EnvironmentError("Supabase URL and Key must be set.")
    supabase: Client = None
else:
    try:
        # Configurar o cliente HTTP com timeouts
        http_client = httpx.Client(timeout=10.0) # Define um timeout de 10 segundos para todas as requisições
        
        supabase: Client = create_client(
            url,
            key,
            http_client=http_client # Passa o cliente HTTP configurado
        )
        print("[INFO] Cliente Supabase inicializado com sucesso.")
    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha ao inicializar o cliente Supabase: {e}")
        supabase: Client = None
