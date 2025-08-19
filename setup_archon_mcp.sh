#!/usr/bin/env bash
# Script de integração Gemini MCP para Archon AI
# Preencha os placeholders antes de rodar 🛠️

https://mcpservers.org/ 

# Controle de Versão e Análise de Código
gemini mcp add git -- uvx mcp-server-git --repository /caminho/para/seu/repo
gemini mcp add github -- env GITHUB_PERSONAL_ACCESS_TOKEN=SEU_TOKEN_DE_ACESSO npx -y @modelcontextprotocol/server-github
gemini mcp add gitlab -- env GITLAB_PERSONAL_ACCESS_TOKEN=SEU_TOKEN_DE_ACESSO npx -y @modelcontextprotocol/server-gitlab

# Context7 MCP — documentação sempre atualizada via Context7
gemini mcp add --transport sse context7 https://context7.liam.sh/sse

# Cloud e Infraestrutura (IaaS/PaaS)
gemini mcp add firebase -- npx -y firebase-tools@latest experimental:mcp
gemini mcp add kubernetes -- env KUBECONFIG=/caminho/para/seu/kubeconfig npx -y mcp-server-kubernetes
gemini mcp add docker -- uvx docker-mcp
gemini mcp add aws-kb -- env AWS_ACCESS_KEY_ID=SEU_ACCESS_KEY AWS_SECRET_ACCESS_KEY=SEU_SECRET_KEY npx -y @modelcontextprotocol/server-aws-kb-retrieval

# Bancos de Dados e APIs
gemini mcp add postgres -- npx -y @modelcontextprotocol/server-postgres postgresql://USUARIO:SENHA@HOST:5432/SEU_BANCO
gemini mcp add redis -- npx -y @modelcontextprotocol/server-redis redis://USUARIO:SENHA@HOST:6379/0
gemini mcp add clickhouse -- npx -y clickhouse-mcp --dsn "clickhouse://USUARIO:SENHA@HOST:8443/SEU_DB"

# Monitoramento e Observabilidade
gemini mcp add sentry -- env SENTRY_AUTH_TOKEN=SUA_CHAVE_DE_API SENTRY_ORG=SEU_ORG SENTRY_PROJECT=SEU_PROJETO npx -y @sentry/mcp-server
gemini mcp add grafana -- env GRAFANA_URL=https://SEU_DOMINIO GRAFANA_API_KEY=SUA_CHAVE_DE_API npx -y @grafana/mcp-grafana
gemini mcp add datadog -- env DATADOG_API_KEY=SUA_CHAVE_DE_API DATADOG_SITE=SEU_SITE npx -y @datadog/mcp-server

# Produtividade e Documentação
gemini mcp add notion -- env NOTION_API_KEY=SUA_CHAVE_DE_API npx -y @modelcontextprotocol/server-notion
gemini mcp add confluence -- env ATLASSIAN_API_TOKEN=SEU_TOKEN_DE_ACESSO npx -y @modelcontextprotocol/server-confluence
gemini mcp add slack -- env SLACK_BOT_TOKEN=SEU_TOKEN_DE_ACESSO npx -y @modelcontextprotocol/server-slack

# Testes e Qualidade
##gemini mcp add playwright -- npx -y mcp-server-playwright
gemini mcp add playwright npx @playwright/mcp@latest
gemini mcp add jest -- npx -y mcp-server-jest
gemini mcp add cypress -- npx -y mcp-server-cypress

# Desenvolvimento Mobile e Cross-platform
gemini mcp add expo -- npx -y expo-cli@latest mcp
gemini mcp add flutter -- flutter mcp
gemini mcp add android-studio -- studio.sh mcp
gemini mcp add android-studio sse studio.sh mcp

# Compatibilidade e Testes de Ambiente
gemini mcp add browserstack -- env BROWSERSTACK_USERNAME=SEU_USUARIO BROWSERSTACK_ACCESS_KEY=SUA_CHAVE_DE_API npx -y mcp-server-browserstack
gemini mcp add saucelabs -- env SAUCE_USERNAME=SEU_USUARIO SAUCE_ACCESS_KEY=SUA_CHAVE_DE_API npx -y mcp-server-saucelabs

# Testes e Automação de Navegador
gemini mcp add playwright -- npx -y @microsoft/playwright-mcp
## Automatiza interações de navegador (cliques, formulários, testes E2E) via MCP.

# Crawling e Scraping
gemini mcp add firecrawl -- npx -y @mendableai/firecrawl-mcp
##Raspagem estruturada de sites (Markdown/JSON), ideal para dar contexto real ao LLM.

# Gemini CLI via MCP
gemini mcp add gemini -- npx -y @blesscat/gemini-cli-mcp
## Expõe comandos Gemini (chat, generate, list-models) como ferramentas MCP.

echo "Todas as integrações foram adicionadas (ou tentadas). Preencha os placeholders e execute o script com atenção."
