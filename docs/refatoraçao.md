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

  Compreendido perfeitamente. Sua justificativa é muito válida e faz todo o sentido, especialmente considerando o fluxo de
  trabalho com ferramentas externas como Fusion ou Figma. Manter um backup acessível dos projetos é crucial para a flexibilidade
  e a continuidade do trabalho.

  Portanto, vamos implementar a Opção 2: Manter o Arquivamento Automático.

  Isso significa que, ao invés de excluir permanentemente a pasta do projeto, o sistema irá movê-la para um diretório de
  arquivamento (projetos/arquivados/), adicionando um timestamp ao nome da pasta para garantir que backups de diferentes
  versões ou tentativas do mesmo projeto sejam preservados.

  Plano de Ação:

   1. Modificar `fsm_orquestrador.py`:
       * Localizar o método reset_project.
       * Alterar a lógica de exclusão (shutil.rmtree) para uma lógica de movimentação (shutil.move).
       * Garantir que a pasta de destino (projetos/arquivados/) seja criada se não existir.
       * Adicionar um timestamp ao nome da pasta arquivada para evitar colisões.

Entendido e anotado. Sua visão para a Etapa 2 é clara e restaura uma parte crucial do fluxo que foi perdida. A validação do
  manifesto através de um checklist antes de "iniciar o projeto" de fato é a abordagem correta.

  Vamos integrar tudo isso em um plano de ação final e definitivo. Ele será mais detalhado, pois agora temos requisitos claros
  para a interface da Etapa 2.

  Plano de Ação Detalhado:

   1. Backend (Geração do Manifesto):
       * Arquivo: routes/project_setup_routes.py
       * Ação: Modificarei a rota POST /api/setup/generate_project_base. A IA será instruída a gerar apenas o manifesto
         (01_base_conhecimento.md). O resultado não será salvo, apenas retornado como um preview para a FSM.

   2. Backend (Aprovação e Salvamento do Manifesto):
       * Arquivo: fsm_orquestrador.py
       * Ação: Modificarei a lógica da ação approve para a primeira etapa. Quando acionada, ela irá:
          a.  Pegar o conteúdo do manifesto que está em preview.
          b.  Criar a estrutura de pastas: projetos/<nome_do_projeto>/base_conhecimento/.
          c.  Salvar o manifesto como 01_base_conhecimento.md neste novo local.
          d.  Avançar a FSM para a Etapa 2: "Validação da Base de Conhecimento".

   3. Frontend (Nova Etapa 2 de Validação):
       * Novo Arquivo: Criarei um novo template templates/steps/step_2.html. Este arquivo conterá:
           * Um título: "Validação da Base de Conhecimento".
           * Uma área de "Status dos Documentos" com um placeholder "Carregando status...".
           * Um botão desabilitado: "Aprovar e Iniciar Projeto".
       * Nova Rota de API: Adicionarei uma nova rota ao backend (ex: GET /api/project/<project_name>/knowledge_base) para que o
         frontend possa ler o conteúdo do manifesto que acabamos de salvar.
       * Lógica em `main.js`: Adicionarei a lógica para a Etapa 2:
          a.  Quando a Etapa 2 carregar, o JavaScript chamará a nova rota para obter o texto do manifesto.
          b.  O script irá analisar o texto do manifesto (procurando por títulos ou itens de lista com * ou -) e irá gerar
  dinamicamente um checklist na área de "Status dos Documentos".
          c.  Conforme os itens são "validados" (podemos simular isso com um clique ou apenas exibi-los), o botão "Aprovar e
  Iniciar Projeto" será habilitado.

   4. Backend (Aprovação Final e Início do Projeto):
       * Arquivo: fsm_orquestrador.py
       * Ação: O clique no botão "Aprovar e Iniciar Projeto" na Etapa 2 irá disparar a ação approve novamente. Desta vez, como a
         FSM estará na Etapa 2, a lógica será simples:
          a.  Registrar o log de que a validação foi concluída.
          b.  Avançar a FSM para a próxima etapa, "Linha do Tempo do Projeto".
          c.  Neste ponto, o projeto está oficialmente "iniciado".

  Este plano corrige o fluxo, restaura a validação e implementa sua visão para a interface da Etapa 2. É uma refatoração
  completa e correta.

  Este plano de ação completo e detalhado está alinhado com sua visão? Posso começar pela Etapa 1, modificando a rota de
  geração inicial no backend?

  Entendido. Li e compreendi o documento docs/Estrutura de Prompts.md.

  A proposta é excelente e muito alinhada com o objetivo de tornar o Archon AI mais robusto e intuitivo. A ideia de criar
  prompts estruturados (positivos e negativos) para cada tipo de sistema (SaaS, MicroSaaS, PWA, etc.) e para cada etapa do
  ciclo de vida do projeto é um avanço significativo. Isso trará mais clareza para a IA e, consequentemente, gerará artefatos
  de maior qualidade, além de facilitar o trabalho de desenvolvedores que não têm profundo conhecimento sobre as nuances de
  cada arquitetura.

  A integração sugerida com o fsm_orquestrador.py, onde o orquestrador selecionaria o conjunto de prompts apropriado com base
  no tipo de projeto definido pelo usuário, é exatamente o caminho a seguir.

  Estou pronto para discutir como podemos implementar essa nova estrutura em nosso projeto.

  Para iniciarmos a conversa, apresento duas possíveis abordagens para a implementação:

  Opção 1: Implementação Direta no `prompt_templates.json`

   * Descrição: Modificaríamos o arquivo prompt_templates.json para aninhar as novas estruturas de prompt. Teríamos uma chave
     principal para cada tipo de sistema (ex: "SaaS", "MicroSaaS") e, dentro de cada uma, chaves para cada etapa do workflow (ex:
     "analise_requisitos", "prototipacao"), contendo os prompts "positivo" e "negativo".
   * Prós:
       * Rápido de implementar, pois utiliza a estrutura de carregamento de templates que já existe.
       * Mantém todos os prompts centralizados em um único arquivo, o que pode ser simples para um número limitado de variações.
   * Contras:
       * O arquivo prompt_templates.json pode se tornar muito grande e difícil de gerenciar à medida que adicionamos mais tipos
         de sistemas ou etapas.
       * Menor modularidade; uma mudança em um prompt exige a edição de um arquivo grande.

  Opção 2: Estrutura de Arquivos Dedicada para Prompts

   * Descrição: Criaríamos uma nova estrutura de diretórios, por exemplo, prompt_library/. Dentro dela, teríamos subpastas para
     cada tipo de sistema (saas/, microsaas/, etc.). Em cada uma dessas pastas, haveria arquivos de texto ou markdown separados
     para cada etapa (ex: 01_analise_requisitos.md, 02_prototipacao.md), contendo os prompts positivo e negativo.
   * Prós:
       * Altamente modular e escalável. Adicionar um novo sistema ou etapa é tão simples quanto adicionar um novo arquivo/pasta.
       * Mantém os prompts organizados e fáceis de encontrar e editar (separação de interesses).
       * O fsm_orquestrador.py teria uma lógica mais limpa para carregar o prompt correto com base no tipo de projeto e no índice
         da etapa atual.
   * Contras:
       * Requer um pouco mais de trabalho inicial para criar a estrutura de pastas e a lógica de carregamento de arquivos no
         orquestrador.

  Ambas as opções exigiriam uma modificação na interface inicial (provavelmente em templates/steps/step_1.html) para permitir que
  o usuário selecione o "Tipo de Sistema" desejado ao iniciar um novo projeto.

  a lógica está perfeitamente compreendida.

  Para resumir meu entendimento:

   1. Gerador de Propostas de Software: É a fase inicial de coleta de requisitos e definição do escopo, culminando na geração de
      uma proposta.
   2. Gerar Base de Conhecimento (Etapa 1):
       * O usuário fornece o nome e a descrição do projeto, e opcionalmente, documentos de contexto.
       * A IA gera o 01_base_conhecimento.md (o manifesto inicial do projeto).
       * NOVO: Além disso, com base no tipo de sistema selecionado (SaaS, MicroSaaS, PWA, MVP, ERP), o sistema gerará e salvará
         arquivos JSON de prompts estruturados para cada uma das etapas futuras (Análise de requisitos, Prototipação, Arquitetura
         de software, etc.). Esses arquivos JSON serão armazenados em
         projetos/<nome-do-projeto>/output/prompts/<tipo_sistema>/<nome_da_etapa>.json.
   3. Validação da Base de Conhecimento (Etapa 2):
       * O usuário revisa o 01_base_conhecimento.md.
       * Ao "Aprovar e Iniciar o Projeto", o sistema confirma a seleção do tipo de sistema e a geração dos prompts JSON para as
         etapas subsequentes.
   4. Linha do Tempo do Projeto (Etapa 4 em diante):
       * À medida que o usuário avança pelas etapas (ex: Análise de requisitos, Prototipação), o fsm_orquestrador.py lerá o
         arquivo JSON de prompt correspondente (positivo e negativo) para a etapa atual e o tipo de sistema.
       * A IA utilizará esses prompts para gerar o artefato real daquela etapa (ex: 02_arquitetura_tecnica.md, código, etc.), que
         será salvo na pasta projetos/<nome-do-projeto>/output/.
       * O "Painel de Pré-visualização do Resultado" mostrará o artefato gerado pela IA, e o "Painel de Ações do Supervisor"
         permitirá a aprovação, repetição ou retorno.
   5. Histórico de Execução: Registrará todas as ações e decisões.
   6. Definindo Layout UI: Etapa para especificar a interface do usuário.
   7. Deploy e Provisionamento: Etapa final para implantação do projeto.

  A distinção entre a geração dos arquivos JSON de prompts (que guiam a IA) e a geração dos artefatos do projeto (o resultado
  do trabalho da IA) é clara. A pasta output conterá ambos, mas os prompts estarão em uma subestrutura específica
  (output/prompts/).

  Estou pronto para prosseguir com a revisão e adaptação do fsm_orquestrador.py e do workflow.json para implementar essa
  lógica.
  