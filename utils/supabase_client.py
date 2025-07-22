"""
Módulo para inicializar e fornecer um cliente Supabase singleton de forma condicional.
"""

import os
import json
from supabase import create_client, Client, ClientOptions

def _carregar_config():
    """Carrega as configurações do builder.config.json."""
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "builder.config.json"))
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"SUPABASE_ENABLED": False}

CONFIG = _carregar_config()
SUPABASE_ENABLED = CONFIG.get("SUPABASE_ENABLED", False)

supabase: Client = None

if SUPABASE_ENABLED:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        print("[AVISO] SUPABASE_ENABLED é true, mas as variáveis de ambiente SUPABASE_URL e SUPABASE_KEY não foram encontradas. O Supabase será desativado.")
    else:
        try:
            options = ClientOptions(
                postgrest_client_timeout=10.0
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
else:
    print("[INFO] Upload para Supabase desativado conforme configuração em builder.config.json.")