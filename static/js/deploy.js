// Deploy and Provisioning Interface JavaScript
class DeployManager {
  constructor() {
    this.initializeEventListeners();
    this.loadCredentialsStatus();
  }

  initializeEventListeners() {
    // Toggle visibility para campos de senha
    document.querySelectorAll(".toggle-visibility").forEach((button) => {
      button.addEventListener(
        "click",
        this.togglePasswordVisibility.bind(this),
      );
    });

    // Salvar credenciais
    const saveBtn = document.getElementById("save-credentials-btn");
    if (saveBtn) {
      saveBtn.addEventListener("click", this.saveCredentials.bind(this));
    }

    // Validar credenciais
    const validateBtn = document.getElementById("validate-credentials-btn");
    if (validateBtn) {
      validateBtn.addEventListener(
        "click",
        this.validateCredentials.bind(this),
      );
    }

    // Action buttons
    const provisionBtn = document.getElementById("provision-database-btn");
    if (provisionBtn) {
      provisionBtn.addEventListener("click", () =>
        this.executeAction("provision_database"),
      );
    }

    const deployBtn = document.getElementById("deploy-frontend-btn");
    if (deployBtn) {
      deployBtn.addEventListener("click", () =>
        this.executeAction("deploy_frontend"),
      );
    }

    const paymentsBtn = document.getElementById("setup-payments-btn");
    if (paymentsBtn) {
      paymentsBtn.addEventListener("click", () =>
        this.executeAction("setup_payments"),
      );
    }

    const completeBtn = document.getElementById("deploy-complete-btn");
    if (completeBtn) {
      completeBtn.addEventListener("click", () =>
        this.executeAction("complete_deploy"),
      );
    }

    // Clear console
    const clearBtn = document.getElementById("clear-console-btn");
    if (clearBtn) {
      clearBtn.addEventListener("click", this.clearConsole.bind(this));
    }

    // Monitor input changes to enable/disable buttons
    document.querySelectorAll(".credentials-input").forEach((input) => {
      input.addEventListener("input", this.updateButtonStates.bind(this));
    });
  }

  togglePasswordVisibility(event) {
    const button = event.currentTarget;
    const targetId = button.getAttribute("data-target");
    const input = document.getElementById(targetId);

    if (input.type === "password") {
      input.type = "text";
      button.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                    <line x1="1" x2="23" y1="1" y2="23"/>
                </svg>
            `;
    } else {
      input.type = "password";
      button.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                </svg>
            `;
    }
  }

  async loadCredentialsStatus() {
    try {
      const response = await fetch("/api/deploy/get_credentials_status");
      const data = await response.json();

      if (data.status) {
        this.updateStatusIndicators(data.status);
        this.updateButtonStates();
      }
    } catch (error) {
      this.logToConsole(
        `❌ Erro ao carregar status das credenciais: ${error.message}`,
        "error",
      );
    }
  }

  updateStatusIndicators(status) {
    // Atualizar indicadores visuais
    const vercelStatus = document.getElementById("vercel-status");
    const supabaseStatus = document.getElementById("supabase-status");
    const stripeStatus = document.getElementById("stripe-status");

    if (vercelStatus) {
      if (status.vercel === "configured") {
        vercelStatus.textContent = "Configurado";
        vercelStatus.className =
          "px-2 py-1 text-xs rounded-full bg-green-600 text-green-100";
      } else {
        vercelStatus.textContent = "Não configurado";
        vercelStatus.className =
          "px-2 py-1 text-xs rounded-full bg-gray-600 text-gray-300";
      }
    }

    if (supabaseStatus) {
      if (status.supabase === "configured") {
        supabaseStatus.textContent = "Configurado";
        supabaseStatus.className =
          "px-2 py-1 text-xs rounded-full bg-green-600 text-green-100";
      } else {
        supabaseStatus.textContent = "Não configurado";
        supabaseStatus.className =
          "px-2 py-1 text-xs rounded-full bg-gray-600 text-gray-300";
      }
    }

    if (stripeStatus) {
      if (status.stripe === "configured") {
        stripeStatus.textContent = "Configurado";
        stripeStatus.className =
          "px-2 py-1 text-xs rounded-full bg-green-600 text-green-100";
      } else {
        stripeStatus.textContent = "Não configurado";
        stripeStatus.className =
          "px-2 py-1 text-xs rounded-full bg-gray-600 text-gray-300";
      }
    }
  }

