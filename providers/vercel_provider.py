import subprocess
import os

def deploy(api_token):
    """Executa o deploy para a Vercel usando a Vercel CLI."""
    if not api_token:
        return {"success": False, "error": "Token da API da Vercel não fornecido."}

    try:
        # Constrói o comando de deploy com o token
        command = ["vercel", "--prod", "--token", api_token]

        # Executa o comando no diretório raiz do projeto
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
            check=True
        )

        return {"success": True, "output": result.stdout}

    except FileNotFoundError:
        return {"success": False, "error": "O comando 'vercel' não foi encontrado. Certifique-se de que a Vercel CLI está instalada globalmente (npm i -g vercel)."}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": f"Ocorreu um erro durante o deploy:\n{e.stderr}"}
    except Exception as e:
        return {"success": False, "error": f"Um erro inesperado ocorreu: {str(e)}"}