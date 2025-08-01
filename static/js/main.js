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
        selectedSystemType: null, // NEW: To store the selected system type (SaaS, MicroSaaS, etc.)
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
            this.archiveProjectModal.init(); // INICIALIZA O NOVO MODAL
            this.checkProjectStatus();
            this.checkApiKeyStatus();
            this.startPolling();
            console.log("ArchonDashboard Initialized and Connected.");
        });
    },

    cacheDomElements() {
        this.elements = {
            contentArea: document.getElementById('content-area'),
            dynamicContentWrapper: document.getElementById('dynamic-content-wrapper'),
            sidebar: document.getElementById('sidebar'),
            apiKeyBtn: document.getElementById('btn-gravar-api-key'),
            resetProjectBtn: document.getElementById('download-reset-project'), // O botão que abre o modal
            loadProposalGeneratorLink: document.getElementById('load-proposal-generator'),
            stepLinks: document.querySelectorAll('.step-link'),
        };
    },

    bindEventListeners() {
        // Header
        this.elements.apiKeyBtn.addEventListener('click', () => this.apiKeyModal.open());
        // Ação do botão de reset agora abre o modal
        this.elements.resetProjectBtn.addEventListener('click', () => this.archiveProjectModal.open());

        // Sidebar Links
        this.elements.loadProposalGeneratorLink.addEventListener('click', (e) => {
            e.preventDefault();
            this.loadContent('/proposal_generator', 'Gerador de Propostas');
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
            
            if ([ 'approve', 'repeat', 'back', 'start', 'next_step', 'prev_step', 'generateEstimateBtn', 'addFeatureBtn', 'remove-feature', 'generatePdfBtn' ].includes(action)) {
                e.preventDefault();
            }

            switch(action) {
                case 'next_step':
                case 'prev_step':
                    this.navigateStep(action);
                    break;
                case 'approve':
                case 'repeat':
                case 'back':
                case 'start':
                    // Ações da FSM agora usam a nova função performSupervisorAction
                    this.performSupervisorAction(action);
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
                case 'generate_knowledge_base':
                    console.log("DEBUG: Botão 'Gerar Documentos' clicado. Chamando handleGeneration.");
                    this.knowledgeBaseGenerator.handleGeneration();
                    break;
                case 'run-agent-btn':
                    this.handleStructureAgent();
                    break;
            }
        });
    },

    async handleStructureAgent() {
        const taskInput = document.getElementById('agent-task-input');
        const runBtn = document.getElementById('run-agent-btn');
        
        if (!taskInput || !runBtn) return;

        if (!taskInput.value.trim()) {
            alert('Por favor, descreva sua ideia de projeto.');
            return;
        }

        runBtn.disabled = true;
        runBtn.textContent = 'Processando...';

        try {
            // Step 1: Get the structured text from the agent
            const response = await fetch('/structure-idea', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task_description: taskInput.value })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ error: `API Error: ${response.statusText}` }));
                throw new Error(errorData.error || 'Falha ao comunicar com o agente de estruturação.');
            }
            const data = await response.json();
            const structuredText = data.structured_text;

            // Step 2: Load the proposal generator view
            await this.loadContent('/proposal_generator', 'Gerador de Propostas');
            
            // Step 3: Now that the content is loaded, populate the textarea
            // We need to wait a tick for the DOM to update after loadContent
            setTimeout(() => {
                const proposalTextarea = document.getElementById('projectDescription');
                const stepAiCard = document.getElementById('step-ai'); // Adicionado: Referência ao card da Etapa 1

                if (proposalTextarea) {
                    proposalTextarea.value = structuredText;
                    
                    // Adicionado: Remover a classe 'hidden' do card da Etapa 1
                    if (stepAiCard) {
                        stepAiCard.classList.remove('hidden');
                    }

                    // Scroll to the element to make it visible
                    proposalTextarea.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    proposalTextarea.focus();
                    // Flash a highlight on the textarea
                    proposalTextarea.classList.add('ring-2', 'ring-emerald-500', 'transition-all', 'duration-500');
                    setTimeout(() => {
                        proposalTextarea.classList.remove('ring-2', 'ring-emerald-500');
                    }, 2000);
                } else {
                     // Se o gerador de propostas não estiver carregado, apenas mostramos o resultado.
                     alert('Não foi possível encontrar o campo de descrição da proposta após o carregamento. Verifique o console para o texto estruturado.');
                     console.log("Texto Estruturado:", structuredText);
                }
            }, 100); // 100ms delay to ensure DOM is ready

        } catch (error) {
            console.error("Error in structure agent workflow:", error);
            alert(`Ocorreu um erro: ${error.message}`);
        } finally {
            runBtn.disabled = false;
            runBtn.textContent = 'Executar Agente';
        }
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

    async performSupervisorAction(action, payload = {}) {
        console.log(`Performing supervisor action: ${action} with payload:`, payload);
        try {
            const body = { action, ...payload };
            const response = await fetch('/api/supervisor/action', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ error: `HTTP error! Status: ${response.status}` }));
                throw new Error(errorData.error || 'Unknown server error');
            }

            const data = await response.json();
            this.updateUI(data);
            return data;
        } catch (error) {
            console.error(`Error performing action ${action}:`, error);
            alert(`An error occurred: ${error.message}`);
        }
    },

    // --- MODAL DE ARQUIVAMENTO (LÓGICA REFEITA) ---
    archiveProjectModal: {
        elements: {},
        init() {
            this.elements = {
                modal: document.getElementById('archive-project-modal'),
                closeBtn: document.getElementById('close-archive-modal'),
                cancelBtn: document.getElementById('cancel-archive-btn'),
                confirmBtn: document.getElementById('confirm-archive-btn'),
                messageDiv: document.getElementById('archive-message'),
                listContainer: document.getElementById('project-list-container'),
            };
            this.bindEvents();
        },

        bindEvents() {
            this.elements.closeBtn.addEventListener('click', () => this.close());
            this.elements.cancelBtn.addEventListener('click', () => this.close());
            this.elements.confirmBtn.addEventListener('click', () => this.handleConfirm());
        },

        async open() {
            this.showMessage('Carregando lista de projetos...', 'loading');
            this.elements.modal.classList.remove('hidden');
            this.elements.confirmBtn.disabled = true;

            try {
                const response = await fetch('/api/supervisor/list_projects');
                if (!response.ok) throw new Error('Falha ao buscar projetos.');
                const data = await response.json();

                if (data.projects && data.projects.length > 0) {
                    this.populateList(data.projects);
                    this.showMessage('Selecione um projeto para arquivar.', 'info');
                } else {
                    this.elements.listContainer.innerHTML = '<p class="text-center text-gray-400">Nenhum projeto ativo encontrado para arquivar.</p>';
                    this.showMessage('Nenhum projeto para arquivar.', 'info');
                }
            } catch (error) {
                console.error("Error fetching project list:", error);
                this.showMessage(error.message, 'error');
            }
        },

        populateList(projects) {
            this.elements.listContainer.innerHTML = projects.map(p => `
                <label class="block w-full p-3 rounded-md bg-gray-700 hover:bg-gray-600 cursor-pointer">
                    <input type="radio" name="project_to_archive" value="${p}" class="mr-3">
                    <span class="font-mono">${p}</span>
                </label>
            `).join('');
            
            // Habilita o botão de confirmação quando uma opção é selecionada
            this.elements.listContainer.addEventListener('change', () => {
                this.elements.confirmBtn.disabled = false;
            });
        },

        async handleConfirm() {
            const selectedProject = this.elements.listContainer.querySelector('input[name="project_to_archive"]:checked');
            if (!selectedProject) {
                this.showMessage('Por favor, selecione um projeto.', 'error');
                return;
            }

            const projectName = selectedProject.value;
            
            this.showMessage(`Preparando download e reset de '${projectName}'...`, 'loading');
            this.elements.confirmBtn.disabled = true;

            try {
                const response = await fetch('/api/supervisor/download_and_reset_project', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ project_name: projectName }),
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({ error: `HTTP error! Status: ${response.status}` }));
                    throw new Error(errorData.error || 'Falha ao iniciar o processo.');
                }

                const blob = await response.blob();
                
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = `${projectName}.zip`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);

                this.showMessage('Processo concluído! O download foi iniciado e o projeto foi resetado.', 'success');
                
                setTimeout(() => {
                    this.close();
                    window.location.reload();
                }, 2000);

            } catch (error) {
                console.error(`Erro no processo de download/reset:`, error);
                this.showMessage(`Erro: ${error.message}`, 'error');
                this.elements.confirmBtn.disabled = false;
            }
        },

        close() {
            this.elements.modal.classList.add('hidden');
            this.elements.listContainer.innerHTML = '';
            this.showMessage('', 'info');
        },

        showMessage(message, type = 'info') {
            this.elements.messageDiv.textContent = message;
            this.elements.messageDiv.className = 'text-sm text-center h-5'; // Reset
            switch (type) {
                case 'success': this.elements.messageDiv.classList.add('text-green-400'); break;
                case 'error': this.elements.messageDiv.classList.add('text-red-500'); break;
                case 'loading': this.elements.messageDiv.classList.add('text-blue-400'); break;
                default: this.elements.messageDiv.classList.add('text-gray-400');
            }
        }
    },

    navigateStep(direction) {
        let currentStep = this.state.currentStep;

        if (direction === 'next_step') {
            if (currentStep === 2) {
                currentStep = 4; // Pula a etapa 3
            } else if (currentStep < 7) {
                currentStep++;
            }
        } else if (direction === 'prev_step') {
            if (currentStep === 4) {
                currentStep = 2; // Pula a etapa 3
            } else if (currentStep > 1) {
                currentStep--;
            }
        }

        this.state.currentStep = currentStep;
        const stepLink = document.querySelector(`.step-link[data-step="${currentStep}"]`);
        if (stepLink) {
            const stepName = stepLink.dataset.name;
            this.loadContent(`/api/get_step_template/${currentStep}`, stepName);
        } else {
            console.error(`Link da barra lateral para a etapa ${currentStep} não foi encontrado.`);
        }
    },

    async loadContent(url, contentName) {
        // Extrai o número da etapa da URL, se for uma página de etapa
        const stepMatch = url.match(/\/api\/get_step_template\/(\d+)/);
        if (stepMatch && stepMatch[1]) {
            this.state.currentStep = parseInt(stepMatch[1], 10);
        }

        const target = this.elements.dynamicContentWrapper;
        target.innerHTML = `<p class="text-center">Carregando ${contentName}...</p>`;
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Network response was not ok. Status: ${response.status}`);
            
            const html = await response.text();
            target.innerHTML = html;

            // [GEMINI-FIX] Executa scripts que são injetados dinamicamente via innerHTML.
            const scriptTag = target.querySelector("script");
            if (scriptTag) {
                const newScript = document.createElement("script");
                newScript.textContent = scriptTag.textContent;
                document.body.appendChild(newScript).remove(); // Adiciona o script ao corpo para execução e o remove em seguida.
            }
            
            if (url.includes('proposal_generator')) {
                this.proposalGenerator.init();
            } else if (stepMatch) {
                // Se carregamos uma etapa, atualizamos o destaque da sidebar
                this.updateSidebarHighlighting();
                // NEW: Initialize systemTypeSelector if step 2 is loaded
                if (parseInt(stepMatch[1], 10) === 2) {
                    this.systemTypeSelector.init();
                }
            }

            this.checkProjectStatus();

        } catch (error) {
            console.error(`Error loading content from ${url}:`, error);
            target.innerHTML = `<p class="text-center text-red-500">Erro ao carregar o conteúdo. Detalhes: ${error.message}</p>`;
        }
    },

    

    // ---------------------------------------------------------------------------
    // 4. UI UPDATES
    // ---------------------------------------------------------------------------
    updateUI(data) {
        if (data.project_name) {
            this.state.projectName = data.project_name;
            console.log(`Project Name updated to: ${this.state.projectName}`);
        }
        // Adicione outras lógicas de atualização de UI aqui, se necessário
    },

    updateSidebar() {
        // ... (implementation is correct)
    },

    updateDynamicContent(data) {
        // ... (implementation is correct)
    },

    updateSidebarHighlighting() {
        this.elements.stepLinks.forEach(link => {
            link.classList.remove('active-step');
            if (parseInt(link.dataset.step, 10) === this.state.currentStep) {
                link.classList.add('active-step');
            }
        });
    },

    // ---------------------------------------------------------------------------
    // 5. PROPOSAL GENERATOR LOGIC
    // ---------------------------------------------------------------------------
    proposalGenerator: {

    },

    // ---------------------------------------------------------------------------
    // 6. KNOWLEDGE BASE GENERATOR LOGIC (STEP 1)
    // ---------------------------------------------------------------------------
    knowledgeBaseGenerator: {
        init() {
            console.log("Knowledge Base Generator Initialized.");
            const uploadInput = document.getElementById("context-documents-upload");
            const filesListDiv = document.getElementById("uploaded-files-list");

            if (uploadInput) {
                uploadInput.addEventListener("change", function () {
                    filesListDiv.innerHTML = ""; // Limpa a lista anterior
                    if (uploadInput.files.length > 0) {
                        const title = document.createElement("p");
                        title.textContent = "Arquivos selecionados:";
                        title.className = "font-semibold";
                        filesListDiv.appendChild(title);

                        for (const file of uploadInput.files) {
                            const fileItem = document.createElement("p");
                            fileItem.textContent = `- ${file.name}`;
                            filesListDiv.appendChild(fileItem);
                        }
                    }
                });
            }
        },

        async handleGeneration() {
            const projectNameInput = document.getElementById("project-name");
            const projectDescriptionTextarea = document.getElementById("project-description");
            const messageDiv = document.getElementById("generation-message");
            const generateBtn = document.getElementById("generate-knowledge-base-btn");
            const uploadInput = document.getElementById("context-documents-upload");

            const projectName = projectNameInput?.value.trim();
            const projectDescription = projectDescriptionTextarea?.value.trim();
            const selectedSystemType = ArchonDashboard.state.selectedSystemType; // NEW: Get selected system type

            if (!projectName) {
                messageDiv.textContent =
                    "Erro: O nome do projeto é obrigatório.";
                messageDiv.className = "text-red-500";
                projectNameInput.focus();
                return;
            }

            if (!projectDescription) {
                messageDiv.textContent = "Por favor, descreva o projeto.";
                messageDiv.className = "text-yellow-500";
                return;
            }

            messageDiv.textContent =
                "Gerando base de conhecimento... Isso pode levar alguns minutos.";
            messageDiv.className = "text-blue-400";
            generateBtn.disabled = true;

            const formData = new FormData();
            formData.append("project_name", projectName);
            formData.append("project_description", projectDescription);

            // Adiciona os arquivos de contexto ao FormData
            for (const file of uploadInput.files) {
                formData.append("files", file);
            }

            try {
                const response = await fetch("/api/setup/generate_project_base", { // Rota corrigida
                    method: "POST",
                    body: formData,
                });

                const result = await response.json();

                if (response.ok) {
                    messageDiv.textContent = result.message;
                    messageDiv.className = "text-green-500";
                    // Atualiza o status geral do dashboard para refletir a conclusão da etapa
                    ArchonDashboard.checkProjectStatus();
                } else {
                    messageDiv.textContent = `Erro: ${result.error}`;
                    messageDiv.className = "text-red-500";
                }
            } catch (error) {
                messageDiv.textContent = `Erro de rede: ${error.message}`;
                messageDiv.className = "text-red-500";
            } finally {
                generateBtn.disabled = false;
            }
        }
    },

    // ---------------------------------------------------------------------------
    // 9. SYSTEM TYPE SELECTOR LOGIC (STEP 2)
    // ---------------------------------------------------------------------------
    systemTypeSelector: {
        init() {
            console.log("System Type Selector Initialized.");
            const systemTypeButtons = document.querySelectorAll('.system-type-btn');
            systemTypeButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    const selectedType = e.currentTarget.dataset.systemType;
                    ArchonDashboard.systemTypeSelector.selectSystemType(selectedType);
                });
            });
            // Restore selection if already in state
            if (ArchonDashboard.state.selectedSystemType) {
                this.highlightSelectedButton(ArchonDashboard.state.selectedSystemType);
            }
        },

        selectSystemType(type) {
            ArchonDashboard.state.selectedSystemType = type;
            this.highlightSelectedButton(type);
            console.log(`System Type Selected: ${type}`);
        },

        highlightSelectedButton(selectedType) {
            const systemTypeButtons = document.querySelectorAll('.system-type-btn');
            systemTypeButtons.forEach(button => {
                if (button.dataset.systemType === selectedType) {
                    button.classList.add('ring-2', 'ring-offset-2', 'ring-blue-500'); // Add highlight
                } else {
                    button.classList.remove('ring-2', 'ring-offset-2', 'ring-blue-500'); // Remove highlight
                }
            });
        }
    },

    // ---------------------------------------------------------------------------
    // 7. API KEY MODAL LOGIC (REBUILT)
    // ---------------------------------------------------------------------------
    apiKeyModal: {

    },

    // ---------------------------------------------------------------------------
    // 8. PROPOSAL GENERATOR LOGIC
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

        async handlePDFGeneration() {
            if (!this.fullProposalData) {
                alert("Por favor, gere uma estimativa com a IA primeiro.");
                return;
            }

            // --- 1. SETUP & CONFIGURATION ---
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF({ orientation: 'p', unit: 'mm', format: 'a4' });

            // --- Helper para converter imagem para Base64 ---
            const getBase64Image = async (url) => {
                const response = await fetch(url);
                const blob = await response.blob();
                return new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.onloadend = () => resolve(reader.result);
                    reader.onerror = reject;
                    reader.readAsDataURL(blob);
                });
            };

            // --- Estilos e Cores ---
            const COLORS = {
                primary: '#0077B6', // Azul principal
                secondary: '#03254C', // Azul escuro para totais
                text: '#212529',      // Texto principal (quase preto)
                lightText: '#6c757d', // Texto cinza claro
                headerFill: '#00AEEF' // Azul mais claro para cabeçalhos de tabela
            };

            const FONT_SIZES = {
                title: 20,
                subtitle: 14,
                h1: 12,
                body: 10,
                small: 8
            };

            let currentY = 0;
            const pageMargin = 15;
            const pageWidth = doc.internal.pageSize.getWidth();

            // --- Helper para renderizar texto com Markdown Básico ---
            const renderMarkdownText = (text, initialY) => {
                let y = initialY;
                const lines = text.split('\n');

                lines.forEach(line => {
                    if (y > 270) { // Margem inferior para evitar sobreposição com o footer
                        doc.addPage();
                        addHeader();
                        y = 40; // Reinicia Y na nova página
                    }

                    let style = 'normal';
                    let size = FONT_SIZES.body;
                    let leftMargin = pageMargin;
                    let processedLine = line.trim();

                    // Limpa toda a sintaxe de formatação para obter o texto puro
                    const cleanText = processedLine.replace(/^[#*\-]+\s*/, '').replace(/\*\*/g, '');

                    if (processedLine.startsWith('# ')) {
                        style = 'bold';
                        size = FONT_SIZES.subtitle;
                        y += 4; // Espaço extra antes de um título principal
                    } else if (processedLine.startsWith('##')) {
                        style = 'bold';
                        size = FONT_SIZES.h1;
                        y += 3; // Espaço extra antes de um subtítulo
                    } else if (processedLine.startsWith('*') || processedLine.startsWith('-')) {
                        leftMargin += 5; // Indentação para itens de lista
                        processedLine = `• ${cleanText}`;
                    } else {
                        processedLine = cleanText;
                    }

                    doc.setFont('helvetica', style);
                    doc.setFontSize(size);

                    const splitText = doc.splitTextToSize(processedLine, pageWidth - leftMargin - pageMargin);
                    doc.text(splitText, leftMargin, y);
                    y += (splitText.length * 5) + 3; // Ajusta o espaçamento entre linhas
                });
                return y;
            };

            // --- 2. ASSETS & DATA ---
            const logoBase64 = await getBase64Image('/static/assets/5logo_Archon.png');
            const introText = this.fullProposalData.texto_introducao || 'Introdução não gerada.';
            const iaParams = this.fullProposalData.parametros_ia || {};
            const formatCurrency = (value) => `R$ ${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

            // --- Coleta de dados do formulário ---
            const clientName = document.getElementById('clientName').value || 'N/A';
            const projectName = document.getElementById('projectName').value || 'N/A';
            const preparedBy = document.getElementById('preparedBy').value || 'N/A';
            const team = document.getElementById('teamComposition').value || 'A definir';
            const timeline = parseInt(document.getElementById('timeline').value) || 0;
            const monthlyCost = parseFloat(document.getElementById('devCost').value) || 0;
            const monthlyFees = parseFloat(document.getElementById('indirectCosts').value) || 0; // Renomeado de indirectCosts
            const taxesPercent = parseFloat(document.getElementById('taxes').value) || 0;
            const profitMarginPercent = parseFloat(document.getElementById('profitMargin').value) || 0;
            const features = Array.from(document.querySelectorAll('.feature-input')).map(input => input.value).filter(val => val.trim() !== '');

            // --- Cálculos Financeiros CORRIGIDOS ---
            const devTotal = monthlyCost * timeline;
            const feesTotal = monthlyFees * timeline; // Custo total das mensalidades
            const subtotal = devTotal + feesTotal;
            const taxValue = subtotal * (taxesPercent / 100);
            const profitValue = subtotal * (profitMarginPercent / 100);
            const grandTotal = subtotal + taxValue + profitValue;

            // --- 3. HEADER & FOOTER ---
            const addHeader = () => {
                doc.addImage(logoBase64, 'PNG', pageMargin, 10, 30, 15); // Logo
                doc.setFont('helvetica', 'bold');
                doc.setFontSize(FONT_SIZES.title);
                doc.setTextColor(COLORS.primary);
                doc.text('Proposta de Software', pageWidth - pageMargin, 20, { align: 'right' });
            };

            const addFooter = () => {
                const pageCount = doc.internal.getNumberOfPages();
                doc.setFontSize(FONT_SIZES.small);
                doc.setTextColor(COLORS.lightText);
                doc.text(`Página ${doc.internal.getCurrentPageInfo().pageNumber} de ${pageCount}`, pageWidth / 2, 285, { align: 'center' });
                doc.text('Archon AI - Inovação e Tecnologia', pageMargin, 285);
                doc.text('Proposta válida por 30 dias.', pageWidth - pageMargin, 285, { align: 'right' });
            };

            // --- 4. PDF CONTENT GENERATION ---
            addHeader();
            currentY = 40;

            // --- Bloco de Informações Gerais ---
            doc.setFontSize(FONT_SIZES.body);
            doc.setTextColor(COLORS.text);
            doc.text(`Projeto: ${projectName}`, pageMargin, currentY);
            doc.text(`Cliente: ${clientName}`, pageMargin, currentY + 7);
            doc.text(`Preparado por: ${preparedBy}`, pageMargin, currentY + 14);
            doc.text(`Data: ${new Date().toLocaleDateString('pt-BR')}`, pageWidth - pageMargin, currentY + 14, { align: 'right' });
            currentY += 25;

            // --- Introdução da IA ---
            doc.setFont('helvetica', 'bold');
            doc.setFontSize(FONT_SIZES.h1);
            doc.setTextColor(COLORS.primary);
            doc.text('1. Introdução e Visão Geral', pageMargin, currentY);
            currentY += 8;
            doc.setTextColor(COLORS.text);
            currentY = renderMarkdownText(introText, currentY); // USA A NOVA FUNÇÃO
            currentY += 5; // Espaçamento extra após a seção de introdução

            // --- Tabela de Entendimento do Projeto ---
            doc.setFont('helvetica', 'bold');
            doc.setFontSize(FONT_SIZES.h1);
            doc.setTextColor(COLORS.primary);
            doc.text('2. Entendimento do Projeto (Análise da IA)', pageMargin, currentY);
            currentY += 8;

            const projectUnderstandingBody = [];
            const addSection = (title, items, nameKey, descKey) => {
                if (items && items.length > 0) {
                    projectUnderstandingBody.push([{ content: title, colSpan: 2, styles: { halign: 'center', fontStyle: 'bold', fillColor: '#eaf2f8', textColor: COLORS.primary } }]);
                    items.forEach(p => projectUnderstandingBody.push([p[nameKey], p[descKey]]));
                }
            };
            addSection('Personas / Usuários-Alvo', iaParams.userPersonas, 'personaName', 'description');
            addSection('Entidades Centrais do Sistema', iaParams.coreEntities, 'entityName', 'description');
            addSection('Principais Casos de Uso', iaParams.mainUseCases, 'useCase', 'description');

            doc.autoTable({
                startY: currentY,
                head: [['Componente', 'Descrição']],
                body: projectUnderstandingBody,
                theme: 'grid',
                headStyles: { fillColor: COLORS.headerFill, textColor: '#ffffff', fontStyle: 'bold' },
                margin: { left: pageMargin, right: pageMargin }
            });
            currentY = doc.lastAutoTable.finalY + 10;

            // --- Tabela de Escopo e Cronograma ---
            doc.autoTable({
                startY: currentY,
                head: [['3. Escopo do Projeto', '']],
                body: [
                    ['Composição da Equipe', team],
                    ['Cronograma Estimado', `${timeline} meses`]
                ].concat(features.length > 0 ? [[{ content: 'Funcionalidades Principais', colSpan: 2, styles: { halign: 'center', fontStyle: 'bold', fillColor: '#eaf2f8', textColor: COLORS.primary } }]] : []).concat(features.map(f => [f, ''])),
                theme: 'grid',
                headStyles: { fillColor: COLORS.headerFill, textColor: '#ffffff', fontStyle: 'bold' },
                margin: { left: pageMargin, right: pageMargin }
            });
            currentY = doc.lastAutoTable.finalY + 10;

            // --- Tabela Financeira ---
            doc.autoTable({
                startY: currentY,
                head: [['4. Investimento', 'Valor']],
                body: [
                    ['Custo de Desenvolvimento', formatCurrency(devTotal)],
                    ['Mensalidades', formatCurrency(feesTotal)],
                    [{ content: 'Subtotal', styles: { fontStyle: 'bold' } }, { content: formatCurrency(subtotal), styles: { fontStyle: 'bold' } }],
                    [`Impostos (${taxesPercent}%)`, formatCurrency(taxValue)],
                    [`Margem de Lucro (${profitMarginPercent}%)`, formatCurrency(profitValue)],
                ],
                foot: [
                    [{ content: 'Valor Total do Projeto', styles: { fontStyle: 'bold', fontSize: 12, fillColor: COLORS.secondary, textColor: '#ffffff' } },
                     { content: formatCurrency(grandTotal), styles: { fontStyle: 'bold', fontSize: 12, halign: 'right', fillColor: COLORS.secondary, textColor: '#ffffff' } }]
                ],
                theme: 'grid',
                headStyles: { fillColor: COLORS.headerFill, textColor: '#ffffff', fontStyle: 'bold' },
                columnStyles: { 1: { halign: 'right' } },
                margin: { left: pageMargin, right: pageMargin }
            });
            currentY = doc.lastAutoTable.finalY + 10;

            // --- Adiciona o footer em todas as páginas ---
            const pageCount = doc.internal.getNumberOfPages();
            for (let i = 1; i <= pageCount; i++) {
                doc.setPage(i);
                addFooter();
            }

            // --- 5. SAVE DOCUMENT ---
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
