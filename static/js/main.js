// static/js/main.js
// =================================================================================
// ARCHON DASHBOARD - REBUILT & RECONNECTED FRONTEND LOGIC
// =================================================================================
// This script manages the entire dashboard UI, state, and API communication.
// It is the single source of truth for all frontend interactivity.

const ArchonDashboard = {
    // ---------------------------------------------------------------------------
    // 1. STATE & CONFIGURATION
    // ---------------------------------------------------------------------------
    state: {
        currentStep: 1,
        projectName: null,
        isPolling: false,
        pollingInterval: null,
        timeline: [], // Authoritative timeline from the backend
    },

    // Cache for DOM elements
    elements: {},

    // ---------------------------------------------------------------------------
    // 2. INITIALIZATION
    // ---------------------------------------------------------------------------
    init() {
        document.addEventListener('DOMContentLoaded', () => {
            this.cacheDomElements();
            this.bindEventListeners();
            this.apiKeyModal.init();
            this.checkProjectStatus(); // Initial status check
            this.startPolling();
            console.log("ArchonDashboard Initialized and Connected.");
        });
    },

    cacheDomElements() {
        this.elements = {
            contentArea: document.getElementById('content-area'),
            sidebar: document.getElementById('sidebar'),
            openApiKeyModalBtn: document.getElementById('open-api-key-modal'),
            resetProjectBtn: document.getElementById('reset-project'),
            loadProposalGeneratorLink: document.getElementById('load-proposal-generator'),
            stepLinks: document.querySelectorAll('.step-link'),
        };
    },

    bindEventListeners() {
        // Header
        this.elements.openApiKeyModalBtn.addEventListener('click', () => this.apiKeyModal.open());
        this.elements.resetProjectBtn.addEventListener('click', () => this.resetProject());

        // Sidebar Links
        this.elements.loadProposalGeneratorLink.addEventListener('click', (e) => {
            e.preventDefault();
            this.loadContent('{{ url_for('proposal_generator') }}', 'Gerador de Propostas');
        });

        this.elements.stepLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const step = e.currentTarget.dataset.step;
                const name = e.currentTarget.dataset.name;
                this.loadContent(`/api/get_step_template/${step}`, name);
            });
        });

        // Event Delegation for dynamically loaded content
        this.elements.contentArea.addEventListener('click', (e) => {
            const button = e.target.closest('button[data-action]');
            if (button) {
                e.preventDefault();
                const action = button.dataset.action;
                this.performAction(action);
            }
        });
    },

    // ---------------------------------------------------------------------------
    // 3. CORE LOGIC & API CALLS
    // ---------------------------------------------------------------------------
    startPolling() {
        if (!this.state.isPolling) {
            this.state.isPolling = true;
            this.state.pollingInterval = setInterval(() => this.checkProjectStatus(), 5000);
            console.log("Backend polling started.");
        }
    },

    async checkProjectStatus() {
        try {
            const response = await fetch('/api/supervisor/status');
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            this.updateUI(data);
        } catch (error) {
            console.error("Error fetching project status:", error);
            // Optionally, display an error message to the user in the UI
        }
    },

    async performAction(action) {
        console.log(`Performing action: ${action}`);
        const observationsTextarea = document.getElementById('observations-textarea');
        const previewTextarea = document.getElementById('preview-textarea');

        const payload = {
            action: action,
            observation: observationsTextarea ? observationsTextarea.value : "",
            project_name: this.state.projectName,
            current_preview_content: previewTextarea ? previewTextarea.value : "",
        };

        try {
            const response = await fetch('/api/supervisor/action', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            // Immediately update the UI after a successful action
            this.checkProjectStatus();
        } catch (error) {
            console.error(`Error performing action '${action}':`, error);
        }
    },

    async loadContent(url, contentName) {
        this.elements.contentArea.innerHTML = `<p class="text-center">Carregando ${contentName}...</p>`;
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Network response was not ok. Status: ${response.status}`);
            
            const html = await response.text();
            this.elements.contentArea.innerHTML = html;
            
            // After loading new content, immediately run checkProjectStatus
            // to populate it with the latest data from the backend.
            this.checkProjectStatus();

        } catch (error) {
            console.error(`Error loading content from ${url}:`, error);
            this.elements.contentArea.innerHTML = `<p class="text-center text-red-500">Erro ao carregar o conteúdo. Detalhes: ${error.message}</p>`;
        }
    },

    resetProject() {
        if (confirm("Você tem certeza que deseja resetar o projeto? Todo o progresso e artefatos gerados serão perdidos.")) {
            console.log("Requesting project reset...");
            fetch('/api/supervisor/reset', { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        window.location.reload();
                    } else {
                        alert("Falha ao resetar o projeto.");
                    }
                });
        }
    },

    // ---------------------------------------------------------------------------
    // 4. UI UPDATES
    // ---------------------------------------------------------------------------
    updateUI(data) {
        if (!data) return;

        // Update global state
        this.state.projectName = data.project_name;
        this.state.timeline = data.timeline || [];
        
        // Find the current step to display
        const inProgressStep = this.state.timeline.find(s => s.status === 'in-progress');
        const currentStepIndex = inProgressStep ? this.state.timeline.indexOf(inProgressStep) : -1;
        this.state.currentStep = currentStepIndex + 1;

        this.updateSidebar();
        this.updateDynamicContent(data);
    },

    updateSidebar() {
        this.elements.stepLinks.forEach((link, index) => {
            const stepStatus = this.state.timeline[index]?.status || 'pending';
            link.classList.remove('bg-green-600', 'bg-blue-600', 'bg-gray-700', 'text-white');

            switch(stepStatus) {
                case 'completed':
                    link.classList.add('bg-green-600', 'text-white');
                    break;
                case 'in-progress':
                    link.classList.add('bg-blue-600', 'text-white');
                    break;
                case 'pending':
                default:
                    link.classList.add('bg-gray-700');
                    break;
            }
        });
    },

    updateDynamicContent(data) {
        // This function is responsible for updating the content inside #content-area
        // that was dynamically loaded.
        
        // Update project name if the element exists
        const projectNameDisplay = document.getElementById('project-name-display');
        if (projectNameDisplay) {
            projectNameDisplay.textContent = data.project_name || "Nome do Projeto Ainda Não Definido";
        }

        // Update preview textarea if it exists
        const previewTextarea = document.getElementById('preview-textarea');
        if (previewTextarea && data.current_step) {
            previewTextarea.value = data.current_step.preview_content || "";
        }

        // Update action buttons based on backend state
        const actions = data.actions || {};
        const approveButton = document.querySelector('button[data-action="approve"]');
        const repeatButton = document.querySelector('button[data-action="repeat"]');
        const backButton = document.querySelector('button[data-action="back"]');

        if (approveButton) approveButton.disabled = data.is_finished;
        if (repeatButton) repeatButton.disabled = data.is_finished;
        if (backButton) backButton.disabled = !actions.can_go_back;
    },

    // ---------------------------------------------------------------------------
    // 5. API KEY MODAL LOGIC (No changes needed here)
    // ---------------------------------------------------------------------------
    apiKeyModal: {
        elements: {},
        init() {
            this.elements = {
                modal: document.getElementById('api-key-modal'),
                closeBtn: document.getElementById('close-api-key-modal'),
                statusDiv: document.getElementById('api-key-status'),
                keyInput: document.getElementById('api-key-input'),
                messageDiv: document.getElementById('api-key-message'),
                testBtn: document.getElementById('test-api-key'),
                saveBtn: document.getElementById('save-api-key-action'),
                removeBtn: document.getElementById('remove-api-key'),
                providerSelect: document.getElementById('api-provider-select'),
                toggleVisibilityBtn: document.getElementById('toggle-api-key-visibility'),
                eyeIcon: document.getElementById('eye-icon'),
                eyeOffIcon: document.getElementById('eye-off-icon'),
                openModalButton: document.getElementById('open-api-key-modal')
            };
            this.bindEvents();
            this.checkStatus();
        },
        bindEvents() {
            this.elements.closeBtn.addEventListener('click', () => this.close());
            this.elements.toggleVisibilityBtn.addEventListener('click', () => this.toggleVisibility());
            this.elements.saveBtn.addEventListener('click', () => this.save());
            this.elements.testBtn.addEventListener('click', () => this.test());
            this.elements.removeBtn.addEventListener('click', () => this.remove());
            this.elements.providerSelect.addEventListener('change', () => this.checkStatus());
        },
        open() {
            this.elements.modal.classList.remove('hidden');
            this.checkStatus();
        },
        close() {
            this.elements.modal.classList.add('hidden');
        },
        toggleVisibility() {
            if (this.elements.keyInput.type === 'password') {
                this.elements.keyInput.type = 'text';
                this.elements.eyeIcon.classList.add('hidden');
                this.elements.eyeOffIcon.classList.remove('hidden');
            } else {
                this.elements.keyInput.type = 'password';
                this.elements.eyeIcon.classList.remove('hidden');
                this.elements.eyeOffIcon.classList.add('hidden');
            }
        },
        showMessage(message, isError = false) {
            this.elements.messageDiv.textContent = message;
            this.elements.messageDiv.className = isError ? 'text-red-400 text-sm text-center h-5' : 'text-green-400 text-sm text-center h-5';
        },
        async checkStatus() {
            const provider = this.elements.providerSelect.value;
            if (provider !== 'gemini') {
                this.elements.statusDiv.innerHTML = `<p class="text-yellow-400">Verificação de status não implementada para ${provider}.</p>`;
                this.elements.openModalButton.classList.remove('api-key-alert');
                return;
            }
            try {
                const response = await fetch('/api/keys/check');
                const data = await response.json();
                if (data.is_configured) {
                    this.elements.statusDiv.innerHTML = '<p class="text-green-400 font-semibold">API Key do Gemini está configurada e ativa.</p>';
                    this.elements.removeBtn.disabled = false;
                    this.elements.openModalButton.classList.remove('api-key-alert');
                } else {
                    this.elements.statusDiv.innerHTML = '<p class="text-yellow-400">API Key do Gemini não configurada.</p>';
                    this.elements.removeBtn.disabled = true;
                    this.elements.openModalButton.classList.add('api-key-alert');
                }
            } catch (error) {
                this.elements.statusDiv.innerHTML = '<p class="text-red-500">Erro ao verificar o status da API Key.</p>';
                this.elements.openModalButton.classList.add('api-key-alert');
            }
        },
        async save() {
            const apiKey = this.elements.keyInput.value.trim();
            const provider = this.elements.providerSelect.value;
            if (!apiKey) {
                return this.showMessage('Por favor, insira uma API Key.', true);
            }
            try {
                const response = await fetch('/api/keys/save', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ provider, api_key: apiKey })
                });
                const data = await response.json();
                this.showMessage(data.message || data.error, !response.ok);
                if (response.ok) this.checkStatus();
            } catch (error) {
                this.showMessage('Erro ao salvar a API Key.', true);
            }
        },
        async test() {
            const apiKey = this.elements.keyInput.value.trim();
            const provider = this.elements.providerSelect.value;
            if (!apiKey) {
                return this.showMessage('Por favor, insira uma API Key para testar.', true);
            }
            this.showMessage(`Testando a chave para ${provider}...`);
            try {
                const response = await fetch('/api/keys/test', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ provider, api_key: apiKey })
                });
                const data = await response.json();
                this.showMessage(data.message, !data.success);
                 if (data.success) {
                    const archonMessageDiv = document.createElement('div');
                    archonMessageDiv.className = 'mt-4 p-4 bg-blue-900 border border-blue-700 rounded-lg text-center';
                    archonMessageDiv.innerHTML = '<p class="font-mono text-lg text-blue-300">🤖 Oi, sou o Archon e estou pronto para começar.</p>';
                    this.elements.messageDiv.after(archonMessageDiv);
                    setTimeout(() => archonMessageDiv.remove(), 5000);
                }
            } catch (error) {
                this.showMessage('Erro ao testar a API Key.', true);
            }
        },
        async remove() {
            const provider = this.elements.providerSelect.value;
            try {
                const response = await fetch('/api/keys/remove', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ provider })
                });
                const data = await response.json();
                this.showMessage(data.message || data.error, !response.ok);
                if (response.ok) {
                    this.checkStatus();
                    this.elements.keyInput.value = '';
                }
            } catch (error) {
                this.showMessage('Erro ao remover a API Key.', true);
            }
        }
    }
};

// Initialize the application
ArchonDashboard.init();