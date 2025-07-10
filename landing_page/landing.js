document.addEventListener("DOMContentLoaded", async () => {
  // --- Elementos da UI ---

  // Elementos do Popup (para o plano Starter)
  const paymentPopup = document.getElementById("payment-popup");
  const closePopupBtn = document.getElementById("close-popup-btn");
  const popupOverlay = document.getElementById("popup-overlay");
  const triggerButtons = document.querySelectorAll(".btn-open-popup");
  const checkoutButton = document.getElementById("checkout-button");
  const emailInput = document.getElementById("email-for-payment");

  // Botão de Download do Plano Pro
  const downloadProBtn = document.getElementById("downloadProBtn");

  let stripe; // Variável para a instância do Stripe

  // --- Inicialização do Stripe ---
  try {
    const response = await fetch('/api/stripe-public-key');
    const data = await response.json();
    if (data.publicKey) {
      stripe = Stripe(data.publicKey);
    } else {
      console.error("landing.js: Chave pública do Stripe não encontrada:", data.error);
      alert("Erro ao carregar o sistema de pagamento. Tente novamente mais tarde.");
    }
  } catch (error) {
    console.error("landing.js: Erro ao buscar a chave pública do Stripe:", error);
    alert("Erro de conexão com o serviço de pagamento. Tente novamente mais tarde.");
  }

  // Função para abrir o popup (Plano Starter)
  function openPopup() {
    if (paymentPopup) {
      paymentPopup.classList.remove("hidden");
    }
  }

  // Função para fechar o popup (Plano Starter)
  function closePopup() {
    if (paymentPopup) {
      paymentPopup.classList.add("hidden");
    }
  }

  // Adiciona o evento de clique a todos os botões que devem abrir o popup (Plano Starter)
  triggerButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault(); // Previne a navegação padrão do link '#'
      openPopup();
    });
  });

  // Eventos para fechar o popup (Plano Starter)
  if (closePopupBtn) {
    closePopupBtn.addEventListener("click", closePopup);
  }
  if (popupOverlay) {
    popupOverlay.addEventListener("click", closePopup);
  }

  // Lógica do botão de checkout (Plano Starter)
  if (checkoutButton) {
    checkoutButton.addEventListener("click", async () => {
      const email = emailInput.value;
      if (!email || !email.includes("@")) {
        alert("Por favor, insira um e-mail válido.");
        emailInput.focus();
        return;
      }

      if (!stripe) {
        alert("O sistema de pagamento não foi inicializado corretamente. Por favor, recarregue a página.");
        console.error("landing.js: Tentativa de checkout sem a instância do Stripe.");
        return;
      }

      // Mostra um estado de carregamento no botão
      checkoutButton.disabled = true;
      checkoutButton.innerHTML = '<span>Processando...</span>';

      try {
        const response = await fetch('/api/create-checkout-session-starter', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email })
        });

        const session = await response.json();

        if (session.checkout_url) {
          window.location.href = session.checkout_url;
        } else if (session.error) {
          alert(session.error.message || session.error);
          console.error("landing.js: Erro na sessão de checkout Starter:", session.error);
        } else {
          alert("Ocorreu um erro inesperado ao iniciar o checkout.");
          console.error("landing.js: Erro inesperado na sessão de checkout Starter.");
        }
      } catch (error) {
        console.error("landing.js: Erro ao criar sessão de checkout Starter:", error);
        alert("Erro de conexão ao serviço de pagamento. Tente novamente mais tarde.");
      } finally {
        // Restaura o botão
        checkoutButton.disabled = false;
        checkoutButton.innerHTML = `
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"></path></svg>
          <span>Pagar com Segurança</span>
        `;
      }
    });
  }

  // Lógica do botão de Download do Plano Pro
  if (downloadProBtn) {
    downloadProBtn.addEventListener('click', async (e) => {
      e.preventDefault();

      if (!stripe) {
        alert("O sistema de pagamento não foi inicializado corretamente. Por favor, recarregue a página.");
        console.error("landing.js: Tentativa de checkout Pro sem a instância do Stripe.");
        return;
      }

      downloadProBtn.disabled = true;
      downloadProBtn.textContent = 'Processando...';

      try {
        const response = await fetch('/api/create-checkout-session-pro', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
        });

        const session = await response.json();

        if (session.checkout_url) {
          window.location.href = session.checkout_url;
        } else if (session.error) {
          alert(session.error);
          console.error("landing.js: Erro na sessão de checkout Pro:", session.error);
        } else {
          alert("Ocorreu um erro inesperado ao iniciar o checkout.");
          console.error("landing.js: Erro inesperado na sessão de checkout Pro.");
        }
      } catch (error) {
        console.error("landing.js: Erro ao criar sessão de checkout:", error);
        alert("Erro de conexão ao serviço de pagamento. Tente novamente mais tarde.");
      }
    });
  } else {
    console.log("landing.js: Botão de download do plano Pro não encontrado.");
  }
});
