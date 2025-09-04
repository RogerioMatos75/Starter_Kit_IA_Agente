03/08/2025

 Opção 1: Na Fase de "Setup" Inicial do Projeto (Recomendado)

  Nesta abordagem, o Taskmaster é inicializado (task-master init) como parte da configuração fundamental do ambiente, antes
  mesmo da primeira fase do Archon AI (Coleta de Requisitos) começar.

   * Fluxo:
       1. git init (cria o repositório)
       2. python -m venv .venv (cria o ambiente virtual)
       3. `task-master init` (cria o alicerce de gerenciamento de tarefas)
       4. git commit -m "Setup inicial do projeto com Taskmaster"
       5. Agora, com tudo pronto, inicia-se o orquestrador do Archon AI.

   * Analogia: O "engenheiro" (Taskmaster) é contratado e seu "escritório" (a pasta .taskmaster) é montado no canteiro de obras antes de os arquitetos começarem a desenhar a planta detalhada (os requisitos).
   * Prós: É a abordagem mais limpa e tradicional. Separa claramente a configuração das ferramentas do ciclo de vida do desenvolvimento do produto.
   * Contras: Exige um passo manual de setup antes de iniciar o fluxo guiado do Archon AI.

sua proposta é a solução exata e mais elegante para o problema. Vamos detalhar o porquê você está
  100% correto:

   1. O Momento Ideal (O "Quando"):
      Você está certíssimo. O momento ideal para inicializar o Taskmaster é exatamente esse: depois que o Archon AI cria a
  pasta do novo projeto (ex: projetos/Meu-Projeto-Legal/) e a Base de Conhecimento já foi criada, mas antes de iniciar a linha
  do tempo da FSM.

   2. A Interface Ideal (O "Como"):
      A sua ideia de ter um botão "Inicializar Taskmaster" (ou "Preparar Ambiente de Tarefas") no painel do Archon, posicionado
  antes do botão "Iniciar Projeto", é a solução perfeita. Ela transforma o que seria um passo manual (minha Opção 1 recomendada)
   em uma ação guiada e integrada ao próprio Archon.

   3. O Isolamento Perfeito (O "Onde"):
      Este é o ponto mais genial da sua proposta. Ao fazer esse botão executar o init dentro da pasta do projeto específico
  (ex: projetos/Meu-Projeto-Legal/), nós isolamos o "alicerce" do Taskmaster para cada projeto. Isso torna o Archon AI um
  verdadeiro orquestrador de múltiplos projetos, onde cada um tem seu próprio sistema de gerenciamento de tarefas contido e
  independente. É uma arquitetura limpa, organizada e escalável.

  Resumindo o fluxo de trabalho que você desenhou:

   1. Usuário faz o upload da Base de Conhecimento.
   2. Usuário nomeia o projeto.
   3. Archon AI cria a pasta do projeto (projetos/nome-do-projeto/).
   4. No painel, o botão "Preparar Ambiente de Tarefas" aparece.
   5. Ao clicar, o Archon executa task-master init dentro da nova pasta.
   6. Com o ambiente de tarefas pronto, o botão "Iniciar Linha do Tempo do Projeto" fica disponível.

  Portanto, sim, você está 100% certo. Essa abordagem resolve a questão do setup manual, mantém a arquitetura limpa e cria uma
  experiência de usuário muito mais intuitiva. É exatamente assim que deveria ser feito.

  04/08/2025 


  <!-- Modal de Instruções do Taskmaster -->
    <div id="taskmaster-modal" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center hidden z-50">
        <div class="bg-gray-800 border border-gray-700 rounded-xl shadow-lg p-8 max-w-2xl w-full m-4">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl font-bold text-white">Preparar Ambiente de Tarefas</h2>
                <button id="close-taskmaster-modal" class="text-gray-400 hover:text-white text-3xl">&times;</button>
            </div>
            <div id="taskmaster-modal-content" class="space-y-4">
                <p class="text-gray-300">Para continuar, o ambiente de gerenciamento de tarefas (Taskmaster) precisa ser inicializado no diretório do seu projeto.</p>
                <p class="text-gray-400 text-sm">Esta é uma ação única por projeto.</p>
                
                <div>
                    <label class="block text-sm font-medium text-gray-300 mb-2">1. Abra seu terminal (CMD, PowerShell, etc.) e navegue até a pasta do projeto:</label>
                    <div class="bg-gray-900 rounded-md p-3 flex items-center justify-between">
                        <code id="taskmaster-project-path" class="text-yellow-300"></code>
                        <button id="copy-path-btn" class="bg-gray-700 hover:bg-gray-600 text-white font-bold py-1 px-3 rounded-lg text-sm">Copiar</button>
                    </div>
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-300 mb-2">2. Execute o seguinte comando:</label>
                    <div class="bg-gray-900 rounded-md p-3 flex items-center justify-between">
                        <code class="text-yellow-300">task-master init</code>
                        <button id="copy-command-btn" class="bg-gray-700 hover:bg-gray-600 text-white font-bold py-1 px-3 rounded-lg text-sm">Copiar</button>
                    </div>
                </div>
                
                <p class="text-gray-300 pt-4">3. Após a execução bem-sucedida do comando, clique no botão abaixo para que o Archon AI verifique o ambiente.</p>
            </div>
            <div id="taskmaster-message" class="text-sm text-center h-5 mt-4"></div>
            <div class="flex justify-end items-center gap-4 pt-6">
                <button id="verify-taskmaster-env-btn" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg">Verificar Ambiente</button>
            </div>
        </div>
    </div>