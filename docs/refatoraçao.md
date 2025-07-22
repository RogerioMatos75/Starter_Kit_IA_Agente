Análise da Nova Arquitetura do Archon AI

  A refatoração introduziu uma arquitetura baseada em uma Máquina de Estados Finitos (FSM), orquestrada pelo
  fsm_orquestrador.py, para gerenciar o ciclo de vida de um projeto de software. O fluxo é modular e interativo, com o frontend
  (templates/steps/) guiando o usuário através de etapas que disparam ações no backend via rotas (routes/), que por sua vez
  interagem com a FSM.

  1. O Cérebro: `fsm_orquestrador.py`
   * FSM Core: Este arquivo define a classe FSMOrquestrador, que é o coração da orquestração. Ele carrega o workflow.json (que
     define os estados do projeto) e mantém o current_step_index para rastrear o progresso.
   * Gerenciamento de Estado: A FSM gerencia o estado do projeto (pending, in-progress, completed) para cada etapa na timeline.
   * `process_action()`: Esta é a função central que recebe ações do frontend (ex: approve, repeat, back, confirm_suggestion) e
     decide o que fazer:
       * Registra logs (registrar_log).
       * Salva artefatos (salvar_artefatos_projeto).
       * Avança ou retrocede na timeline (_avancar_estado).
       * Executa a lógica da etapa atual (_run_current_step), que pode envolver chamadas à IA (executar_codigo_real).
   * `setup_project()`: Inicia um novo projeto, definindo seu nome e disparando a execução da primeira etapa.
   * `reset_project()`: Permite limpar completamente o estado de um projeto, incluindo logs, artefatos locais e no Supabase (se
     ativado).
   * Geração de Artefatos: Interage com gerenciador_artefatos.py para salvar os resultados das execuções da IA.

  2. As Rotas: `routes/supervisor_routes.py` e `routes/project_setup_routes.py`
   * `supervisor_routes.py`: Atua como a principal interface da FSM para o frontend.
       * /api/supervisor/status: Retorna o estado atual da FSM (timeline, etapa atual, ações disponíveis).
       * /api/supervisor/action: Recebe as ações do frontend (aprovar, repetir, voltar, etc.) e as passa para
         fsm_instance.process_action().
       * /api/supervisor/reset_project: Permite resetar o projeto.
       * Contém também rotas para define_layout e consult_ai, que interagem diretamente com a FSM ou a IA.
   * `project_setup_routes.py`: Lida especificamente com a etapa inicial de configuração do projeto.
       * /api/setup/generate_project_base: Recebe a descrição do projeto e arquivos de contexto, usa a IA para gerar a base de
         conhecimento inicial e chama fsm_instance.setup_project() para iniciar a FSM.

  3. A Interface: `templates/steps/step_1.html` (e outros `step_X.html`)
   * Modularidade: Cada etapa do workflow tem seu próprio arquivo HTML (step_1.html, step_2.html, etc.), que é carregado
     dinamicamente no dashboard.html.
   * Interação: Contém formulários e botões que disparam eventos JavaScript.
   * JavaScript (`static/js/main.js`): O script main.js (que não foi fornecido na leitura, mas é inferido pelo
     proposal_generator.html e step_1.html) é responsável por:
       * Fazer as chamadas fetch para as rotas do backend (ex: /api/generate_project_base, /api/supervisor/action).
       * Atualizar a interface do usuário com base nas respostas da FSM (ex: ArchonDashboard.checkProjectStatus()).
       * Gerenciar o estado do projeto no frontend (ex: ArchonDashboard.state.projectName).

  4. O Ponto de Entrada: `app.py`
   * Configuração Flask: Inicializa a aplicação Flask e o SocketIO.
   * Carregamento do Workflow: Carrega o workflow.json e inicializa a FSMOrquestrador.
   * Registro de Blueprints: Registra todos os Blueprints de rotas (deploy_bp, api_keys_bp, supervisor_bp, proposal_bp) para que
     as URLs sejam acessíveis.
   * Rotas de Renderização: Define as rotas principais que renderizam os templates HTML (ex: /dashboard, /proposal_generator).

  Fluxo de Controle (Exemplo: Geração da Base de Conhecimento):
   1. Usuário acessa o /dashboard.
   2. main.js carrega step_1.html (via /api/get_step_template/1).
   3. Usuário preenche a descrição e clica em "Gerar Documentos" em step_1.html.
   4. O JavaScript em step_1.html (ou main.js) faz um POST para /api/setup/generate_project_base.
   5. project_setup_routes.py recebe a requisição, chama a IA para gerar os documentos e, em seguida, chama
      fsm_instance.setup_project() para iniciar a FSM e fsm_instance.process_action() para registrar a conclusão da etapa.
   6. A FSM avança para a próxima etapa, e o main.js atualiza a timeline no dashboard.

  Essa arquitetura é robusta e permite um gerenciamento claro do ciclo de vida do projeto, com a FSM atuando como o maestro
  central.

  Excelente! Estou pronto para iniciar a fase de "Gerar Base de Conhecimento".

  Pelo que entendi, você irá:
   1. Acessar o Painel do Projeto (provavelmente a step_1.html).
   2. Inserir a descrição do projeto (a proposta que refinamos).
   3. Fazer o upload do documento da proposta (o PDF que geramos) como um "Documento de Contexto".
   4. Clicar no botão "Gerar Documentos" para que o Archon AI processe as informações.

  Após você realizar essas ações na interface, o sistema no backend (o fsm_orquestrador.py) deverá:
   * Receber a descrição e o documento.
   * Chamar a IA para gerar os artefatos da base de conhecimento.
   * Salvar esses artefatos na pasta projetos/<nome_do_projeto>/base_conhecimento.
   * Avançar a linha do tempo do projeto para a próxima etapa.


