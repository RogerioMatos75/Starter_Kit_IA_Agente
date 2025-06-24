document.addEventListener('DOMContentLoaded', () => {
    // Mapeia os elementos do HTML para variáveis
    const timelineContainer = document.getElementById('timeline-container');
    const previewTextarea = document.getElementById('preview-textarea');
    const observationsTextarea = document.getElementById('observations-textarea');
    const approveBtn = document.getElementById('btn-approve');
    const repeatBtn = document.getElementById('btn-repeat');
    const backBtn = document.getElementById('btn-back');
    const pauseBtn = document.getElementById('btn-pause');
    const logsTableBody = document.getElementById('logs-table-body');
    const shutdownBtn = document.getElementById('btn-shutdown');

    /**
     * Busca o estado atual do projeto na API e atualiza a UI.
     */
    async function fetchStatus() {
        try {
            const response = await fetch('/api/status');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            updateUI(data);
            fetchLogs(); // Também busca os logs ao atualizar o status
        } catch (error) {
            console.error("Could not fetch project status:", error);
            previewTextarea.value = "Error: Could not connect to the backend. Is the Flask server running?";
        }
    }

    /**
     * Atualiza a interface do usuário com os dados recebidos da API.
     * @param {object} data - O objeto de status do projeto.
     */
    function updateUI(data) {
        // 1. Atualiza a Linha do Tempo (Timeline)
        timelineContainer.innerHTML = ''; // Limpa a timeline atual
        data.timeline.forEach(step => {
            let classes = 'flex flex-col items-center justify-center border-b-[3px] pb-[13px] pt-4';
            let textClasses = 'text-sm font-bold leading-normal tracking-[0.015em]';

            if (step.status === 'in-progress') {
                classes += ' border-b-[#dce8f3] text-white';
                textClasses += ' text-white';
            } else if (step.status === 'completed') {
                classes += ' border-b-transparent text-[#5de4c7]'; // Verde para concluído
                textClasses += ' text-[#5de4c7]';
            } else { // pending
                classes += ' border-b-transparent text-[#9daebe]';
                textClasses += ' text-[#9daebe]';
            }

            const stepElement = document.createElement('a');
            stepElement.className = classes;
            stepElement.href = '#';
            stepElement.innerHTML = `<p class="${textClasses}">${step.name}</p>`;
            timelineContainer.appendChild(stepElement);
        });

        // 2. Atualiza o Painel de Preview
        previewTextarea.value = data.current_step.preview_content;

        // 3. Habilita/Desabilita o botão "Voltar"
        const isFinished = data.actions.is_finished;
        backBtn.disabled = isFinished || !data.actions.can_go_back;
        if (backBtn.disabled) {
            backBtn.classList.add('opacity-50', 'cursor-not-allowed');
        } else {
            backBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        }

        // 4. Desabilita todos os botões de ação se o projeto estiver finalizado
        approveBtn.disabled = isFinished;
        repeatBtn.disabled = isFinished;
        pauseBtn.disabled = isFinished;
        // O botão de encerrar nunca é desabilitado
        [approveBtn, repeatBtn, pauseBtn].forEach(btn => {
            if (isFinished) btn.classList.add('opacity-50', 'cursor-not-allowed');
            else btn.classList.remove('opacity-50', 'cursor-not-allowed');
        });
    }

    /**
     * Busca o histórico de logs na API e atualiza a tabela de logs.
     */
    async function fetchLogs() {
        try {
            const response = await fetch('/api/logs');
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
        logsTableBody.innerHTML = ''; // Limpa a tabela
        if (logs.length === 0) {
            logsTableBody.innerHTML = `<tr><td colspan="5" class="text-center py-4 text-[#9daebe]">Nenhum registro de log encontrado.</td></tr>`;
            return;
        }
        logs.reverse().forEach(log => { // Exibe os mais recentes primeiro
            const row = `
                <tr>
                    <td class="px-4 py-2 whitespace-nowrap text-sm font-medium">${log.etapa}</td>
                    <td class="px-4 py-2 whitespace-nowrap text-sm">${log.status}</td>
                    <td class="px-4 py-2 whitespace-nowrap text-sm">${log.decisao}</td>
                    <td class="px-4 py-2 whitespace-nowrap text-sm">${new Date(log.data_hora).toLocaleString()}</td>
                    <td class="px-4 py-2 text-sm">${log.observacao || '-'}</td>
                </tr>
            `;
            logsTableBody.innerHTML += row;
        });
    }

    /**
     * Envia uma ação para o backend.
     * @param {string} action - O nome da ação (approve, repeat, etc.).
     */
    async function handleAction(action) {
        const observation = observationsTextarea.value;
        console.log(`Sending action: ${action} with observation: "${observation}"`);

        try {
            const response = await fetch('/api/action', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ action, observation }),
            });
            const data = await response.json();
            updateUI(data); // Atualiza a UI com o novo estado retornado pelo backend
            observationsTextarea.value = ''; // Limpa as observações
            fetchLogs(); // Atualiza os logs após uma ação
        } catch (error) {
            console.error("Error performing action:", error);
        }
    }

    /**
     * Pede confirmação e envia o comando para encerrar o servidor.
     */
    async function handleShutdown() {
        if (confirm("Tem certeza que deseja encerrar o servidor? Esta ação é irreversível.")) {
            try {
                // Envia a requisição, mas não espera uma resposta completa, pois o servidor vai desligar.
                fetch('/api/shutdown', { method: 'POST' });
                // Atualiza a UI para informar o usuário
                document.body.innerHTML = '<div class="flex items-center justify-center h-screen"><h1 class="text-white text-2xl text-center p-10">Servidor encerrado. Você já pode fechar esta aba.</h1></div>';
            } catch (error) {
                // Este catch pode não ser acionado se o servidor desligar antes de responder.
                console.error("Error sending shutdown signal:", error);
                alert("Sinal de encerramento enviado. O servidor deve estar offline.");
            }
        }
    }

    // Adiciona os "escutadores" de evento aos botões
    approveBtn.addEventListener('click', () => handleAction('approve'));
    repeatBtn.addEventListener('click', () => handleAction('repeat'));
    backBtn.addEventListener('click', () => handleAction('back'));
    pauseBtn.addEventListener('click', () => handleAction('pause'));
    shutdownBtn.addEventListener('click', () => handleShutdown());

    // Carrega o estado inicial do projeto quando a página é aberta
    fetchStatus(); // Isso também chamará fetchLogs()
    // fetchLogs(); // Pode ser chamado aqui também se quiser carregar os logs independentemente do status
});