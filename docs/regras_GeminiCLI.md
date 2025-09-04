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
```bash
type GEMINI.md | gemini --ide-mode
```
(internamente, eu usaria a ferramenta `save_memory`)

# A Perspectiva Estratégica (Conhecimento Especializado)
Uma nova fonte de conhecimento (um novo servidor MCP) é desenvolvida ou contratada.
```bash
gemini mcp add <nome-do-servidor> <endereço-do-servidor>
```
gemini mcp

Manage MCP servers

Commands:
```bash
  gemini mcp add <name> <commandOrUrl> [args...]  Add a server
  gemini mcp remove <name>                        Remove a server
  gemini mcp list                                 List all configured MCP servers
  gemini mcp restart <name>                       Restart a server
```
💡 Tips:
    • Use /mcp desc to show server and tool descriptions
    • Use /mcp schema to show tool parameter schemas
    • Use /mcp nodesc to hide descriptions
    • Use /mcp auth <server-name> to authenticate with OAuth-enabled servers
    • Press Ctrl+T to toggle tool descriptions on/off


Options:
  -h, --help  Show help for command


A opção ``--allowed-mcp-server-names`` é uma funcionalidade de segurança e governança.
Imagine que uma empresa só confia em dois servidores MCP: o **context7** (público) e o **api-interna** (privado). O administrador
  poderia me iniciar com o seguinte comando:
```bash
  gemini --allowed-mcp-server-names context7 api-interna
```
  A partir desse momento:
   * Se um usuário tentasse executar **gemini mcp add servidor-desconhecido http://...**, a operação falharia.
   * O comando **gemini mcp add api-interna http://...** funcionaria normalmente (pois **api-interna** está na lista de permissões).

  Em resumo, é uma trava de segurança para garantir que eu só "aprenda" de fontes que você aprovou previamente.

-----------------------------------------------------------------------------------
# gemini mcp list

✗ android-studio: studio.sh mcp (stdio) - Disconnected 
✓ context7: https://context7.liam.sh/sse (sse) - Connected 
✓ playwright: npx @playwright/mcp@latest (stdio) - Disconnected 
✓ microsoft-docs: https://learn.microsoft.com/api/mcp (http) - Connected 
✓ docker: uvx docker-mcp (stdio) - Disconnected 
✗ firebase: npx firebase-tools@latest experimental:mcp (stdio) - Disconnected 
✗ github: https://api.githubcopilot.com/mcp (http) - Disconnected 


```bash
gemini mcp add --transport http microsoft-docs https://learn.microsoft.com/api/mcp
gemini mcp add --transport http figma http://127.0.0.1:3845/mcp
gemini mcp add --transport sse context7 https://context7.liam.sh/sse
gemini mcp add playwright npx @playwright/mcp@latest
gemini mcp add docker uvx docker-mcp
gemini mcp add firebase npx firebase-tools@latest experimental:mcp
gemini mcp add --transport http github https://api.githubcopilot.com/mcp