document.addEventListener("DOMContentLoaded", () => {
  // Mapeia os elementos do HTML para variáveis
  const timelineContainer = document.getElementById("timeline-container");
  const previewTextarea = document.getElementById("preview-textarea");
  const observationsTextarea = document.getElementById("observations-textarea");
  const projectNameInput = document.getElementById("project-name-input");
  // const conceptualFilesInput = document.getElementById("conceptual-files-input"); // Removido
  // const fileListDisplay = document.getElementById("file-list-display"); // Removido
  const startProjectBtn = document.getElementById("btn-start-project");
  const approveBtn = document.getElementById("btn-approve");
  const repeatBtn = document.getElementById("btn-repeat");
  const backBtn = document.getElementById("btn-back");
  const pauseBtn = document.getElementById("btn-pause");
  const logsTableBody = document.getElementById("logs-table-body");
  const confirmSuggestionBtn = document.getElementById(
    "btn-confirm-suggestion",
  );
  const consultAIBtn = document.getElementById("btn-consult-ai");
  const shutdownBtn = document.getElementById("btn-shutdown");
  const apiKeyModal = document.getElementById("api-key-modal");
  const apiKeySection = document.getElementById("api-key-section");
  const newApiKeyInput = document.getElementById("new-api-key-input");
  const apiProviderSelect = document.getElementById("api-provider-select");
  const customProviderName = document.getElementById("custom-provider-name");
  const customProviderInput = document.getElementById("custom-provider-input");
  const saveApiKeyBtn = document.getElementById("btn-save-api-key");
  const testApiKeyBtn = document.getElementById("btn-test-api-key");
  const toggleApiBtn = document.getElementById("btn-toggle-api-section");
  const closeApiBtn = document.getElementById("btn-close-api-section");
  const apiKeysOutput = document.getElementById("api-keys-output");
  const apiKeysList = document.getElementById("api-keys-list");
  const toggleVisibilityBtn = document.getElementById(
    "toggle-api-key-visibility",
  );

  // Elementos para a nova funcionalidade de Gerar Base de Conhecimento
  const projectDescriptionInput = document.getElementById('project-description');
  const generateButton = document.getElementById('generate-knowledge-base-btn');
  const generationMessage = document.getElementById('generation-message');

  // Novos elementos para upload de documentos
  const contextDocumentsUpload = document.getElementById('context-documents-upload');
  const uploadedFilesList = document.getElementById('uploaded-files-list');

  // Event listener para exibir os nomes dos arquivos selecionados
  if (contextDocumentsUpload) {
    contextDocumentsUpload.addEventListener('change', () => {
      uploadedFilesList.innerHTML = ''; // Limpa a lista anterior
      if (contextDocumentsUpload.files.length > 0) {
        for (const file of contextDocumentsUpload.files) {
          const listItem = document.createElement('div');
          listItem.textContent = `• ${file.name} (${(file.size / 1024).toFixed(2)} KB)`;
          uploadedFilesList.appendChild(listItem);
        }
      } else {
        uploadedFilesList.innerHTML = '';
      }
    });
  }

  // Array com todos os botões de ação do supervisor para facilitar a manipulação em massa
  const supervisorActionBtns = [startProjectBtn, approveBtn, repeatBtn, backBtn, pauseBtn];

  // Variável para rastrear a etapa atual
  let currentStep = 1; // Começa na etapa 1 (Download Templates)

  // Variável para controlar o estado da sidebar
  let sidebarCollapsed = false;

  // Declarar apenas uma vez!
  const sidebarToggleBtn = document.getElementById("sidebar-toggle");
  const sidebarExpandBtn = document.getElementById("sidebar-expand-btn");

  /**
   * Função para mostrar uma etapa específica
   */
  function showStep(stepNumber) {
    // Esconde todas as seções de conteúdo dinamicamente
    document.querySelectorAll(".content-section").forEach((section) => {
      section.classList.add("hidden");
    });

    // Mostra a seção solicitada
    const targetContent = document.getElementById(`step-${stepNumber}-content`);
    if (targetContent) targetContent.classList.remove("hidden");

    // Se for a etapa 2 (Base de Conhecimento), busca o status dos arquivos
    if (stepNumber === 2) {
      fetchKnowledgeBaseStatus();
    }

    // Atualiza a sidebar
    updateSidebarSteps(stepNumber);
    currentStep = stepNumber;
  }

  /**
   * Atualiza o estado visual da sidebar
   */
  function updateSidebarSteps(currentStep) {
    const steps = document.querySelectorAll(".sidebar-step");
    steps.forEach((step, index) => {
      const stepNumber = index + 1;
      const stepElement = step.querySelector(".step-number");
      const stepIcon = step.querySelector(".step-icon");

      // Remove todas as classes de estado
      step.classList.remove("current", "completed", "pending");
      stepElement.classList.remove("current", "completed", "pending");
      if (stepIcon)
        stepIcon.classList.remove("current", "completed", "pending");

      if (stepNumber === currentStep) {
        step.classList.add("current");
        stepElement.classList.add("current");
        if (stepIcon) stepIcon.classList.add("current");
      } else if (stepNumber < currentStep) {
        step.classList.add("completed");
        stepElement.classList.add("completed");
        if (stepIcon) stepIcon.classList.add("completed");
      } else {
        step.classList.add("pending");
        stepElement.classList.add("pending");
        if (stepIcon) stepIcon.classList.add("pending");
      }
    });

  }

  // Adiciona event listeners para os passos da sidebar
  document.querySelectorAll(".sidebar-step").forEach((step, index) => {
    step.addEventListener("click", () => {
      showStep(index + 1);
    });
  });

  // Torna a função showStep global para uso nos botões
  window.showStep = showStep;

  /**
   * Função para resetar o estado da sidebar (útil para debug)
   */
  function resetSidebar() {
    const sidebar = document.getElementById("sidebar");
    const sidebarToggleBtn = document.getElementById("sidebar-toggle");
    const sidebarExpandBtn = document.getElementById("sidebar-expand-btn");

    // Remove todas as classes de estado
    sidebar.classList.remove("sidebar-icons-only", "sidebar-collapsed");
    sidebarExpandBtn.classList.add("hidden");
    sidebarCollapsed = false;

    // Restaura o ícone para colapsar removendo a classe 'expanded'
    sidebarToggleBtn.classList.remove("expanded");

    console.log("Sidebar resetada para estado expandido");
  }

  // Torna a função global para debug
  window.resetSidebar = resetSidebar;

  /**
   * Função para toggle da sidebar (agora com modo ícones)
   */
  function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const sidebarToggleBtn = document.getElementById("sidebar-toggle");
    const sidebarExpandBtn = document.getElementById("sidebar-expand-btn");

    // Verifica o estado atual baseado nas classes CSS
    const isIconsOnly = sidebar.classList.contains("sidebar-icons-only");
    const isCollapsed = sidebar.classList.contains("sidebar-collapsed");

    if (isIconsOnly || isCollapsed) {
      // Expandir sidebar completa
      sidebar.classList.remove("sidebar-icons-only");
      sidebar.classList.remove("sidebar-collapsed");
      sidebarExpandBtn.classList.add("hidden");
      sidebarCollapsed = false;

      // Mudar ícone para colapsar (removendo a classe que mostra o ícone de expandir)
      sidebarToggleBtn.classList.remove("expanded");

      console.log("Sidebar expandida");
    } else {
      // Modo ícones apenas
      sidebar.classList.remove("sidebar-collapsed");
      sidebar.classList.add("sidebar-icons-only");
      sidebarExpandBtn.classList.add("hidden");
      sidebarCollapsed = true;
      // Mudar ícone para expandir (adicionando a classe que o mostra)
      sidebarToggleBtn.classList.add("expanded");

      // Atualizar estados dos ícones
      setTimeout(() => {
        // Chama a função principal que já lida com todos os estados
        updateSidebarSteps(currentStep);
      }, 100);

      console.log("Sidebar em modo ícones");
    }
  }

  // Event listeners para os botões de toggle
  if (sidebarToggleBtn) {
    sidebarToggleBtn.addEventListener("click", (e) => {
      e.preventDefault();
      console.log("Clique no botão toggle da sidebar");
      toggleSidebar();
    });
  }

  if (sidebarExpandBtn) {
    sidebarExpandBtn.addEventListener("click", (e) => {
      e.preventDefault();
      console.log("Clique no botão expandir da sidebar");
      toggleSidebar();
    });
  }

  /**
   * Remove o estado ativo de todos os botões do supervisor.
   */
  function clearButtonStates() {
    supervisorActionBtns.forEach((btn) => {
      btn.classList.remove("active", "processing");
    });
  }

  /**
   * Define um botão como ativo visualmente.
   * @param {HTMLElement} activeButton - O botão que deve ficar ativo.
   */
  function setActiveButton(activeButton) {
    clearButtonStates();
    activeButton.classList.add("active");
  }

  /**
   * Verifica se a chave da API está configurada e ajusta a UI.
   */
  async function checkApiKey() {
    try {
      const response = await fetch("/api/check_api_key");
      const data = await response.json();
      if (data.is_configured) {
        // Chave configurada: deixa o botão normal
        toggleApiBtn.innerHTML = `<span>Gerenciar API Keys</span>`;
        toggleApiBtn.className =
          "flex items-center gap-2 rounded-lg bg-blue-600/20 px-4 py-2 text-sm font-semibold text-blue-300 transition-colors hover:bg-blue-600/30";
      } else {
        // Chave não configurada: destaca o botão
        toggleApiBtn.innerHTML = `<span>Configurar API (Obrigatório)</span>`;
        toggleApiBtn.className =
          "flex items-center gap-2 rounded-lg bg-yellow-600/20 px-4 py-2 text-sm font-semibold text-yellow-300 transition-colors hover:bg-yellow-600/30 animate-pulse";
      }
    } catch (error) {
      console.error("Erro ao verificar a chave da API:", error);
      // Em caso de erro, assume que a chave precisa ser configurada
      toggleApiBtn.innerHTML = `<span>Erro ao verificar API</span>`;
      toggleApiBtn.className =
        "flex items-center gap-2 rounded-lg bg-red-600/20 px-4 py-2 text-sm font-semibold text-red-300";
    }
  }

  function toggleApiSection() {
    apiKeyModal.style.display =
      apiKeyModal.style.display === "none" ? "flex" : "none";
  }

  function closeApiSection() {
    apiKeyModal.style.display = "none";
  }

  /**
   * Adiciona mensagem ao output das API Keys
   */
  function addToApiOutput(message, type = "info") {
    const timestamp = new Date().toLocaleTimeString();
    const colors = {
      info: "text-blue-400",
      success: "text-green-400",
      error: "text-red-400",
      warning: "text-yellow-400",
    };

    const messageDiv = document.createElement("div");
    messageDiv.className = `${colors[type]} mb-1`;
    messageDiv.innerHTML = `[${timestamp}] ${message}`;

    apiKeysOutput.appendChild(messageDiv);
    apiKeysOutput.scrollTop = apiKeysOutput.scrollHeight;
  }

  /**
   * Atualiza a lista de API Keys configuradas
   */
  function updateApiKeysList() {
    // Esta função será chamada para carregar as chaves já configuradas
    fetch("/api/list_api_keys")
      .then((response) => response.json())
      .then((data) => {
        if (data.keys && data.keys.length > 0) {
          apiKeysList.innerHTML = "";
          data.keys.forEach((key) => {
            const keyDiv = document.createElement("div");
            keyDiv.className =
              "flex items-center justify-between p-3 bg-[#141a1f] border border-[#3d4d5c] rounded-lg";
            keyDiv.innerHTML = `
              <div class="flex items-center gap-3">
                <div class="w-2 h-2 rounded-full ${key.status === "active" ? "bg-green-400" : "bg-red-400"}"></div>
                <div>
                  <div class="text-white font-medium">${key.provider}</div>
                  <div class="text-[#9daebe] text-sm">Última verificação: ${key.lastCheck || "Nunca"}</div>
                </div>
              </div>
              <div class="flex gap-2">
                <button data-action="test" data-provider="${key.provider}" class="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition-colors">
                  Testar
                </button>
                <button data-action="remove" data-provider="${key.provider}" class="px-3 py-1 bg-red-600 hover:bg-red-700 text-white text-sm rounded transition-colors">
                  Remover
                </button>
              </div>
            `;
            apiKeysList.appendChild(keyDiv);
          });
        } else {
          apiKeysList.innerHTML = `
            <div class="text-[#9daebe] text-sm p-4 border border-dashed border-[#3d4d5c] rounded-lg text-center">
              Nenhuma API Key configurada ainda
            </div>
          `;
        }
      })
      .catch((error) => {
        console.error("Erro ao carregar API Keys:", error);
        addToApiOutput("❌ Erro ao carregar lista de API Keys", "error");
      });
  }

  /**
   * Mostra/oculta campo de provedor personalizado
   */
  function handleProviderChange() {
    if (apiProviderSelect.value === "custom") {
      customProviderName.classList.remove("hidden");
    } else {
      customProviderName.classList.add("hidden");
    }
  }

  /**
   * Toggle para mostrar/ocultar a chave da API
   */
  function toggleApiKeyVisibility() {
    const input = newApiKeyInput;
    const eyeIcon = document.getElementById("eye-icon");

    if (input.type === "password") {
      input.type = "text";
      eyeIcon.innerHTML = `
        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
        <path d="M9.5 15s2.5-2 2.5-3-2.5-3-2.5-3"/>
      `;
    } else {
      input.type = "password";
      eyeIcon.innerHTML = `
        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
        <circle cx="12" cy="12" r="3"/>
      `;
    }
  }

  /**
   * Define um botão como processando.
   * @param {HTMLElement} processingButton - O botão que está processando.
   */
  function setProcessingButton(processingButton) {
    clearButtonStates();
    processingButton.classList.add("processing");
  }

  /**
   * Busca o estado atual do projeto na API e atualiza a UI.
   */
  async function fetchStatus() {
    try {
      const response = await fetch("/api/status");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      updateUI(data);
      fetchLogs(); // Também busca os logs ao atualizar o status
    } catch (error) {
      console.error("Could not fetch project status:", error);
      previewTextarea.value =
        "Error: Could not connect to the backend. Is the Flask server running?";
    }
  }

  /**
   * Atualiza a interface do usuário com os dados recebidos da API.
   * @param {object} data - O objeto de status do projeto.
   */
  function updateUI(data) {
    // 1. Atualiza a Linha do Tempo (Timeline)
    timelineContainer.innerHTML = ""; // Limpa a timeline atual
    let completed = 0;
    data.timeline.forEach((step) => {
      let classes =
        "flex flex-col items-center justify-center border-b-[3px] pb-[13px] pt-4";
      let textClasses = "text-sm font-bold leading-normal tracking-[0.015em]";

      if (step.status === "in-progress") {
        classes += " border-b-[#dce8f3] text-white";
        textClasses += " text-white";
      } else if (step.status === "completed") {
        classes += " border-b-transparent text-[#5de4c7]"; // Verde para concluído
        textClasses += " text-[#5de4c7]";
        completed++;
      } else {
        // pending
        classes += " border-b-transparent text-[#9daebe]";
        textClasses += " text-[#9daebe]";
      }

      const stepElement = document.createElement("a");
      // Adiciona a classe para prevenir a seleção de texto, melhorando a UX
      stepElement.className = classes + " prevent-select";
      stepElement.href = "#";
      stepElement.innerHTML = `<p class="${textClasses}">${step.name}</p>`;
      timelineContainer.appendChild(stepElement);
    });

    // Atualiza a barra de progresso visual (slider)
    const progressBar = document.getElementById("progress-bar");
    const progressLabel = document.getElementById("progress-label");
    const total = data.timeline.length;
    let percent = 0;
    if (total > 0) {
      // Considera etapa atual como "em andamento" (in-progress)
      const inProgress = data.timeline.find((s) => s.status === "in-progress");
      percent = ((completed + (inProgress ? 1 : 0)) / total) * 100;
    }
    if (progressBar) progressBar.style.width = percent + "%";
    if (progressLabel) progressLabel.textContent = Math.round(percent) + "%";

    // 2. Atualiza o Painel de Preview
    if (previewTextarea) {
      previewTextarea.value = data.current_step.preview_content;
    }

    // 2.1 Atualiza o indicador de cache
    const cacheIndicator = document.getElementById("cache-indicator");
    if (cacheIndicator && data.current_step.from_cache) {
      cacheIndicator.classList.remove("hidden");
    } else if (cacheIndicator) {
      cacheIndicator.classList.add("hidden");
    }

    // Esconde o botão de confirmar sugestão por padrão
    if (confirmSuggestionBtn) {
      confirmSuggestionBtn.classList.add("hidden");
    }

    // 3. Habilita/Desabilita o botão "Voltar"
    const isFinished = data.actions.is_finished;
    if (backBtn) {
      backBtn.disabled = isFinished || !data.actions.can_go_back;
      if (backBtn.disabled) {
        backBtn.classList.add("opacity-50", "cursor-not-allowed");
      } else {
        backBtn.classList.remove("opacity-50", "cursor-not-allowed");
      }
    }

    // 4. Desabilita todos os botões de ação se o projeto estiver finalizado
    // Apenas se o projeto já foi iniciado
    if (data.project_name) {
      if (approveBtn) approveBtn.disabled = isFinished;
      if (repeatBtn) repeatBtn.disabled = isFinished;
      if (pauseBtn) pauseBtn.disabled = isFinished;
      supervisorActionBtns.forEach((btn) => {
        if (btn && isFinished)
          btn.classList.add("opacity-50", "cursor-not-allowed");
      });
    }

    // 5. Limpa os estados visuais dos botões quando o status é atualizado
    // (exceto quando é uma atualização imediata após uma ação bem-sucedida)
    if (!data.immediate_update) {
      clearButtonStates();
    }
  }

  /**
   * Busca o histórico de logs na API e atualiza a tabela de logs.
   */
  async function fetchLogs() {
    try {
      const response = await fetch("/api/logs");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const logs = await response.json();
      updateLogsUI(logs);
    } catch (error) {
      console.error("Could not fetch logs:", error);
      logsTableBody.innerHTML = `<tr><td colspan="5" class="text-center py-4 text-red-500">Erro ao carregar logs.</td></tr>`;
    }
  }

  /**
   * Busca o histórico de logs na API e atualiza a tabela de logs.
   */
  async function fetchLogs() {
    try {
      const response = await fetch("/api/logs");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const logs = await response.json();
      updateLogsUI(logs);
    } catch (error) {
      console.error("Could not fetch logs:", error);
      logsTableBody.innerHTML = `<tr><td colspan="5" class="text-center py-4 text-red-500">Erro ao carregar logs.</td></tr>`;
    }
  }

  /**
   * Busca o status de validação da base de conhecimento e atualiza a UI da Etapa 2.
   */
  async function fetchKnowledgeBaseStatus() {
    const documentStatusList = document.getElementById("document-status-list");
    const nextStep2Btn = document.getElementById("next-step-2-btn");

    if (!documentStatusList || !nextStep2Btn) return; // Garante que os elementos existem

    documentStatusList.innerHTML = '<li>Carregando status...</li>';
    nextStep2Btn.disabled = true;
    nextStep2Btn.classList.add("opacity-50", "cursor-not-allowed");

    // Mapeamento de nomes de arquivo para nomes simplificados
    const simplifiedNames = {
      "plano_base.md": "Plano Base",
      "arquitetura_tecnica.md": "Arquitetura Técnica",
      "regras_negocio.md": "Regras de Negócio",
      "fluxos_usuario.md": "Fluxos de Usuário",
      "backlog_mvp.md": "Backlog MVP",
      "autenticacao_backend.md": "Autenticação Backend",
    };

    try {
      const response = await fetch("/api/validate_knowledge_base");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      documentStatusList.innerHTML = ''; // Limpa o carregando
      data.validation_results.forEach(result => {
        const listItem = document.createElement('li');
        const icon = result.is_valid 
          ? '<svg class="w-4 h-4 text-green-500 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>'
          : '<svg class="w-4 h-4 text-red-500 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>';
        
        const displayName = simplifiedNames[result.file] || result.file; // Usa nome simplificado ou o nome original
        listItem.innerHTML = `${icon} ${displayName} ${result.is_valid ? '(Válido)' : '(Inválido)'}`;
        documentStatusList.appendChild(listItem);
      });

      if (data.all_valid) {
        nextStep2Btn.disabled = false;
        nextStep2Btn.classList.remove("opacity-50", "cursor-not-allowed");
      } else {
        // Se a validação falhar, a mensagem de erro já é exibida pelo backend
        // e o botão de próxima etapa permanece desabilitado.
        // Não é necessário exibir uma mensagem adicional aqui, pois o usuário já verá os itens inválidos.
      }

    } catch (error) {
      console.error("Erro ao buscar status da base de conhecimento:", error);
      documentStatusList.innerHTML = '<li class="text-red-500">Erro ao carregar status dos documentos.</li>';
    }
  }

  /**
   * Atualiza a tabela de logs com os dados recebidos.
   * @param {Array} logs - Array de objetos de log.
   */
  function updateLogsUI(logs) {
    logsTableBody.innerHTML = ""; // Limpa a tabela
    if (logs.length === 0) {
      logsTableBody.innerHTML = `<tr><td colspan="5" class="text-center py-4 text-[#9daebe]">Nenhum registro de log encontrado.</td></tr>`;
      return;
    }
    logs.reverse().forEach((log) => {
      // Exibe os mais recentes primeiro
      const row = `
                <tr>
                    <td class="px-4 py-2 whitespace-nowrap text-sm font-medium">${log.etapa}</td>
                    <td class="px-4 py-2 whitespace-nowrap text-sm">${log.status}</td>
                    <td class="px-4 py-2 whitespace-nowrap text-sm">${log.decisao}</td>
                    <td class="px-4 py-2 whitespace-nowrap text-sm">${new Date(log.data_hora).toLocaleString()}</td>
                    <td class="px-4 py-2 text-sm">${log.observacao || "-"}</td>
                </tr>
            `;
      logsTableBody.innerHTML += row;
    });
  }

  /**
   * Lida com a geração da base de conhecimento via IA e upload de documentos.
   */
  async function handleGenerateKnowledgeBase() {
    const description = projectDescriptionInput.value.trim();
    const project_name = projectNameInput.value.trim(); // Pega o nome do projeto

    if (!description) {
      generationMessage.textContent = 'Por favor, insira uma descrição para o projeto.';
      generationMessage.style.color = 'red';
      return;
    }

    if (!project_name) {
      generationMessage.textContent = 'Por favor, defina um nome para o projeto antes de gerar a base de conhecimento.';
      generationMessage.style.color = 'red';
      projectNameInput.focus();
      return;
    }

    generationMessage.textContent = 'Gerando base de conhecimento e enviando documentos... Isso pode levar alguns minutos.';
    generationMessage.style.color = 'yellow';
    generateButton.disabled = true; // Desabilita o botão para evitar múltiplos cliques
    generateButton.classList.add("processing");

    const formData = new FormData();
    formData.append('project_description', description);
    formData.append('project_name', project_name); // Adiciona o nome do projeto ao FormData

    // Adiciona os arquivos selecionados ao FormData
    if (contextDocumentsUpload && contextDocumentsUpload.files.length > 0) {
      for (const file of contextDocumentsUpload.files) {
        formData.append('files', file);
      }
    }

    try {
      const response = await fetch('/api/generate_project_base', {
        method: 'POST',
        // Não defina 'Content-Type' para FormData, o navegador faz isso automaticamente
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        generationMessage.textContent = data.message;
        generationMessage.style.color = 'green';
        projectDescriptionInput.value = ''; // Limpa o campo após o sucesso
        // Limpa os arquivos selecionados e a lista de exibição
        if (contextDocumentsUpload) contextDocumentsUpload.value = '';
        uploadedFilesList.innerHTML = '';
      } else {
        generationMessage.textContent = `Erro: ${data.error || 'Ocorreu um erro desconhecido.'}`;
        generationMessage.style.color = 'red';
      }
    } catch (error) {
      console.error('Erro ao gerar base de conhecimento ou enviar documentos:', error);
      generationMessage.textContent = 'Erro de conexão. Verifique o console para mais detalhes.';
      generationMessage.style.color = 'red';
    } finally {
      generateButton.disabled = false; // Reabilita o botão
      generateButton.classList.remove("processing");
    }
  }

  // Adiciona event listener para o botão de gerar base de conhecimento
  if (generateButton) {
    generateButton.addEventListener('click', handleGenerateKnowledgeBase);
  }

  /**
   * Envia uma ação para o backend.
   * @param {string} action - O nome da ação (approve, repeat, etc.).
   * @param {HTMLElement} clickedButton - O botão que foi clicado.
   */
  async function handleAction(action, clickedButton) {
    const projectName = projectNameInput.value; // O nome já estará travado
    const observation = observationsTextarea.value;
    const currentPreviewContent = previewTextarea.value; // Pega o conteúdo atual do preview
    console.log(
      `Sending action: ${action} with project: "${projectName}" and observation: "${observation}"`,
    );
    // Define o botão como processando durante a requisição
    setProcessingButton(clickedButton);

    try {
      const response = await fetch("/api/action", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          action,
          observation,
          project_name: projectName,
          current_preview_content: currentPreviewContent, // Envia o conteúdo atualizado
        }),
      });
      const data = await response.json();

      // Define o botão como ativo após a ação bem-sucedida
      setActiveButton(clickedButton);

      updateUI(data); // Atualiza a UI com o novo estado retornado pelo backend
      observationsTextarea.value = ""; // Limpa as observações
      fetchLogs(); // Atualiza os logs após uma ação
    } catch (error) {
      console.error("Error performing action:", error);
      // Remove estados visuais em caso de erro
      clearButtonStates();
    }
  }

  

  /**
   * Pede confirmação e envia o comando para encerrar o servidor.
   */
  async function handleResetProject() {
    // O botão "Resetar Projeto" apaga todo o progresso e arquivos gerados.
    if (
      confirm(
        "Tem certeza que deseja resetar o projeto? Isso apagará todo o progresso e arquivos gerados.",
      )
    ) {
      setProcessingButton(shutdownBtn);
      try {
        const response = await fetch("/api/reset_project", {
          method: "POST",
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        updateUI(data); // Atualiza a UI com o novo, resetado estado
        observationsTextarea.value = ""; // Limpa as observações
        fetchLogs(); // Atualiza os logs (que agora devem estar vazios)
        alert(
          "Projeto resetado com sucesso! Um novo projeto pode ser iniciado.",
        ); // Informa o usuário
      } catch (error) {
        console.error("Error resetting project:", error);
        clearButtonStates();
        alert(
          "Erro ao resetar o projeto. Verifique o console para mais detalhes.",
        );
      }
    }
  }

  /**
   * Lida com a consulta à IA para refinamento.
   */
  async function handleConsultAI() {
    const query = observationsTextarea.value.trim();
    const context = previewTextarea.value;

    if (!query) {
      alert(
        "Por favor, digite sua dúvida ou sugestão no campo de observações para consultar a IA.",
      );
      observationsTextarea.focus();
      return;
    }

    const consultAISpan = consultAIBtn.querySelector("span");
    const defaultText = consultAIBtn.dataset.defaultText || "Consultar IA";
    const loadingText = consultAIBtn.dataset.loadingText || "Consultando...";

    console.log(`Consultando a IA com a dúvida: "${query}"`);
    consultAIBtn.disabled = true;
    consultAIBtn.classList.add("processing");
    if (consultAISpan) consultAISpan.textContent = loadingText;

    try {
      const response = await fetch("/api/consult_ai", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, context }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || `HTTP error! status: ${response.status}`);
      }

      previewTextarea.value = data.refined_content;
      alert("Sugestão da IA carregada no painel de pré-visualização!");
      // Mostra o botão para o usuário confirmar a sugestão
      if (confirmSuggestionBtn) {
        confirmSuggestionBtn.classList.remove("hidden");
      }
      observationsTextarea.value = "";
    } catch (error) {
      console.error("Erro ao consultar a IA:", error);
      alert(`Erro ao consultar a IA: ${error.message}`);
    } finally {
      consultAIBtn.disabled = false;
      consultAIBtn.classList.remove("processing");
      if (consultAISpan) consultAISpan.textContent = defaultText;
    }
  }

  /**
   * Salva uma nova API Key.
   */
  async function handleSaveApiKey() {
    const apiKey = newApiKeyInput.value.trim();
    const provider = apiProviderSelect.value;
    const customProvider = customProviderInput.value.trim();

    if (!apiKey) {
      addToApiOutput("❌ Por favor, insira uma chave de API válida.", "error");
      newApiKeyInput.focus();
      return;
    }

    if (provider === "custom" && !customProvider) {
      addToApiOutput(
        "❌ Por favor, defina um nome para o provedor personalizado.",
        "error",
      );
      customProviderInput.focus();
      return;
    }

    const providerName = provider === "custom" ? customProvider : provider;

    addToApiOutput(`🔄 Salvando API Key para ${providerName}...`, "info");
    setProcessingButton(saveApiKeyBtn);

    try {
      const response = await fetch("/api/save_api_key", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          api_key: apiKey,
          provider: providerName,
          provider_type: provider,
        }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Erro desconhecido ao salvar a chave.");
      }

      addToApiOutput(`✅ ${data.message}`, "success");

      // Limpa o formulário
      newApiKeyInput.value = "";
      customProviderInput.value = "";
      apiProviderSelect.value = "gemini";
      customProviderName.classList.add("hidden");

      // Atualiza a lista de chaves
      updateApiKeysList();
      checkApiKey();
    } catch (error) {
      addToApiOutput(`❌ Erro: ${error.message}`, "error");
    } finally {
      clearButtonStates();
    }
  }

  /**
   * Testa uma API Key.
   * @param {boolean} isNewKey - True se estiver testando a chave do campo de input.
   */
  async function handleTestApiKey(isNewKey = true) {
    const apiKeyToTest = isNewKey ? newApiKeyInput.value.trim() : null;

    if (isNewKey && !apiKeyToTest) {
      addToApiOutput("❌ Insira uma chave no campo acima para testar.", "error");
      return;
    }

    const endpoint = isNewKey
      ? "/api/test_new_api_key"
      : "/api/test_active_api_key";
    const body = isNewKey ? { api_key: apiKeyToTest } : {};
    const testingMessage = isNewKey
      ? "🔄 Testando a NOVA chave fornecida..."
      : "🔄 Testando a chave ATIVA no servidor...";

    addToApiOutput(testingMessage, "info");
    setProcessingButton(testApiKeyBtn);

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await response.json();
      if (!response.ok) {
        // Usa a mensagem de erro do backend se disponível
        throw new Error(data.message || `Erro HTTP: ${response.status}`);
      }

      if (data.success) {
        addToApiOutput(`✅ ${data.message}`, "success");
      } else {
        // Caso de 200 OK mas success: false
        throw new Error(data.message || "A API retornou uma falha inesperada.");
      }
    } catch (error) {
      addToApiOutput(`❌ Erro no teste: ${error.message}`, "error");
    } finally {
      clearButtonStates();
    }
  }

  async function handleRemoveApiKey(provider) {
    if (confirm(`Tem certeza que deseja remover a API Key do ${provider}?`)) {
      addToApiOutput(`🗑️ Removendo ${provider}...`, "warning");
      
      try {
        const response = await fetch("/api/remove_api_key", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ provider }),
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.error || "Erro ao remover a chave.");
        }

        addToApiOutput(`✅ ${data.message}`, "success");
        updateApiKeysList();
        checkApiKey();
      } catch (error) {
        addToApiOutput(`❌ Erro ao remover: ${error.message}`, "error");
      }
    }
  }


  // Adiciona os "escutadores" de evento aos botões
  approveBtn.addEventListener("click", () =>
    handleAction("approve", approveBtn),
  );
  repeatBtn.addEventListener("click", () => handleAction("repeat", repeatBtn));
  backBtn.addEventListener("click", () => handleAction("back", backBtn));
  pauseBtn.addEventListener("click", () => handleAction("pause", pauseBtn));
  // Remove o antigo event listener do botão de iniciar projeto da etapa 3
  // startProjectBtn.addEventListener("click", () => handleSetupProject());

  // Novo fluxo: botão de iniciar projeto no painel do supervisor
  startProjectBtn.addEventListener("click", async () => {
    const projectName = projectNameInput.value.trim();
    if (!projectName) {
      alert("Por favor, defina um nome para o projeto antes de iniciar.");
      projectNameInput.focus();
      return;
    }
    // Se o projeto ainda não foi iniciado, envia ação 'start' para retomar após pausa
    const statusResp = await fetch("/api/status");
    const statusData = await statusResp.json();
    if (!statusData.project_name) {
      // Se o projeto não tem nome, significa que é o primeiro início
      // e a base de conhecimento já deve ter sido gerada na Etapa 1.
      // Agora, o setup inicial é feito com a ação 'start'
      await handleAction("start", startProjectBtn);
    } else {
      // Retomar projeto pausado
      await handleAction("start", startProjectBtn);
    }
  });
  confirmSuggestionBtn.addEventListener("click", () =>
    handleAction("confirm_suggestion", confirmSuggestionBtn),
  );
  consultAIBtn.addEventListener("click", () => handleConsultAI());
  shutdownBtn.addEventListener("click", () => handleResetProject());
  saveApiKeyBtn.addEventListener("click", handleSaveApiKey);
  testApiKeyBtn.addEventListener("click", () => handleTestApiKey(true));
  toggleApiBtn.addEventListener("click", toggleApiSection);
  closeApiBtn.addEventListener("click", closeApiSection);
  apiProviderSelect.addEventListener("change", handleProviderChange);
  toggleVisibilityBtn.addEventListener("click", toggleApiKeyVisibility);

  // Delegação de eventos para a lista de API Keys
  apiKeysList.addEventListener("click", (e) => {
    const button = e.target.closest("button");
    if (!button) return;

    const action = button.dataset.action;
    const provider = button.dataset.provider;

    if (action === "test") {
      // Ao testar uma chave salva, testamos a que está ativa no ambiente.
      handleTestApiKey(false);
    } else if (action === "remove") {
      handleRemoveApiKey(provider);
    }
  });
  // Fechar modal ao clicar fora dele
  apiKeyModal.addEventListener("click", (e) => {
    if (e.target === apiKeyModal) {
      closeApiSection();
    }
  });

  // Fechar modal com Escape
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && apiKeyModal.style.display === "flex") {
      closeApiSection();
    }
  });

  // Inicializa os estados dos botões
  clearButtonStates();

  // Garante que a sidebar inicie no estado expandido
  const sidebar = document.getElementById("sidebar");
  sidebar.classList.remove("sidebar-icons-only", "sidebar-collapsed");
  sidebarCollapsed = false;

  // Inicializa a sidebar na etapa 1 (Download Templates)
  showStep(1);

  // Carrega o estado inicial do projeto quando a página é aberta
  checkApiKey(); // Verifica a chave da API primeiro
  updateApiKeysList(); // Carrega a lista de API Keys
  fetchStatus(); // Isso também chamará fetchLogs()
  // fetchLogs(); // Pode ser chamado aqui também se quiser carregar os logs independentemente do status
});
