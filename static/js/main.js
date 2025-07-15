// static/js/main.js

// =================================================================================
// ARCHON APP - REFACTORED FRONTEND LOGIC
// =================================================================================
// This script manages the entire dashboard UI, state, and API communication.
// It's designed to be state-driven and robust.

const ArchonApp = {
  // ---------------------------------------------------------------------------
  // 1. STATE MANAGEMENT
  // ---------------------------------------------------------------------------
  // Centralized state for the entire application. UI is a function of this state.
  state: {
    currentStep: 1,
    totalSteps: 7,
    projectName: null,
    sidebarState: "expanded", // "expanded", "icons-only", "collapsed"
    isPolling: false,
    pollingInterval: null,
    timeline: [], // Authoritative timeline from the backend
  },

  // ---------------------------------------------------------------------------
  // 2. INITIALIZATION
  // ---------------------------------------------------------------------------
  // Entry point of the application.
  init() {
    this.elements.cache();
    this.events.bind();
    this.api.fetchStatus(); // Get initial state from backend
    this.sidebar.applyCurrentState(); // Apply initial sidebar state
    this.startPolling();
  },

  // Starts polling the backend for status updates.
  startPolling() {
    if (!this.state.isPolling) {
      this.state.isPolling = true;
      this.state.pollingInterval = setInterval(() => this.api.fetchStatus(), 5000);
      console.log("Backend polling started.");
    }
  },

  // ---------------------------------------------------------------------------
  // 3. DOM ELEMENTS CACHE
  // ---------------------------------------------------------------------------
  // Caches all necessary DOM elements for performance.
  elements: {
    _cache: {},
    cache() {
      this._cache = {
        sidebar: document.getElementById("sidebar"),
        sidebarSteps: document.querySelectorAll(".sidebar-step[data-step]"),
        stepContentWrapper: document.getElementById("step-content-wrapper"),
        sidebarToggle: document.getElementById("sidebar-toggle"),
        sidebarExpandBtn: document.getElementById("sidebar-expand-btn"),
        mainContent: document.getElementById("main-content"),
        btnShutdown: document.getElementById("btn-shutdown"),
      };
    },
    get(key) {
      return this._cache[key];
    },
  },

  // ---------------------------------------------------------------------------
  // 4. EVENT BINDING
  // ---------------------------------------------------------------------------
  // Binds all event listeners.
  events: {
    bind() {
      const elements = ArchonApp.elements;

      // Sidebar step navigation
      elements.get("sidebarSteps").forEach((step) => {
        step.addEventListener("click", () => {
          const stepNum = parseInt(step.dataset.step, 10);
          ArchonApp.ui.showStep(stepNum);
        });
      });

      // Sidebar controls
      elements.get("sidebarToggle")?.addEventListener("click", () => ArchonApp.sidebar.toggle());
      elements.get("sidebarExpandBtn")?.addEventListener("click", () => ArchonApp.sidebar.expand());

      // Global actions
      elements.get("btnShutdown")?.addEventListener("click", () => {
        if (confirm("Você tem certeza que deseja resetar o projeto? Todo o progresso e artefatos gerados serão perdidos.")) {
          ArchonApp.api.resetProject();
        }
      });

      // Delegated events for dynamically loaded content
      elements.get("stepContentWrapper").addEventListener("click", (e) => {
        const button = e.target.closest("button");
        if (!button) return;

        const action = button.dataset.action;
        if (!action) return;

        const observation = document.getElementById("observations-textarea")?.value || "";
        const previewContent = document.getElementById("preview-textarea")?.value || "";

        if (action === 'generate_base') {
            ArchonApp.api.generateProjectBase();
        } else {
            ArchonApp.api.performAction(action, observation, previewContent);
        }
      });
    },
  },

  // ---------------------------------------------------------------------------
  // 5. API COMMUNICATION
  // ---------------------------------------------------------------------------
  // Handles all fetch requests to the backend.
  api: {
    async fetchStatus() {
      try {
        const response = await fetch("/api/supervisor/status");
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        const data = await response.json();
        ArchonApp.ui.update(data);
      } catch (error) {
        console.error("Error fetching status:", error);
      }
    },
    async performAction(action, observation = "", content = "") {
      try {
        const response = await fetch("/api/supervisor/action", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            action,
            observation,
            project_name: ArchonApp.state.projectName,
            current_preview_content: content,
          }),
        });
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        const data = await response.json();
        ArchonApp.ui.update(data);
      } catch (error) {
        console.error(`Error performing action '${action}':`, error);
      }
    },
    async generateProjectBase() {
        const name = document.getElementById('project-name-input')?.value;
        const description = document.getElementById('project-description')?.value;
        if (!name || !description) {
            return alert("Nome e descrição do projeto são obrigatórios.");
        }
        ArchonApp.state.projectName = name;
        const formData = new FormData(document.querySelector('form'));
        formData.append('project_name', name);
        formData.append('project_description', description);
        // Lógica de envio...
    },
    async resetProject() {
        // Lógica de reset...
    },
  },

  // ---------------------------------------------------------------------------
  // 6. UI MANIPULATION
  // ---------------------------------------------------------------------------
  // Handles all updates to the DOM.
  ui: {
    // Main UI update function, called after API calls.
    update(data) {
      if (!data) return;
      
      ArchonApp.state.projectName = data.project_name;
      ArchonApp.state.timeline = data.timeline;

      const inProgressStep = data.timeline.find(s => s.status === 'in-progress');
      const stepToShow = inProgressStep ? data.timeline.indexOf(inProgressStep) + 1 : (data.is_finished ? ArchonApp.state.totalSteps : 1);

      if (ArchonApp.state.currentStep !== stepToShow) {
        this.showStep(stepToShow);
      }
      
      this.updateSidebarState(data.timeline);
      this.updateSupervisorPanel(data);
    },

    // Shows the content for a specific step by fetching it from the server.
    async showStep(stepNumber) {
      ArchonApp.state.currentStep = stepNumber;
      const wrapper = ArchonApp.elements.get("stepContentWrapper");
      wrapper.innerHTML = `<div class="loading-spinner"></div>`; // Show a spinner

      try {
        const response = await fetch(`/api/get_step_template/${stepNumber}`);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const html = await response.text();
        wrapper.innerHTML = html;

        // After loading, re-run the status update to populate the new content
        // with the latest data (e.g., preview content, button states).
        ArchonApp.api.fetchStatus(); 
        
      } catch (error) {
        console.error(`Error fetching step ${stepNumber}:`, error);
        wrapper.innerHTML = `<p class="text-red-500">Error loading content. Please try again.</p>`;
      }

      // Immediate visual feedback on the sidebar
      this.updateSidebarState(null, stepNumber);
    },

    // Updates the sidebar visual state (colors, icons).
    updateSidebarState(timelineData, clickedStep = null) {
      const timeline = timelineData || ArchonApp.state.timeline;
      ArchonApp.elements.get("sidebarSteps").forEach((step, index) => {
        const stepNum = index + 1;
        const status = timeline[index]?.status || 'pending';

        step.classList.remove("current", "completed", "pending");

        if (clickedStep && stepNum === clickedStep) {
          step.classList.add("current");
        } else {
          if (status === 'completed') step.classList.add("completed");
          else if (status === 'in-progress') step.classList.add("current");
          else step.classList.add("pending");
        }
      });
    },

    // Updates the supervisor panel content and button states.
    updateSupervisorPanel(data) {
        const preview = document.getElementById("preview-textarea");
        if (preview) preview.value = data.current_step.preview_content || "";

        const actions = data.actions;
        document.querySelector('[data-action="approve"]')?.toggleAttribute("disabled", data.is_finished);
        document.querySelector('[data-action="repeat"]')?.toggleAttribute("disabled", data.is_finished);
        document.querySelector('[data-action="back"]')?.toggleAttribute("disabled", !actions.can_go_back);
        document.querySelector('[data-action="start"]')?.toggleAttribute("disabled", !ArchonApp.state.projectName);
    }
  },

  // ---------------------------------------------------------------------------
  // 7. SIDEBAR LOGIC
  // ---------------------------------------------------------------------------
  // Manages the sidebar's visual states (expanded, icons-only, collapsed).
  sidebar: {
    toggle() {
      const state = ArchonApp.state;
      if (state.sidebarState === "expanded") this.toIconsOnly();
      else if (state.sidebarState === "icons-only") this.collapse();
      else this.expand();
    },
    expand() {
      ArchonApp.state.sidebarState = "expanded";
      this.applyCurrentState();
    },
    toIconsOnly() {
      ArchonApp.state.sidebarState = "icons-only";
      this.applyCurrentState();
    },
    collapse() {
      ArchonApp.state.sidebarState = "collapsed";
      this.applyCurrentState();
    },
    applyCurrentState() {
      const sidebar = ArchonApp.elements.get("sidebar");
      const mainContent = ArchonApp.elements.get("mainContent");
      const expandBtn = ArchonApp.elements.get("sidebarExpandBtn");
      const state = ArchonApp.state.sidebarState;

      sidebar.classList.remove("sidebar-expanded", "sidebar-icons-only", "sidebar-collapsed");
      
      if (state === "expanded") {
        sidebar.classList.add("sidebar-expanded");
        mainContent.style.marginLeft = "384px";
        expandBtn.classList.add("hidden");
      } else if (state === "icons-only") {
        sidebar.classList.add("sidebar-icons-only");
        mainContent.style.marginLeft = "80px";
        expandBtn.classList.add("hidden");
      } else { // collapsed
        sidebar.classList.add("sidebar-collapsed");
        mainContent.style.marginLeft = "0";
        expandBtn.classList.remove("hidden");
      }
      this.updateToggleButton();
    },
    updateToggleButton() {
      const toggleBtn = ArchonApp.elements.get("sidebarToggle");
      if (!toggleBtn) return;
      const icon = toggleBtn.querySelector(".sidebar-icon");
      const state = ArchonApp.state.sidebarState;
      
      if (state === "expanded") {
        icon.style.transform = "rotate(0deg)";
        toggleBtn.title = "Recolher para ícones";
      } else if (state === "icons-only") {
        icon.style.transform = "rotate(0deg)";
        toggleBtn.title = "Esconder completamente";
      } else {
        icon.style.transform = "rotate(180deg)";
        toggleBtn.title = "Expandir sidebar";
      }
    }
  },
};

document.addEventListener("DOMContentLoaded", () => ArchonApp.init());
