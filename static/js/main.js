// static/js/main.js

const ArchonApp = {
  // ESTADO DA APLICAÇÃO
  state: {
    currentStep: 1,
    totalSteps: 7, // Ajuste este número se adicionar mais etapas
    projectName: "",
    sidebarState: "expanded", // 'expanded', 'icons-only', 'collapsed'
  },

  // CACHE DE ELEMENTOS DO DOM
  elements: {},

  // FUNÇÃO DE INICIALIZAÇÃO
  init() {
    this.cacheElements();
    this.bindEvents();
    this.ui.showStep(1); // Exibe a primeira etapa ao carregar
    this.sidebar.updateToggleButton(); // Inicializa o estado do botão
    this.api.checkApiKey();
  },

  cacheElements() {
    // Mapeia todos os elementos do DOM uma única vez
    this.elements.sidebarSteps = document.querySelectorAll(
      ".sidebar-step[data-step]",
    );
    this.elements.stepContentWrapper = document.getElementById(
      "step-content-wrapper",
    );
    this.elements.sidebar = document.getElementById("sidebar");
    this.elements.sidebarToggle = document.getElementById("sidebar-toggle");
    this.elements.sidebarExpandBtn =
      document.getElementById("sidebar-expand-btn");
    this.elements.mainContent = document.getElementById("main-content");
    
    // Elementos do Modal de API Key
    this.elements.apiKeyModal = document.getElementById("api-key-modal");
    this.elements.btnToggleApiSection = document.getElementById("btn-toggle-api-section");
    this.elements.btnCloseApiSection = document.getElementById("btn-close-api-section");
    this.elements.newApiKeyInput = document.getElementById("new-api-key-input");
    this.elements.toggleApiKeyVisibility = document.getElementById("toggle-api-key-visibility");
    this.elements.btnTestApiKey = document.getElementById("btn-test-api-key");
    this.elements.btnSaveApiKey = document.getElementById("btn-save-api-key");
    this.elements.apiProviderSelect = document.getElementById("api-provider-select");
    this.elements.apiKeysOutput = document.getElementById("api-keys-output");
  },

  bindEvents() {
    // Adiciona todos os event listeners da aplicação
    this.elements.sidebarSteps.forEach((step) => {
      step.addEventListener("click", () => {
        const stepNum = parseInt(step.dataset.step, 10);
        this.ui.showStep(stepNum);
      });
    });

    // Event listener para o botão de toggle do sidebar
    if (this.elements.sidebarToggle) {
      this.elements.sidebarToggle.addEventListener("click", (e) => {
        e.preventDefault();
        console.log(
          "Toggle clicked. Current state:",
          ArchonApp.state.sidebarState,
        );
        this.sidebar.toggle();
      });
    }

    // Event listener para o botão de expandir sidebar (quando colapsado)
    if (this.elements.sidebarExpandBtn) {
      this.elements.sidebarExpandBtn.addEventListener("click", () => {
        this.sidebar.expand();
      });
    }

    // Event listeners para o modal de API Key
    if (this.elements.btnToggleApiSection) {
        this.elements.btnToggleApiSection.addEventListener("click", () => this.apiKeyModal.show());
    }
    if (this.elements.btnCloseApiSection) {
        this.elements.btnCloseApiSection.addEventListener("click", () => this.apiKeyModal.hide());
    }
    if (this.elements.apiKeyModal) {
        this.elements.apiKeyModal.addEventListener("click", (e) => {
            // Fecha o modal se o clique for no backdrop (o próprio modal)
            if (e.target === this.elements.apiKeyModal) {
                this.apiKeyModal.hide();
            }
        });
    }

    // Event listener para o botão de visibilidade da chave
    if (this.elements.toggleApiKeyVisibility) {
      this.elements.toggleApiKeyVisibility.addEventListener("click", () => {
        const input = this.elements.newApiKeyInput;
        const icon = this.elements.toggleApiKeyVisibility.querySelector("svg");
        if (input.type === "password") {
          input.type = "text";
          icon.innerHTML = `<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07L3 3" />`;
        } else {
          input.type = "password";
          icon.innerHTML = `<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" />`;
        }
      });
    }

    // Event listeners para os botões de Testar e Salvar
    if (this.elements.btnTestApiKey) {
      this.elements.btnTestApiKey.addEventListener("click", () => this.api.testApiKey());
    }
    if (this.elements.btnSaveApiKey) {
      this.elements.btnSaveApiKey.addEventListener("click", () => this.api.saveApiKey());
    }
  },

  // OBJETO PARA O MODAL DE API KEY
  apiKeyModal: {
    show() {
      const modal = ArchonApp.elements.apiKeyModal;
      if (modal) {
        modal.style.display = "flex";
      }
    },
    hide() {
      const modal = ArchonApp.elements.apiKeyModal;
      if (modal) {
        modal.style.display = "none";
      }
    }
  },

  // OBJETO PARA COMUNICAÇÃO COM API
  api: {
    async checkApiKey() {
      console.log("Verificando status da API Key...");
      try {
        const response = await fetch("/api/keys/check");
        const data = await response.json();
        console.log("Resposta da API (/api/keys/check):", data);

        if (!data.is_configured) {
          console.log("API Key não configurada. Adicionando alerta.");
          ArchonApp.elements.btnToggleApiSection.classList.add("api-key-alert");
        } else {
          console.log("API Key configurada. Removendo alerta.");
          ArchonApp.elements.btnToggleApiSection.classList.remove("api-key-alert");
        }
      } catch (error) {
        console.error("Erro ao verificar a chave de API:", error);
        // Adiciona o alerta em caso de erro na verificação, pois pode indicar um problema
        ArchonApp.elements.btnToggleApiSection.classList.add("api-key-alert");
      }
    },

    async testApiKey() {
      const apiKey = ArchonApp.elements.newApiKeyInput.value;
      if (!apiKey) {
        ArchonApp.ui.showApiKeyStatus("Por favor, insira uma chave de API para testar.", "error");
        return;
      }
      ArchonApp.ui.showApiKeyStatus("Testando conexão...", "loading");

      try {
        const response = await fetch("/api/keys/test", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ api_key: apiKey }),
        });
        const data = await response.json();
        if (data.success) {
          ArchonApp.ui.showApiKeyStatus(data.message, "success");
        } else {
          ArchonApp.ui.showApiKeyStatus(data.message, "error");
        }
      } catch (error) {
        ArchonApp.ui.showApiKeyStatus("Erro de comunicação ao testar a chave.", "error");
      }
    },

    async saveApiKey() {
      const apiKey = ArchonApp.elements.newApiKeyInput.value;
      const provider = ArchonApp.elements.apiProviderSelect.value;

      if (!apiKey) {
        ArchonApp.ui.showApiKeyStatus("Por favor, insira uma chave de API para salvar.", "error");
        return;
      }
      ArchonApp.ui.showApiKeyStatus("Salvando chave...", "loading");

      try {
        const response = await fetch("/api/keys/save", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ api_key: apiKey, provider: provider }),
        });
        const data = await response.json();
        if (response.ok) {
          ArchonApp.ui.showApiKeyStatus(data.message, "success");
          ArchonApp.api.checkApiKey(); // Re-verifica o status para remover o alerta
        } else {
          ArchonApp.ui.showApiKeyStatus(data.error || "Ocorreu um erro", "error");
        }
      } catch (error) {
        ArchonApp.ui.showApiKeyStatus("Erro de comunicação ao salvar a chave.", "error");
      }
    },

    async performAction(
      action,
      observation = "",
      current_preview_content = "",
    ) {
      try {
        const response = await fetch("/api/supervisor/action", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            action,
            observation,
            project_name: ArchonApp.state.projectName,
            current_preview_content,
          }),
        });
        const data = await response.json();
        ArchonApp.ui.updateUI(data);
      } catch (error) {
        console.error("Erro ao executar a ação:", error);
      }
    },

    async fetchStatus() {
      try {
        const response = await fetch("/api/supervisor/status");
        const data = await response.json();
        ArchonApp.ui.updateUI(data);
      } catch (error) {
        console.error("Erro ao buscar o status:", error);
      }
    },

    // Adicione as outras funções de API aqui, como:
    // - saveApiKey
    // - testApiKey
    // - generateProjectBase
    // - etc.
  },

  // OBJETO PARA MANIPULAÇÃO DA UI
  ui: {
    showStep(stepNumber) {
      ArchonApp.state.currentStep = stepNumber;

      // Limpa o conteúdo atual
      const wrapper = ArchonApp.elements.stepContentWrapper;
      wrapper.innerHTML = "";

      // Clona e injeta o novo conteúdo
      const template = document.getElementById(`step-${stepNumber}-template`);
      if (template) {
        const clone = template.content.cloneNode(true);
        wrapper.appendChild(clone);
      }

      // Atualiza a classe ativa na sidebar
      ArchonApp.elements.sidebarSteps.forEach((step) => {
        const stepNum = parseInt(step.dataset.step, 10);
        const stepIcon = step.querySelector(".step-number");
        const stepIconEl = step.querySelector(".step-icon");

        // Remove todas as classes de estado
        step.classList.remove("current", "active", "completed", "pending");

        if (stepIcon) {
          stepIcon.classList.remove("current", "completed", "pending");
        }

        if (stepIconEl) {
          stepIconEl.classList.remove("current", "completed", "pending");
        }

        // Determina o estado baseado na posição relativa
        if (stepNum < stepNumber) {
          // Etapas anteriores = completadas
          step.classList.add("completed");
          if (stepIcon) stepIcon.classList.add("completed");
          if (stepIconEl) stepIconEl.classList.add("completed");
        } else if (stepNum === stepNumber) {
          // Etapa atual = ativa
          step.classList.add("current", "active");
          if (stepIcon) stepIcon.classList.add("current");
          if (stepIconEl) stepIconEl.classList.add("current");
        } else {
          // Etapas futuras = pendentes
          step.classList.add("pending");
          if (stepIcon) stepIcon.classList.add("pending");
          if (stepIconEl) stepIconEl.classList.add("pending");
        }
      });
    },

    updateUI(data) {
      // Exemplo de como atualizar a UI com os dados do status
      if (data.fsm_state) {
        // Atualiza a timeline, o preview, etc.
      }
    },

    showApiKeyStatus(message, type = "info") {
      const outputDiv = ArchonApp.elements.apiKeysOutput;
      let colorClass = "text-[#9daebe]"; // cinza-azulado (padrão)
      if (type === "success") colorClass = "text-green-400";
      if (type === "error") colorClass = "text-red-400";
      if (type === "loading") colorClass = "text-yellow-400";

      outputDiv.innerHTML = `<div class="${colorClass}">${message}</div>`;
    },
  },

  // OBJETO PARA CONTROLE DO SIDEBAR
  sidebar: {
    toggle() {
      const currentState = ArchonApp.state.sidebarState;

      if (currentState === "expanded") {
        this.toIconsOnly();
      } else if (currentState === "icons-only") {
        this.collapse();
      } else {
        this.expand();
      }

      // Atualizar visual do botão
      this.updateToggleButton();
    },

    toIconsOnly() {
      ArchonApp.state.sidebarState = "icons-only";
      const sidebar = ArchonApp.elements.sidebar;
      const expandBtn = ArchonApp.elements.sidebarExpandBtn;

      if (sidebar) {
        sidebar.classList.remove("sidebar-collapsed");
        sidebar.classList.add("sidebar-icons-only");
        // Remove estilos inline forçados
        sidebar.style.transform = "";
        sidebar.style.width = "";
      }

      if (expandBtn) {
        expandBtn.classList.add("hidden");
      }

      console.log("Sidebar modo ícones - mostra apenas ícones clicáveis");
    },

    expand() {
      ArchonApp.state.sidebarState = "expanded";
      const sidebar = ArchonApp.elements.sidebar;
      const expandBtn = ArchonApp.elements.sidebarExpandBtn;

      if (sidebar) {
        sidebar.classList.remove("sidebar-collapsed", "sidebar-icons-only");
        // Remove estilos inline forçados
        sidebar.style.transform = "";
        sidebar.style.width = "";
      }

      if (expandBtn) {
        expandBtn.classList.add("hidden");
      }

      console.log("Sidebar expandido - mostra ícones + texto");
    },

    collapse() {
      ArchonApp.state.sidebarState = "collapsed";
      const sidebar = ArchonApp.elements.sidebar;
      const expandBtn = ArchonApp.elements.sidebarExpandBtn;

      if (sidebar) {
        sidebar.classList.remove("sidebar-icons-only");
        sidebar.classList.add("sidebar-collapsed");
        // Remove estilos inline forçados
        sidebar.style.transform = "";
        sidebar.style.width = "";
      }

      if (expandBtn) {
        expandBtn.classList.remove("hidden");
      }

      console.log("Sidebar colapsado - completamente escondido");
    },

    updateToggleButton() {
      const toggleBtn = ArchonApp.elements.sidebarToggle;
      const currentState = ArchonApp.state.sidebarState;

      if (toggleBtn) {
        const icon = toggleBtn.querySelector(".sidebar-icon");
        if (icon) {
          // Remove classes anteriores
          toggleBtn.classList.remove(
            "state-expanded",
            "state-icons",
            "state-collapsed",
          );

          if (currentState === "expanded") {
            // Estado expandido: setas para esquerda (vai recolher para ícones)
            icon.style.transform = "rotate(0deg) scale(1)";
            toggleBtn.title = "Recolher para ícones";
            toggleBtn.classList.add("state-expanded");
          } else if (currentState === "icons-only") {
            // Estado ícones: setas para esquerda com efeito visual diferente
            icon.style.transform = "rotate(0deg) scale(0.9)";
            toggleBtn.title = "Esconder completamente";
            toggleBtn.classList.add("state-icons");
          } else {
            // Estado colapsado: setas para direita (vai expandir)
            icon.style.transform = "rotate(180deg) scale(1)";
            toggleBtn.title = "Expandir sidebar";
            toggleBtn.classList.add("state-collapsed");
          }
        }
      }
    },
  },
};

document.addEventListener("DOMContentLoaded", () => ArchonApp.init());