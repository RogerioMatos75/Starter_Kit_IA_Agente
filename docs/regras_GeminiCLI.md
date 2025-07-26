---------------------------------------------------------------------------------

# COMO ME UTILIZAR (INSTRUÇÕES PARA O USUÁRIO)
Para garantir que você, como usuário, utilize o Gemini CLI de forma a carregar estas regras e a persona corretamente, siga as instruções abaixo dependendo do seu ambiente de terminal:

## Para PowerShell (Windows):
Para iniciar o Gemini CLI com esta persona e regras, use o seguinte comando no seu terminal PowerShell:
```powershell
gemini --ide-mode Get-Content GEMINI.md
```
## Para Terminais Unix/Linux/WSL (Bash, Zsh, etc.):
Para iniciar o Gemini CLI com esta persona e regras, use o seguinte comando no seu terminal:
```bash
cat GEMINI.md | gemini --ide-mode
```
## Para Terminais Windows (CMD):
Para iniciar o Gemini CLI com esta persona e regras, use o seguinte comando no seu terminal CMD:
```cmd
type GEMINI.md | gemini --ide-mode
```
(internamente, eu usaria a ferramenta `save_memory`)

-----------------------------------------------------------------------------------