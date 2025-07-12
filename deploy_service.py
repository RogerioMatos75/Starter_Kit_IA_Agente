from providers import vercel_provider, supabase_provider

PROVIDERS = {
    "vercel": vercel_provider,
    "supabase": supabase_provider,
}

def deploy_project(provider_name, api_token):
    """Orquestra o deploy chamando o provedor especificado."""
    provider = PROVIDERS.get(provider_name.lower())

    if not provider:
        return {"success": False, "error": f"Provedor de deploy '{provider_name}' não encontrado."}

    print(f"[Deploy Service] Iniciando deploy com o provedor: {provider_name}")
    result = provider.deploy(api_token)
    return result