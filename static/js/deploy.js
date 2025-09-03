const DeployManager = {
    status: { vercel: false, supabase: false, stripe: false },
    debounceTimer: null,

    init() {
        this.cacheElements();
        if (!this.elements.content) {
            console.error('DeployManager Error: Content for step 7 not found in DOM.');
            return;
        }
        this.bindEvents();
        this.updateButtonStates();
        this.log('🚀 Digite o nome de um projeto para carregar suas configurações.');
        console.log('Deploy Manager Initialized.');
    },

    cacheElements() {
        this.elements = {
            content: document.getElementById('step-7-content'),
            saveBtn: document.getElementById('save-credentials-btn'),
            validateBtn: document.getElementById('validate-credentials-btn'),
            clearConsoleBtn: document.getElementById('clear-console-btn'),
            console: document.getElementById('deploy-console'),
            projectNameInput: document.getElementById('deploy-project-name'),
            vercelTokenInput: document.getElementById('vercel-token'),
            supabaseUrlInput: document.getElementById('supabase-url'),
            supabaseKeyInput: document.getElementById('supabase-key'),
            stripeSecretInput: document.getElementById('stripe-secret'),
            stripePublicInput: document.getElementById('stripe-public'),
            vercelStatus: document.getElementById('vercel-status'),
            supabaseStatus: document.getElementById('supabase-status'),
            stripeStatus: document.getElementById('stripe-status'),
            provisionDbBtn: document.getElementById('provision-database-btn'),
            deployFrontendBtn: document.getElementById('deploy-frontend-btn'),
            setupPaymentsBtn: document.getElementById('setup-payments-btn'),
            deployCompleteBtn: document.getElementById('deploy-complete-btn'),
            visibilityToggles: document.querySelectorAll('.toggle-visibility'),
        };
    },

    bindEvents() {
        if (!this.elements.saveBtn) return;

        this.elements.projectNameInput.addEventListener('input', () => {
            clearTimeout(this.debounceTimer);
            this.updateButtonStates();
            this.debounceTimer = setTimeout(() => this.getCredentialsStatus(), 500);
        });

        this.elements.saveBtn.addEventListener('click', () => this.saveCredentials());
        this.elements.validateBtn.addEventListener('click', () => this.validateCredentials());
        this.elements.clearConsoleBtn.addEventListener('click', () => this.clearConsole());

        // --- BOTÕES REATORADOS PARA NAVEGAÇÃO ---
        this.elements.provisionDbBtn.addEventListener('click', () => this.navigateToPage('supabase-setup'));
        this.elements.deployFrontendBtn.addEventListener('click', () => this.navigateToPage('vercel-setup'));
        this.elements.setupPaymentsBtn.addEventListener('click', () => this.navigateToPage('stripe-setup'));
        
        this.elements.deployCompleteBtn.addEventListener('click', () => this.completeDeploy());

        this.elements.visibilityToggles.forEach(toggle => {
            toggle.addEventListener('click', (e) => {
                const targetId = e.currentTarget.dataset.target;
                const targetInput = document.getElementById(targetId);
                if (targetInput) {
                    targetInput.type = targetInput.type === 'password' ? 'text' : 'password';
                }
            });
        });
    },

    navigateToPage(page) {
        const projectName = this.elements.projectNameInput.value.trim();
        if (!projectName) {
            this.log('Por favor, insira um nome de projeto antes de prosseguir.', 'error');
            return;
        }
        // O prefixo /deployment é adicionado por causa do registro do blueprint no Flask
        window.location.href = `/deployment/${page}?project_name=${encodeURIComponent(projectName)}`;
    },

    updateButtonStates() {
        const hasProjectName = this.elements.projectNameInput.value.trim() !== '';
        this.elements.saveBtn.disabled = !hasProjectName;
        this.elements.validateBtn.disabled = !hasProjectName;
    },

    async getCredentialsStatus() {
        const projectName = this.elements.projectNameInput.value.trim();
        if (!projectName) {
            this.resetStatusIndicators();
            return;
        }
        this.log(`Buscando configurações para o projeto: ${projectName}...`, 'api');
        try {
            const response = await fetch('/api/deploy/get_credentials_status', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ project_name: projectName })
            });
            if (!response.ok) throw new Error('Falha ao buscar status das credenciais.');
            const statusData = await response.json();
            this.updateStatusIndicator('vercel', statusData.vercel);
            this.updateStatusIndicator('supabase', statusData.supabase);
            this.updateStatusIndicator('stripe', statusData.stripe);
            this.log('Status das credenciais atualizado.');
        } catch (error) {
            this.log(error.message, 'error');
        }
    },

    resetStatusIndicators() {
        ['vercel', 'supabase', 'stripe'].forEach(provider => {
            this.updateStatusIndicator(provider, { configured: false });
        });
    },

    updateStatusIndicator(provider, status) {
        const statusEl = this.elements[`${provider}Status`];
        const actionBtn = this.elements[`${provider === 'vercel' ? 'deployFrontendBtn' : provider === 'supabase' ? 'provisionDbBtn' : 'setupPaymentsBtn'}`];
        this.status[provider] = status.configured;
        if (status.configured) {
            statusEl.textContent = 'Configurado';
            statusEl.className = 'px-2 py-1 text-xs rounded-full bg-green-600 text-white';
            if (actionBtn) actionBtn.disabled = false;
        } else {
            statusEl.textContent = 'Não configurado';
            statusEl.className = 'px-2 py-1 text-xs rounded-full bg-gray-600 text-gray-300';
            if (actionBtn) actionBtn.disabled = true;
        }
        this.checkCompleteDeployStatus();
    },

    checkCompleteDeployStatus() {
        const hasProjectName = this.elements.projectNameInput.value.trim() !== '';
        this.elements.deployCompleteBtn.disabled = !(hasProjectName && this.status.vercel && this.status.supabase);
    },

    async _runAction(actionFn) {
        const projectName = this.elements.projectNameInput.value.trim();
        if (!projectName) {
            this.log('Por favor, insira um nome de projeto antes de executar uma ação.', 'error');
            return;
        }
        await actionFn(projectName);
    },

    async saveCredentials() {
        this._runAction(async (projectName) => {
            this.log(`Salvando credenciais para ${projectName}...`, 'api');
            this.elements.saveBtn.disabled = true;
            const payload = {
                project_name: projectName,
                vercel_token: this.elements.vercelTokenInput.value,
                supabase_url: this.elements.supabaseUrlInput.value,
                supabase_key: this.elements.supabaseKeyInput.value,
                stripe_secret: this.elements.stripeSecretInput.value,
                stripe_public: this.elements.stripePublicInput.value,
            };
            try {
                const response = await fetch('/api/deploy/save_credentials', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const result = await response.json();
                if (!response.ok) throw new Error(result.error || 'Erro desconhecido ao salvar.');
                this.log(result.message, 'success');
                await this.getCredentialsStatus();
            } catch (error) {
                this.log(error.message, 'error');
            } finally {
                this.elements.saveBtn.disabled = false;
            }
        });
    },

    async validateCredentials() {
        this._runAction(async (projectName) => {
            this.log(`Validando credenciais para ${projectName}...`, 'api');
            this.elements.validateBtn.disabled = true;
            try {
                const response = await fetch('/api/deploy/validate_credentials', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ project_name: projectName })
                });
                const results = await response.json();
                if (!response.ok) throw new Error(results.error || 'Erro desconhecido na validação.');
                this.log('--- Relatório de Validação ---', 'info');
                for (const [provider, result] of Object.entries(results)) {
                    if (result.success) {
                        this.log(`${provider.toUpperCase()}: ${result.message}`, 'success');
                    } else {
                        this.log(`${provider.toUpperCase()}: ${result.error}`, 'error');
                    }
                }
                this.log('--- Fim do Relatório ---', 'info');
            } catch (error) {
                this.log(error.message, 'error');
            } finally {
                this.elements.validateBtn.disabled = false;
            }
        });
    },

    async completeDeploy() {
        this._runAction(async (projectName) => {
            this.log('🚀 Iniciando Deploy Completo Orquestrado...', 'warn');
            this.elements.deployCompleteBtn.disabled = true;
            try {
                const response = await fetch('/api/deploy/complete_deploy', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ project_name: projectName })
                });
                const result = await response.json();
                if (!response.ok) throw new Error(result.error || 'Erro desconhecido no deploy completo.');
                this.log('--- Relatório do Deploy Completo ---', 'info');
                result.details.forEach(detail => {
                    this.log(`[${detail.provider.toUpperCase()}] Deploy finalizado.`, 'success');
                    this.log(JSON.stringify(detail.output, null, 2), 'success');
                });
                this.log(result.message, 'success');
                this.log('--- Fim do Relatório ---', 'info');
            } catch (error) {
                this.log(`Falha no deploy completo: ${error.message}`, 'error');
            } finally {
                this.elements.deployCompleteBtn.disabled = false;
            }
        });
    },

    log(message, type = 'info') {
        if (!this.elements.console) return;
        const timestamp = new Date().toLocaleTimeString('pt-BR');
        let colorClass = 'text-[#9daebe]';
        let icon = 'ℹ️';
        switch (type) {
            case 'success': colorClass = 'text-green-400'; icon = '✅'; break;
            case 'error': colorClass = 'text-red-400'; icon = '❌'; break;
            case 'warn': colorClass = 'text-yellow-400'; icon = '⚠️'; break;
            case 'api': colorClass = 'text-cyan-400'; icon = '📡'; break;
        }
        const logEntry = document.createElement('div');
        logEntry.className = 'mb-1';
        logEntry.innerHTML = `<span class="text-purple-400">[${timestamp}]</span> <span class="${colorClass}">${icon} ${message}</span>`;
        this.elements.console.appendChild(logEntry);
        this.elements.console.scrollTop = this.elements.console.scrollHeight;
    },

    clearConsole() {
        this.elements.console.innerHTML = '';
        this.log('Console limpo.', 'warn');
    }
};