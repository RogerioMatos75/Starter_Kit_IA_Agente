"""
Módulo para inicializar e fornecer um cliente Supabase singleton.
"""

import os
from supabase import create_client, Client, ClientOptions

# Pega as credenciais do Supabase do ambiente
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Cria o cliente Supabase
# A verificação de url e key é feita aqui para falhar rapidamente se não estiverem configuradas
if not url or not key:
    print("[ERRO CRÍTICO] As variáveis de ambiente SUPABASE_URL e SUPABASE_KEY são obrigatórias.")
    supabase: Client = None
else:
    try:
        # Configura opções do cliente, incluindo timeout
        options = ClientOptions(
            postgrest_client_timeout=10.0  # Define um timeout de 10 segundos
        )
        
        supabase: Client = create_client(
            url,
            key,
            options=options
        )
        print("[INFO] Cliente Supabase inicializado com sucesso.")
    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha ao inicializar o cliente Supabase: {e}")
        supabase: Client = None
