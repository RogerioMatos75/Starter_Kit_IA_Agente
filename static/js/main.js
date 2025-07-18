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
            this.checkApiKeyStatus(); // << NOVO: Verifica o status da chave de API
            this.startPolling();
            console.log("ArchonDashboard Initialized and Connected.");
        });
    },

    cacheDomElements() {
        this.elements = {
            contentArea: document.getElementById('content-area'),
            dynamicContentWrapper: document.getElementById('dynamic-content-wrapper'),
            sidebar: document.getElementById('sidebar'),
            apiKeyBtn: document.getElementById('btn-gravar-api-key'), // << ALTERADO
            resetProjectBtn: document.getElementById('reset-project'),
            loadProposalGeneratorLink: document.getElementById('load-proposal-generator'),
            stepLinks: document.querySelectorAll('.step-link'),
        };
    },

    bindEventListeners() {
        // Header
        this.elements.apiKeyBtn.addEventListener('click', () => this.apiKeyModal.open()); // << ALTERADO
        this.elements.resetProjectBtn.addEventListener('click', () => this.resetProject());

        // Sidebar Links
        this.elements.loadProposalGeneratorLink.addEventListener('click', (e) => {
            e.preventDefault();
            this.loadContent('/proposal_generator', 'Gerador de Propostas'); // CORRIGIDO: URL direta para a rota
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
            const button = e.target.closest('button');
            if (!button) return;

            const action = button.dataset.action || button.id;
            
            // Only prevent default for specific actions we handle
            if ([ 'approve', 'repeat', 'back', 'start', 'generateEstimateBtn', 'addFeatureBtn', 'remove-feature', 'generatePdfBtn' ].includes(action)) {
                e.preventDefault();
            }

            switch(action) {
                case 'approve':
                case 'repeat':
                case 'back':
                case 'start':
                    this.performAction(action);
                    break;
                case 'generateEstimateBtn':
                    this.proposalGenerator.handleAIEstimate();
                    break;
                case 'addFeatureBtn':
                    this.proposalGenerator.addFeatureInput();
                    break;
                case 'remove-feature':
                    this.proposalGenerator.removeFeature(button);
                    break;
                case 'generatePdfBtn':
                    this.proposalGenerator.handlePDFGeneration();
                    break;
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
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            const data = await response.json();
            this.updateUI(data);
        } catch (error) {
            console.error("Error fetching project status:", error);
        }
    },

    async performAction(action) {
        // ... (implementation is correct)
    },

    async loadContent(url, contentName) {
        const target = this.elements.dynamicContentWrapper;
        target.innerHTML = `<p class="text-center">Carregando ${contentName}...</p>`;
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Network response was not ok. Status: ${response.status}`);
            
            const html = await response.text();
            target.innerHTML = html;
            
            if (url.includes('proposal_generator')) {
                this.proposalGenerator.init();
            }

            this.checkProjectStatus();

        } catch (error) {
            console.error(`Error loading content from ${url}:`, error);
            target.innerHTML = `<p class="text-center text-red-500">Erro ao carregar o conteúdo. Detalhes: ${error.message}</p>`;
        }
    },

    resetProject() {
        // ... (implementation is correct)
    },

    // ---------------------------------------------------------------------------
    // 4. UI UPDATES
    // ---------------------------------------------------------------------------
    updateUI(data) {
        // ... (implementation is correct)
    },

    updateSidebar() {
        // ... (implementation is correct)
    },

    updateDynamicContent(data) {
        // ... (implementation is correct)
    },

    // ---------------------------------------------------------------------------
    // 5. PROPOSAL GENERATOR LOGIC
    // ---------------------------------------------------------------------------
    proposalGenerator: {
        fullProposalData: null,

        init() {
            console.log("Proposal Generator Initialized.");
            // The main event listeners are already handled by event delegation.
        },

        async handleAIEstimate() {
            const description = document.getElementById('projectDescription')?.value;
            const aiResultDiv = document.getElementById('aiResult');
            const button = document.getElementById('generateEstimateBtn');

            if (!description || !description.trim()) {
                aiResultDiv.innerHTML = `<p class="text-red-400 text-center">Por favor, descreva seu projeto para gerar uma estimativa.</p>`;
                return;
            }

            button.disabled = true;
            aiResultDiv.innerHTML = '<div class="loader"></div><p class="text-center text-gray-400">Analisando sua ideia... Isso pode levar alguns segundos.</p>';

            try {
                const response = await fetch('/api/gerar-estimativa', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ description: description })
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({ error: `API Error: ${response.statusText}` }));
                    throw new Error(errorData.error);
                }

                this.fullProposalData = await response.json();
                this.populateForm(this.fullProposalData.dados_orcamento);

                aiResultDiv.innerHTML = `<p class="text-green-400 text-center font-semibold">Estimativa base gerada! Role para baixo e refine os detalhes.</p>`;
                document.getElementById('step-form')?.classList.remove('hidden');
                document.getElementById('step-pdf')?.classList.remove('hidden');

            } catch (error) {
                console.error("Error calling backend API:", error);
                aiResultDiv.innerHTML = `<p class="text-red-400 text-center">Ocorreu um erro: ${error.message}. Verifique a chave de API e tente novamente.</p>`;
            } finally {
                button.disabled = false;
            }
        },

        populateForm(data) {
            if (!data) return;
            document.getElementById('projectName').value = data.projectName || '';
            document.getElementById('teamComposition').value = data.suggestedTeam || '';
            document.getElementById('timeline').value = data.estimatedTimelineMonths || 3;
            document.getElementById('devCost').value = data.estimatedMonthlyTeamCost || 50000;
            
            const featuresContainer = document.getElementById('coreFeaturesContainer');
            featuresContainer.innerHTML = '';
            if (data.coreFeatures && data.coreFeatures.length > 0) {
                data.coreFeatures.forEach(feature => this.addFeatureInput(feature));
            } else {
                this.addFeatureInput('');
            }
        },

        addFeatureInput(value = '') {
            const container = document.getElementById('coreFeaturesContainer');
            if (!container) return;
            const div = document.createElement('div');
            div.className = 'flex items-center gap-2';
            div.innerHTML = `
                <input type="text" class="form-input feature-input" value="${value}" placeholder="Descreva uma funcionalidade">
                <button type="button" class="text-red-500 hover:text-red-700 font-bold p-2 rounded-full" data-action="remove-feature">&#x2715;</button>
            `;
            container.appendChild(div);
        },

        removeFeature(button) {
            button.closest('.flex.items-center.gap-2').remove();
        },

        handlePDFGeneration() {
            if (!this.fullProposalData) {
                alert("Por favor, gere uma estimativa com a IA primeiro.");
                return;
            }
            
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            const introText = this.fullProposalData.texto_introducao || 'Introdução não gerada.';
            const iaParams = this.fullProposalData.parametros_ia || {};
            const formatCurrency = (value) => `R$ ${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

            const clientName = document.getElementById('clientName').value || 'N/A';
            const projectName = document.getElementById('projectName').value || 'N/A';
            const preparedBy = document.getElementById('preparedBy').value || 'N/A';
            const team = document.getElementById('teamComposition').value || 'A definir';
            const timeline = parseInt(document.getElementById('timeline').value) || 0;
            const monthlyCost = parseFloat(document.getElementById('devCost').value) || 0;
            const indirectCosts = parseFloat(document.getElementById('indirectCosts').value) || 0;
            const taxesPercent = parseFloat(document.getElementById('taxes').value) || 0;
            const profitMarginPercent = parseFloat(document.getElementById('profitMargin').value) || 0;
            const features = Array.from(document.querySelectorAll('.feature-input')).map(input => input.value).filter(val => val.trim() !== '');

            const devTotal = monthlyCost * timeline;
            const subtotal = devTotal + indirectCosts;
            const taxValue = subtotal * (taxesPercent / 100);
            const profitValue = subtotal * (profitMarginPercent / 100);
            const grandTotal = subtotal + taxValue + profitValue;

            let currentY = 15;
            doc.setFontSize(22);
            doc.setFont('helvetica', 'bold');
            doc.setTextColor('#0077B6');
            doc.text('Proposta de Orçamento de Software', 105, currentY + 10, { align: 'center' });
            currentY += 30;

            doc.setFontSize(11);
            doc.setFont('helvetica', 'normal');
            doc.setTextColor(40);
            doc.text(`Projeto: ${projectName}`, 20, currentY);
            doc.text(`Cliente: ${clientName}`, 20, currentY + 7);
            doc.text(`Preparado por: ${preparedBy}`, 20, currentY + 14);
            doc.text(`Data: ${new Date().toLocaleDateString('pt-BR')}`, 190, currentY + 14, { align: 'right' });
            currentY += 25;

            doc.autoTable({
                startY: currentY,
                head: [['Detalhes do Projeto', '']],
                body: [
                    ['Composição da Equipe', team],
                    ['Cronograma Estimado', `${timeline} meses`]
                ],
                theme: 'grid',
                headStyles: { fillColor: '#0077B6' }
            });
            currentY = doc.lastAutoTable.finalY + 10;

            doc.autoTable({
                startY: currentY,
                head: [['Escopo do Projeto (Funcionalidades Principais)']],
                body: features.length > 0 ? features.map(f => [f]) : [['Nenhuma funcionalidade definida']],
                theme: 'grid',
                headStyles: { fillColor: '#0077B6' }
            });
            currentY = doc.lastAutoTable.finalY + 10;

            doc.autoTable({
                startY: currentY,
                head: [['Item do Orçamento', 'Valor']],
                body: [
                    ['Custo de Desenvolvimento', formatCurrency(devTotal)],
                    ['Custos Indiretos', formatCurrency(indirectCosts)],
                    ['Subtotal', formatCurrency(subtotal)],
                    ['Impostos', formatCurrency(taxValue)],
                    ['Margem de Lucro', formatCurrency(profitValue)],
                    ['Valor Total do Projeto', formatCurrency(grandTotal)]
                ],
                theme: 'grid',
                headStyles: { fillColor: '#03254C' },
                styles: { fontStyle: 'bold' },
                columnStyles: { 1: { halign: 'right' } }
            });

            doc.save(`Proposta_${projectName.replace(/\s/g, '_')}.pdf`);
        }
    },

    // ---------------------------------------------------------------------------
    // 6. API KEY MODAL LOGIC (REBUILT)
    // ---------------------------------------------------------------------------
    apiKeyModal: {
        elements: {},
        init() {
            this.elements = {
                modal: document.getElementById('api-key-modal'),
                closeBtn: document.getElementById('close-api-key-modal'),
                statusDiv: document.getElementById('api-key-status'),
                providerSelect: document.getElementById('api-provider-select'),
                keyInput: document.getElementById('api-key-input'),
                toggleVisibilityBtn: document.getElementById('toggle-api-key-visibility'),
                eyeIcon: document.getElementById('eye-icon'),
                eyeOffIcon: document.getElementById('eye-off-icon'),
                messageDiv: document.getElementById('api-key-message'),
                testBtn: document.getElementById('test-api-key'),
                saveBtn: document.getElementById('save-api-key-action'),
                removeBtn: document.getElementById('remove-api-key'),
            };
            this.bindEvents();
        },

        bindEvents() {
            this.elements.closeBtn.addEventListener('click', () => this.close());
            this.elements.toggleVisibilityBtn.addEventListener('click', () => this.toggleVisibility());
            this.elements.saveBtn.addEventListener('click', () => this.saveKey());
            this.elements.testBtn.addEventListener('click', () => this.testKey());
            this.elements.removeBtn.addEventListener('click', () => this.removeKey());
        },

        open() {
            this.elements.modal.classList.remove('hidden');
            this.checkStatus();
        },

        close() {
            this.elements.modal.classList.add('hidden');
            this.clearMessage();
        },

        toggleVisibility() {
            const isPassword = this.elements.keyInput.type === 'password';
            this.elements.keyInput.type = isPassword ? 'text' : 'password';
            this.elements.eyeIcon.classList.toggle('hidden', isPassword);
            this.elements.eyeOffIcon.classList.toggle('hidden', !isPassword);
        },

        async checkStatus() {
            try {
                const response = await fetch('/api/keys/list');
                const data = await response.json();
                if (data.keys && data.keys.length > 0) {
                    const key = data.keys[0];
                    this.elements.statusDiv.innerHTML = `<p class="text-green-400">API Key para <strong>${key.provider}</strong> está configurada.</p>`;
                } else {
                    this.elements.statusDiv.innerHTML = `<p class="text-yellow-400">Nenhuma API Key configurada.</p>`;
                }
            } catch (error) {
                this.elements.statusDiv.innerHTML = `<p class="text-red-500">Erro ao verificar status da chave.</p>`;
                console.error("Error checking key status:", error);
            }
        },

        async saveKey() {
            const provider = this.elements.providerSelect.value;
            const apiKey = this.elements.keyInput.value;

            if (!apiKey.trim()) {
                this.showMessage('Por favor, insira uma API Key.', 'error');
                return;
            }

            try {
                const response = await fetch('/api/keys/save', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ provider, api_key: apiKey })
                });
                const data = await response.json();
                if (response.ok) {
                    this.showMessage(data.message, 'success');
                    this.checkStatus();
                    ArchonDashboard.checkApiKeyStatus(); // Atualiza o botão do header
                } else {
                    throw new Error(data.error || 'Erro desconhecido');
                }
            } catch (error) {
                this.showMessage(`Falha ao salvar: ${error.message}`, 'error');
            }
        },

        async testKey() {
            const apiKey = this.elements.keyInput.value;
            if (!apiKey.trim()) {
                this.showMessage('Insira uma chave no campo para testar.', 'error');
                return;
            }

            this.showMessage('Testando... Isso pode levar um momento.', 'loading');

            try {
                const response = await fetch('/api/keys/test', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ api_key: apiKey })
                });
                const data = await response.json();
                if (data.success) {
                    this.showMessage(data.message, 'success');
                } else {
                    throw new Error(data.message || 'Falha no teste');
                }
            } catch (error) {
                this.showMessage(`Erro no teste: ${error.message}`, 'error');
            }
        },

        async removeKey() {
            const provider = this.elements.providerSelect.value;
            if (!confirm(`Tem certeza que deseja remover a chave da API para ${provider}?`)) {
                return;
            }

            try {
                const response = await fetch('/api/keys/remove', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ provider })
                });
                const data = await response.json();
                if (response.ok) {
                    this.showMessage(data.message, 'success');
                    this.elements.keyInput.value = '';
                    this.checkStatus();
                    ArchonDashboard.checkApiKeyStatus(); // Atualiza o botão do header
                } else {
                    throw new Error(data.error || 'Erro desconhecido');
                }
            } catch (error) {
                this.showMessage(`Falha ao remover: ${error.message}`, 'error');
            }
        },

        showMessage(message, type = 'info') {
            this.elements.messageDiv.textContent = message;
            this.elements.messageDiv.className = 'text-sm text-center h-5'; // Reset classes
            switch (type) {
                case 'success': this.elements.messageDiv.classList.add('text-green-400'); break;
                case 'error': this.elements.messageDiv.classList.add('text-red-500'); break;
                case 'loading': this.elements.messageDiv.classList.add('text-blue-400'); break;
                default: this.elements.messageDiv.classList.add('text-gray-400');
            }
        },

        clearMessage() {
            this.elements.messageDiv.textContent = '';
        }
    },

    // ---------------------------------------------------------------------------
    // 7. API KEY STATUS CHECK (NOVO)
    // ---------------------------------------------------------------------------
    async checkApiKeyStatus() {
        try {
            const response = await fetch('/api/keys/status');
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            const apiKeyBtn = this.elements.apiKeyBtn;

            if (data.has_key) {
                apiKeyBtn.classList.remove('blinking-alert');
            } else {
                apiKeyBtn.classList.add('blinking-alert');
            }
        } catch (error) {
            console.error("Error checking API key status:", error);
            // Mantém o estado visual de erro, se ocorrer
            const apiKeyBtn = this.elements.apiKeyBtn;
            if(apiKeyBtn) {
                apiKeyBtn.classList.add('bg-red-700');
            }
        }
    }
};

// Initialize the application
ArchonDashboard.init();
