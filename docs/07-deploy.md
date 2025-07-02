# Deploy em Produção (Render) e Configuração do Stripe

Este guia detalha o processo para levar sua aplicação Archon AI do ambiente de desenvolvimento local para um ambiente de produção online, acessível publicamente e pronto para processar pagamentos reais.

Utilizaremos a plataforma **Render** para a hospedagem e o **Stripe** em modo "Live" para os pagamentos.

## Parte 1: Deploy da Aplicação na Render

A **Render** é uma plataforma de nuvem (PaaS) que simplifica o processo de deploy. Nosso projeto já está preparado para ela através do arquivo `render.yaml`.

### Pré-requisitos
*   Uma conta no GitHub.
*   Uma conta na Render.
*   Seu projeto Archon AI enviado para um repositório no GitHub.

### O Poder do `render.yaml`

Este arquivo na raiz do projeto é uma declaração de "Infraestrutura como Código". Ele diz à Render exatamente como construir e rodar nossa aplicação:
*   **Serviço:** Define um serviço web.
*   **Runtime:** Especifica que usaremos Python.
*   **Comandos:** Informa como instalar as dependências (`pip install -r requirements.txt`) e como iniciar o servidor em produção (`gunicorn app:app`), que é mais robusto que o servidor de desenvolvimento do Flask.
*   **Variáveis de Ambiente:** Define que as chaves secretas virão de um grupo de variáveis que configuraremos na interface da Render.

### Passo a Passo do Deploy

1.  **Crie um "Blueprint":** No seu dashboard da Render, clique em **New +** e selecione **Blueprint**.
2.  **Conecte seu Repositório:** Conecte sua conta do GitHub à Render e selecione o repositório do seu projeto Archon AI.
3.  **Revisão e Criação:** A Render irá ler o `render.yaml` e mostrar os serviços que serão criados. Dê um nome ao seu grupo de serviços e clique em **Apply**.

A Render irá automaticamente buscar o código, instalar as dependências e iniciar o servidor. O primeiro deploy pode levar alguns minutos.

### Configurando as Variáveis de Ambiente em Produção (Render)

Suas chaves de API não devem estar no código. Vamos configurá-las de forma segura na Render.

1.  No seu dashboard da Render, vá para a seção **Environment**.
2.  Clique em **New Environment Group** para criar um grupo para suas chaves (ex: `archon-prod-keys`).
3.  Dentro do grupo, clique em **Add Environment Variable** e adicione as seguintes chaves:
    *   `GEMINI_API_KEY`: Sua chave da API do Google Gemini.
    *   `STRIPE_SECRET_KEY`: Sua chave secreta **LIVE** do Stripe (veremos a seguir).
    *   `STRIPE_WEBHOOK_SECRET`: Seu segredo do webhook **LIVE** do Stripe (veremos a seguir).
    *   `PYTHON_VERSION`: Defina como `3.11` ou a versão que você está usando.
4.  **Associe o Grupo:** Volte para o seu serviço web, vá na aba **Environment** dele e, na seção "Environment Groups", selecione o grupo que você acabou de criar.

A Render irá reiniciar a aplicação com as novas variáveis de ambiente.

## Parte 2: Deploy da Aplicação na Vercel

A **Vercel** é uma plataforma de deploy para frontends e funções serverless. Nosso projeto pode ser facilmente implantado nela devido ao `vercel.json`.

### Pré-requisitos
*   Uma conta no GitHub.
*   Uma conta na Vercel.
*   Seu projeto Archon AI enviado para um repositório no GitHub.

### O Poder do `vercel.json`

Este arquivo na raiz do projeto configura o deploy na Vercel:
*   **`builds`:** Define que `app.py` será construído usando o runtime `@vercel/python`.
*   **`routes`:** Redireciona todas as requisições para `app.py`.

### Passo a Passo do Deploy

1.  **Importar Projeto:** No seu dashboard da Vercel, clique em **Add New...** e selecione **Project**.
2.  **Importar Repositório Git:** Conecte sua conta do GitHub e importe o repositório do seu projeto Archon AI.
3.  **Configurar Projeto:** A Vercel detectará automaticamente que é um projeto Python. Você pode precisar ajustar as configurações de build se necessário, mas o `vercel.json` já deve ser suficiente.
4.  **Deploy:** Clique em **Deploy**.

A Vercel irá automaticamente buscar o código, instalar as dependências e iniciar o servidor. O primeiro deploy pode levar alguns minutos.

### Configurando as Variáveis de Ambiente em Produção (Vercel)

Na Vercel, as variáveis de ambiente são configuradas por projeto:

1.  No seu dashboard da Vercel, navegue até o seu projeto.
2.  Vá para a aba **Settings** e selecione **Environment Variables**.
3.  Adicione as seguintes chaves:
    *   `GEMINI_API_KEY`: Sua chave da API do Google Gemini.
    *   `STRIPE_SECRET_KEY`: Sua chave secreta **LIVE** do Stripe (veremos a seguir).
    *   `STRIPE_WEBHOOK_SECRET`: Seu segredo do webhook **LIVE** do Stripe (veremos a seguir).
    *   `GITHUB_REPO_URL`: A URL do seu repositório GitHub (se aplicável para o Stripe).

Após adicionar as variáveis, a Vercel fará um redeploy da sua aplicação.

## Parte 3: Configurando o Stripe para Produção (Modo Live)

Para aceitar pagamentos reais, precisamos trocar as chaves de teste do Stripe pelas de produção.

### Passo 1: Obtenha suas Chaves "Live"

1.  Acesse seu Dashboard do Stripe.
2.  No canto superior direito, **desative a opção "Modo de teste"**.
3.  Navegue até a aba **Desenvolvedores > Chaves de API**.
4.  Você verá sua "Chave publicável" e sua "Chave secreta". Copie a **Chave secreta** (ela começa com `sk_live_...`).
5.  Vá até o seu ambiente de deploy (Render ou Vercel) e cole essa chave no valor da variável `STRIPE_SECRET_KEY`.

### Passo 2: Crie o Endpoint do Webhook de Produção

O Stripe precisa saber para onde enviar as notificações de pagamento quando a aplicação está online.

1.  No seu Dashboard do Stripe (ainda em modo Live), vá para **Desenvolvedores > Webhooks**.
2.  Clique em **Adicionar um endpoint**.
3.  **URL do endpoint:** Cole a URL da sua aplicação na Render ou Vercel, seguida de `/webhook`.
    *   Exemplo Render: `https://meu-archon-app.onrender.com/webhook`
    *   Exemplo Vercel: `https://meu-archon-app.vercel.app/webhook`
4.  **Eventos:** Clique em "Selecionar eventos" e escolha `checkout.session.completed`.
5.  Clique em **Adicionar endpoint**.

### Passo 3: Obtenha o Segredo do Webhook

1.  Após criar o endpoint, a página de detalhes será exibida.
2.  Na seção **Segredo do webhook**, clique em **Revelar**.
3.  Copie o segredo (ele começa com `whsec_...`). **Este valor só é mostrado uma vez!**
4.  Vá até o seu ambiente de deploy (Render ou Vercel) e cole este segredo no valor da variável `STRIPE_WEBHOOK_SECRET`.

---

**Pronto!** Após salvar as variáveis de ambiente na sua plataforma de deploy, sua aplicação será reiniciada e estará totalmente configurada para operar em produção, aceitando pagamentos reais e executando a lógica de entrega automatizada.