  async saveCredentials() {
    const saveBtn = document.getElementById("save-credentials-btn");
    const originalText = saveBtn.innerHTML;

    // Disable button and show loading
    saveBtn.disabled = true;
    saveBtn.innerHTML = `
            <span class="flex items-center justify-center gap-2">
                <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" class="opacity-25"></circle>
                    <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" class="opacity-75"></path>
                </svg>
                Salvando...
            </span>
        `;

    try {
      const credentials = {
        vercel_token: document.getElementById("vercel-token").value.trim(),
        supabase_url: document.getElementById("supabase-url").value.trim(),
        supabase_key: document.getElementById("supabase-key").value.trim(),
        stripe_secret: document.getElementById("stripe-secret").value.trim(),
        stripe_public: document.getElementById("stripe-public").value.trim(),
      };

      const response = await fetch("/api/deploy/save_credentials", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(credentials),
      });

      const data = await response.json();

      if (response.ok) {
        this.logToConsole(`✅ ${data.message}`, "success");
        this.loadCredentialsStatus(); // Reload status
      } else {
        this.logToConsole(`❌ ${data.error}`, "error");
      }
    } catch (error) {
      this.logToConsole(
        `❌ Erro ao salvar credenciais: ${error.message}`,
        "error",
      );
    } finally {
      // Restore button
      saveBtn.disabled = false;
      saveBtn.innerHTML = originalText;
    }
  }

  async validateCredentials() {
    const validateBtn = document.getElementById("validate-credentials-btn");
    const originalText = validateBtn.innerHTML;

    validateBtn.disabled = true;
    validateBtn.innerHTML = `
            <svg class="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" class="opacity-25"></circle>
                <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" class="opacity-75"></path>
            </svg>
            <span>Validando...</span>
        `;

    try {
      this.logToConsole("🔍 Iniciando validação das credenciais...", "info");

      const response = await fetch("/api/deploy/validate_credentials", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();

      if (response.ok && data.results) {
        this.logToConsole("📋 Resultados da validação:", "info");

        Object.entries(data.results).forEach(([provider, result]) => {
          const icon =
            result.status === "valid"
              ? "✅"
              : result.status === "invalid"
                ? "❌"
                : "⚠️";
          this.logToConsole(
            `${icon} ${provider.toUpperCase()}: ${result.message}`,
            result.status === "valid" ? "success" : "error",
          );
        });

        // Update button states based on validation
        this.updateButtonStates();
      } else {
        this.logToConsole(
          `❌ Erro na validação: ${data.error || "Erro desconhecido"}`,
          "error",
        );
      }
    } catch (error) {
      this.logToConsole(
        `❌ Erro ao validar credenciais: ${error.message}`,
        "error",
      );
    } finally {
      validateBtn.disabled = false;
      validateBtn.innerHTML = originalText;
    }
  }

  async executeAction(action) {
    const projectName =
      document.getElementById("deploy-project-name").value.trim() ||
      "default-project";
    const buttonId = this.getButtonIdForAction(action);
    const button = document.getElementById(buttonId);

    if (!button) return;

    const originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = `
            <svg class="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" class="opacity-25"></circle>
                <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" class="opacity-75"></path>
            </svg>
            <span>Executando...</span>
        `;

    try {
      this.logToConsole(`🚀 Iniciando: ${this.getActionName(action)}`, "info");

      const response = await fetch(`/api/deploy/${action}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ project_name: projectName }),
      });

      const data = await response.json();

      if (response.ok) {
        this.logToConsole(`✅ ${data.message}`, "success");

        if (data.output) {
          this.logToConsole(data.output, "output");
        }

        if (data.results) {
          Object.entries(data.results).forEach(([step, result]) => {
            const icon = result.success ? "✅" : "❌";
            this.logToConsole(
              `${icon} ${step}: ${result.success ? "Sucesso" : result.error}`,
              result.success ? "success" : "error",
            );
          });
        }
      } else {
        this.logToConsole(`❌ ${data.error}`, "error");
      }
    } catch (error) {
      this.logToConsole(`❌ Erro na execução: ${error.message}`, "error");
    } finally {
      button.disabled = false;
      button.innerHTML = originalText;
    }
  }

  getButtonIdForAction(action) {
    const mapping = {
      provision_database: "provision-database-btn",
      deploy_frontend: "deploy-frontend-btn",
      setup_payments: "setup-payments-btn",
      complete_deploy: "deploy-complete-btn",
    };
    return mapping[action];
  }

  getActionName(action) {
    const mapping = {
      provision_database: "Provisionamento do Banco de Dados",
      deploy_frontend: "Deploy do Frontend",
      setup_payments: "Configuração de Pagamentos",
      complete_deploy: "Deploy Completo",
    };
    return mapping[action];
  }

  updateButtonStates() {
    // Enable/disable action buttons based on credentials
    const hasAnyCredentials = this.hasAnyCredentials();

    const actionButtons = [
      "provision-database-btn",
      "deploy-frontend-btn",
      "setup-payments-btn",
      "deploy-complete-btn",
    ];

    actionButtons.forEach((buttonId) => {
      const button = document.getElementById(buttonId);
      if (button) {
        button.disabled = !hasAnyCredentials;
      }
    });
  }

  hasAnyCredentials() {
    const vercelToken = document.getElementById("vercel-token").value.trim();
    const supabaseUrl = document.getElementById("supabase-url").value.trim();
    const supabaseKey = document.getElementById("supabase-key").value.trim();
    const stripeSecret = document.getElementById("stripe-secret").value.trim();

    return vercelToken || (supabaseUrl && supabaseKey) || stripeSecret;
  }

  logToConsole(message, type = "info") {
    const console = document.getElementById("deploy-console");
    if (!console) return;

    const timestamp = new Date().toLocaleTimeString();
    const colors = {
      info: "text-blue-400",
      success: "text-green-400",
      error: "text-red-400",
      output: "text-[#9daebe]",
    };

    const line = document.createElement("div");
    line.className = `${colors[type] || colors.info} mb-1`;
    line.innerHTML = `<span class="text-gray-500">[${timestamp}]</span> ${message}`;

    console.appendChild(line);
    console.scrollTop = console.scrollHeight;
  }

  clearConsole() {
    const console = document.getElementById("deploy-console");
    if (console) {
      console.innerHTML =
        '<div class="text-[#9daebe]">🚀 Console pronto para deploy...</div>';
    }
  }
}

// Initialize when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  // Only initialize if we're on the dashboard page with deploy section
  if (document.getElementById("step-7-content")) {
    window.deployManager = new DeployManager();
  }
});

// Export for use in other scripts if needed
window.DeployManager = DeployManager;
