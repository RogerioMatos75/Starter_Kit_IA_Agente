# Contribuindo para o Archon AI

Ficamos felizes com o seu interesse em contribuir para o Archon AI! Toda contribuição, desde a correção de um simples erro de digitação até a implementação de uma nova funcionalidade, é muito bem-vinda.

Este documento fornece diretrizes para garantir que o processo de contribuição seja o mais suave e eficaz possível para todos.

## Como Contribuir

Existem várias maneiras de contribuir com o projeto:

*   **Reportando Bugs:** Se você encontrar um comportamento inesperado ou um erro.
*   **Sugerindo Melhorias:** Se você tem uma ideia para uma nova funcionalidade ou uma melhoria em uma existente.
*   **Escrevendo Código:** Corrigindo um bug ou implementando uma nova funcionalidade.
*   **Melhorando a Documentação:** Se você encontrar algo que não está claro ou que poderia ser melhor explicado.

## Reportando Bugs

Bons relatórios de bugs são extremamente úteis. Antes de criar um novo relatório, por favor, verifique a [lista de issues](https://github.com/seu-usuario/seu-repositorio/issues) para ver se o problema já foi reportado.

Ao criar um novo relatório de bug, por favor, inclua o máximo de detalhes possível:

1.  **Use um título claro e descritivo.**
2.  **Descreva o problema:** Explique o que aconteceu e o que você esperava que acontecesse.
3.  **Passos para reproduzir:** Forneça um passo a passo detalhado de como reproduzir o bug.
4.  **Ambiente:** Inclua detalhes sobre o seu ambiente, como sistema operacional, versão do Python e do Node.js.
5.  **Logs ou Screenshots:** Se aplicável, adicione logs de erro do console ou screenshots que demonstrem o problema.

## Sugerindo Melhorias e Novas Funcionalidades

Adoramos receber novas ideias! Para sugerir uma melhoria ou uma nova funcionalidade, crie uma [nova issue](https://github.com/seu-usuario/seu-repositorio/issues).

Por favor, inclua:

1.  **Um título claro e descritivo.**
2.  **Descrição do problema:** Explique o problema que sua sugestão resolve. Por que essa melhoria é necessária?
3.  **Solução proposta:** Descreva em detalhes como a funcionalidade deveria funcionar.
4.  **Alternativas consideradas:** Se você pensou em outras abordagens, mencione-as e explique por que a sua proposta é a melhor.

## Contribuindo com Código (Pull Requests)

Se você deseja corrigir um bug ou implementar uma nova funcionalidade, o processo é o seguinte:

1.  **Fork o Repositório:** Crie um fork do projeto para a sua conta do GitHub.

2.  **Clone o seu Fork:**
    ```bash
    git clone https://github.com/seu-usuario/starter_kit_ia_agente.git
    cd starter_kit_ia_agente
    ```

3.  **Crie uma Nova Branch:** Crie uma branch descritiva para suas alterações.
    ```bash
    # Para uma nova funcionalidade:
    git checkout -b feature/nome-da-funcionalidade

    # Para uma correção de bug:
    git checkout -b fix/descricao-do-bug
    ```

4.  **Faça suas Alterações:** Implemente o código, seguindo as convenções de estilo do projeto.

5.  **Execute os Testes:** Antes de enviar, certifique-se de que todos os testes estão passando.
    ```bash
    pytest
    ```

6.  **Faça o Commit das suas Alterações:** Use mensagens de commit claras e descritivas.
    ```bash
    git commit -m "feat: Adiciona funcionalidade X que faz Y"
    ```

7.  **Envie para o seu Fork:**
    ```bash
    git push origin feature/nome-da-funcionalidade
    ```

8.  **Abra um Pull Request (PR):** Vá para o repositório original no GitHub e abra um Pull Request da sua branch para a branch `main` do projeto principal.

    *   No PR, forneça uma descrição clara das alterações, vincule a issue relacionada (se houver) e explique o "porquê" e o "como" das suas mudanças.

Agradecemos antecipadamente por sua contribuição!