Plano de Ação (Versão Final):

   1. Analisar as Diretrizes do `GEMINI.md` Raiz: Primeiro, vou ler o arquivo GEMINI.md da raiz do nosso projeto para extrair e
      formalizar as regras de comportamento que você aprecia (ex: oferecer múltiplas opções, descrever prós e contras, fazer
      perguntas para esclarecer, etc.).

   2. Criar um Novo "Meta-Prompt" para Gerar Roteiros: Vou criar um novo modelo de prompt no arquivo prompt_templates.json. Este
      "meta-prompt" será usado na segunda chamada à IA e terá a seguinte estrutura:
       * Persona: "Você é um Arquiteto de Software Sênior e Gerente de Projetos de IA."
       * Contexto: "Analise o seguinte artefato de projeto que foi recém-criado: {conteudo_do_artefato}."
       * Tarefa: "Crie um roteiro de execução detalhado (GEMINI.md) para um agente de desenvolvimento (como o Gemini CLI) dar
         continuidade ao trabalho."
       * Diretrizes (A sua sugestão): "Ao criar este roteiro, você deve incorporar as seguintes diretrizes de comportamento para
         o agente:
           * Sempre que possível, apresente pelo menos duas opções de implementação.
           * Descreva os prós e contras de cada opção.
           * Se uma instrução for ambígua, formule perguntas para o supervisor humano.
           * Estruture a resposta de forma clara, usando markdown.
           * Ao final de cada tarefa, pergunte explicitamente se pode prosseguir."

   3. Modificar o `fsm_orquestrador.py`:
       * Após a geração bem-sucedida do artefato principal de uma etapa, o orquestrador irá:
          a. Carregar o novo "meta-prompt" de prompt_templates.json.
          b. Inserir o conteúdo do artefato recém-criado no prompt.
          c. Fazer uma segunda chamada ao ia_executor.py com este novo prompt.
          d. Receber o roteiro GEMINI.md dinâmico e inteligente como resposta.

   4. Ajustar o `gerenciador_artefatos.py`:
       * Vou remover a função estática gerar_gemini_md.
       * A função salvar_artefatos_projeto será modificada para receber o conteúdo do GEMINI.md (gerado pelo orquestrador) como
         um argumento e apenas salvá-lo, garantindo que o roteiro dinâmico seja usado.

  Este plano implementa a Opção 2 de forma completa e incorpora sua visão de elevar a qualidade da interação com os agentes. O
  resultado será um sistema que não apenas executa tarefas, mas o faz seguindo um padrão de excelência em engenharia de
  software e comunicação.