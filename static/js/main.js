document.addEventListener("DOMContentLoaded", () => {
  // Mapeia os elementos do HTML para variáveis
  const timelineContainer = document.getElementById("timeline-container");
  const previewTextarea = document.getElementById("preview-textarea");
  const observationsTextarea = document.getElementById("observations-textarea");
  const projectNameInput = document.getElementById("project-name-input");
  const conceptualFilesInput = document.getElementById("conceptual-files-input");
  const fileListDisplay = document.getElementById("file-list-display");
  const startProjectBtn = document.getElementById("btn-start-project");
  const approveBtn = document.getElementById("btn-approve");
  const repeatBtn = document.getElementById("btn-repeat");
  const backBtn = document.getElementById("btn-back");
  const pauseBtn = document.getElementById("btn-pause");
  const logsTableBody = document.getElementById("logs-table-body");
  const shutdownBtn = document.getElementById("btn-shutdown");

  // Array com todos os botões de ação do supervisor para facilitar a manipulação em massa
  const supervisorActionBtns = [approveBtn, repeatBtn, backBtn, pauseBtn];

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
      } else {
        // pending
        classes += " border-b-transparent text-[#9daebe]";
        textClasses += " text-[#9daebe]";
      }

      const stepElement = document.createElement("a");
      stepElement.className = classes;
      stepElement.href = "#";
      stepElement.innerHTML = `<p class="${textClasses}">${step.name}</p>`;
      timelineContainer.appendChild(stepElement);
    });

    // Habilita/desabilita o campo de nome do projeto
    if (data.project_name) {
      projectNameInput.value = data.project_name;
      projectNameInput.disabled = true; // Trava o nome do projeto
      startProjectBtn.disabled = true; // Desabilita o botão de iniciar
      startProjectBtn.classList.add("opacity-50", "cursor-not-allowed");
      // Habilita os botões de ação do supervisor
      supervisorActionBtns.forEach(btn => {
        btn.disabled = false;
        btn.classList.remove("opacity-50", "cursor-not-allowed");
      });
    } else {
      projectNameInput.disabled = false;
      startProjectBtn.disabled = false;
      startProjectBtn.classList.remove("opacity-50", "cursor-not-allowed");
    }

    // 2. Atualiza o Painel de Preview
    previewTextarea.value = data.current_step.preview_content;

    // 3. Habilita/Desabilita o botão "Voltar"
    const isFinished = data.actions.is_finished;
    backBtn.disabled = isFinished || !data.actions.can_go_back;
    if (backBtn.disabled) {
      backBtn.classList.add("opacity-50", "cursor-not-allowed");
    } else {
      backBtn.classList.remove("opacity-50", "cursor-not-allowed");
    }

    // 4. Desabilita todos os botões de ação se o projeto estiver finalizado
    // Apenas se o projeto já foi iniciado
    if (data.project_name) {
      approveBtn.disabled = isFinished;
      repeatBtn.disabled = isFinished;
      pauseBtn.disabled = isFinished;
      supervisorActionBtns.forEach((btn) => {
        if (isFinished) btn.classList.add("opacity-50", "cursor-not-allowed");
        // else btn.classList.remove("opacity-50", "cursor-not-allowed"); // A habilitação geral já cuida disso
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
   * Envia uma ação para o backend.
   * @param {string} action - O nome da ação (approve, repeat, etc.).
   * @param {HTMLElement} clickedButton - O botão que foi clicado.
   */
  async function handleAction(action, clickedButton) {
    const projectName = projectNameInput.value; // O nome já estará travado
    const observation = observationsTextarea.value;
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
        body: JSON.stringify({ action, observation, project_name: projectName }),
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
   * Lida com o setup inicial do projeto (nome e upload de arquivos).
   */
  async function handleSetupProject() {
    const projectName = projectNameInput.value.trim();

    if (!projectName) {
      alert("Por favor, defina um nome para o projeto antes de iniciar.");
      projectNameInput.focus();
      return;
    }

    const formData = new FormData();
    formData.append('project_name', projectName);

    // Anexa os arquivos conceituais, se houver
    for (const file of conceptualFilesInput.files) {
      formData.append('files', file);
    }

    console.log(`Iniciando o projeto: "${projectName}" com ${conceptualFilesInput.files.length} arquivos.`);
    setProcessingButton(startProjectBtn);

    try {
      const response = await fetch("/api/setup_project", { method: "POST", body: formData });
      const data = await response.json();

      if (!response.ok) {
        // Se o servidor retornou um erro (como 400), 'data' conterá a mensagem de erro.
        throw new Error(data.error || `HTTP error! status: ${response.status}`);
      }

      updateUI(data);
      fetchLogs();
    } catch (error) {
      console.error("Erro ao iniciar o projeto:", error);
      alert(`Erro ao iniciar o projeto: ${error.message}`);
      clearButtonStates(); // Limpa o estado de processamento
      startProjectBtn.disabled = false; // Reabilita o botão
    }
  }

  /**
   * Pede confirmação e envia o comando para encerrar o servidor.
   */
  async function handleShutdown() {
    // O botão "Encerrar" agora funciona como "Resetar Projeto"
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
        alert("Projeto resetado com sucesso! Um novo projeto pode ser iniciado."); // Informa o usuário
      } catch (error) {
        console.error("Error resetting project:", error);
        clearButtonStates();
        alert("Erro ao resetar o projeto. Verifique o console para mais detalhes.");
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
  startProjectBtn.addEventListener("click", () => handleSetupProject());
  shutdownBtn.addEventListener("click", () => handleShutdown());

  // Adiciona um "escutador" para o input de arquivos para dar feedback visual
  conceptualFilesInput.addEventListener("change", () => {
    if (conceptualFilesInput.files.length > 0) {
      const fileNames = Array.from(conceptualFilesInput.files)
        .map(
          (file) =>
            `<span class="font-medium text-slate-300">${file.name}</span>`,
        )
        .join(", ");
      fileListDisplay.innerHTML = `<strong>Arquivos selecionados:</strong> ${fileNames}`;
    } else {
      fileListDisplay.innerHTML = ""; // Limpa a lista se nenhum arquivo for selecionado
    }
  });

  // Inicializa os estados dos botões
  clearButtonStates();

  // Carrega o estado inicial do projeto quando a página é aberta
  fetchStatus(); // Isso também chamará fetchLogs()
  // fetchLogs(); // Pode ser chamado aqui também se quiser carregar os logs independentemente do status
});
