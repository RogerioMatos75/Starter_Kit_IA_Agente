# Customizando o Fluxo de Trabalho com `workflow.json`

O arquivo `workflow.json` é o coração da orquestração no Archon AI. Ele funciona como um "blueprint" ou uma "receita", definindo a sequência exata de etapas (estados) que a IA deve seguir para construir o projeto. Ao editar este arquivo, você pode criar fluxos de trabalho completamente novos e personalizados para qualquer tipo de projeto.

## Estrutura do Arquivo

O arquivo tem uma estrutura simples: um objeto JSON principal com duas chaves:

-   `nome_workflow`: Uma string que dá um nome descritivo ao fluxo de trabalho.
-   `estados`: Um array (lista) de objetos, onde cada objeto representa uma etapa a ser executada.

```json
{
    "nome_workflow": "Desenvolvimento Web Full-Stack Padrão",
    "estados": [
        // ... lista de objetos de estado aqui ...
    ]
}
```

## Anatomia de uma Etapa (Estado)

Cada objeto dentro do array `estados` define uma tarefa específica. Ele é composto pelas seguintes chaves:

| Chave             | Tipo   | Obrigatório | Descrição                                                                                                                              |
| ----------------- | ------ | ----------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `nome`            | string | Sim         | O nome da etapa que aparece na linha do tempo do painel. Ex: "Backend: API de Autenticação".                                           |
| `artefato_gerado` | string | Sim         | O nome do arquivo que será criado na pasta do projeto (`projetos/<nome_do_projeto>/`) quando esta etapa for aprovada. Ex: `api_autenticacao.py`. |
| `descricao`       | string | Sim         | A instrução principal para a IA. Esta é a parte mais importante do prompt, dizendo à IA o que fazer.                                   |
| `tipo`            | string | Não         | Uma categoria para a tarefa (ex: `documentacao`, `backend`, `frontend`). Útil para organização e lógica futura.                         |
| `guia`            | string | Não         | O caminho para um arquivo de contexto (geralmente um `.md` de uma etapa anterior) dentro da pasta do projeto (`projetos/<nome_do_projeto>/...`). O conteúdo deste arquivo será usado como contexto adicional no prompt da IA.         |
| `tecnologia`      | string | Não         | Especifica a tecnologia a ser usada (ex: "Python/Flask", "React/Next.js"). Adiciona mais contexto técnico ao prompt.                  |

### Exemplo Detalhado

Vamos analisar uma etapa do `workflow.json` padrão:

```json
{
    "nome": "Backend: API de Autenticação",
    "tipo": "backend",
    "artefato_gerado": "api_autenticacao.py",
    "tecnologia": "Python/Flask",
    "descricao": "Implementa o endpoint de login e registro de usuários."
}
```

Quando o orquestrador executa esta etapa:
1.  **Nome:** A linha do tempo mostrará "Backend: API de Autenticação" como a etapa atual.
2.  **Prompt:** Um prompt será gerado para a IA contendo:
    *   A **descrição**: "Implementa o endpoint de login e registro de usuários."
    *   A **tecnologia**: "Tecnologia Específica: Python/Flask".
3.  **Execução:** A IA gerará o código Python para uma API Flask com os endpoints de login e registro.
4.  **Aprovação:** Quando o supervisor aprovar o resultado, o código gerado será salvo no arquivo `projetos/<nome_do_projeto>/api_autenticacao.py`.
5.  **Geração do `Gemini.md`:** Um arquivo `Gemini.md` será criado ou atualizado na pasta do projeto (`projetos/<nome_do_projeto>/`). Este arquivo conterá instruções para o agente CLI (como o Gemini CLI) sobre como prosseguir com o artefato gerado, incluindo qual arquivo analisar e quais ações tomar (ex: criar diretórios, instalar dependências, rodar o servidor).

## Como Criar seu Próprio Workflow

Modificar o fluxo de trabalho é simples e poderoso.

### 1. Adicionar uma Nova Etapa
Basta adicionar um novo objeto JSON ao array `estados` na posição desejada.

**Exemplo:** Adicionar uma etapa para criar testes unitários para a API de autenticação.

```json
{
    "nome": "Testes: API de Autenticação",
    "tipo": "teste",
    "artefato_gerado": "test_api_autenticacao.py",
    "tecnologia": "Python/Pytest",
    "guia": "projetos/{project_name}/base_conhecimento/01_base_conhecimento.md",
    "descricao": "Crie testes unitários usando Pytest para validar os endpoints de login e registro da API de autenticação. Use o artefato 'api_autenticacao.py' como referência e verifique casos de sucesso e de falha, como e-mail duplicado e senha incorreta."
}
```

### 2. Reordenar Etapas
A ordem de execução é definida pela ordem dos objetos no array. Para mudar a ordem, simplesmente mova os blocos de objetos JSON para cima ou para baixo na lista.

### 3. Remover uma Etapa
Para remover uma etapa, simplesmente delete seu objeto correspondente do array `estados`.

## Dicas e Boas Práticas

*   **Seja Específico:** Quanto mais clara e detalhada for a `descricao`, melhor será o resultado da IA.
*   **Divida para Conquistar:** Em vez de uma etapa gigante como "Criar todo o backend", divida-a em etapas menores e mais gerenciáveis: "API de Autenticação", "API de Produtos", "API de Pedidos". Isso facilita a supervisão e a correção.
*   **Use o `guia`:** Para tarefas que dependem de decisões anteriores, certifique-se de que essas decisões estejam documentadas em um dos artefatos gerados na pasta `projetos/` e aponte a chave `guia` para ele, usando o placeholder `{project_name}` que será substituído dinamicamente.
*   **Valide seu JSON:** Após editar, use um validador de JSON online para garantir que a sintaxe do arquivo está correta e evitar erros de carregamento.
```

### 2. Reordenar Etapas
A ordem de execução é definida pela ordem dos objetos no array. Para mudar a ordem, simplesmente mova os blocos de objetos JSON para cima ou para baixo na lista.

### 3. Remover uma Etapa
Para remover uma etapa, simplesmente delete seu objeto correspondente do array `estados`.

## Dicas e Boas Práticas

*   **Seja Específico:** Quanto mais clara e detalhada for a `descricao`, melhor será o resultado da IA.
*   **Divida para Conquistar:** Em vez de uma etapa gigante como "Criar todo o backend", divida-a em etapas menores e mais gerenciáveis: "API de Autenticação", "API de Produtos", "API de Pedidos". Isso facilita a supervisão e a correção.
*   **Use o `guia`:** Para tarefas que dependem de decisões anteriores, certifique-se de que essas decisões estejam documentadas em um dos arquivos da pasta `output/` e aponte a chave `guia` para ele.
*   **Valide seu JSON:** Após editar, use um validador de JSON online para garantir que a sintaxe do arquivo está correta e evitar erros de carregamento.