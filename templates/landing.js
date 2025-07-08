document.addEventListener("DOMContentLoaded", async () => {
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

  // Lógica do botão de checkout (Plano Starter - exemplo)
  if (checkoutButton) {
    checkoutButton.addEventListener("click", () => {
      const email = emailInput.value;
      if (!email || !email.includes("@")) {
        alert("Por favor, insira um e-mail válido.");
        emailInput.focus();
        return;
      }
      alert(`Iniciando processo de pagamento para: ${email}.
(Esta é uma simulação. A integração com o backend é necessária.)`);
    });
  }

  // --- Lógica para o Plano Pro (Download de Executáveis) ---

  // 1. Obter a chave pública do Stripe do backend
  try {
    const response = await fetch('/api/stripe-public-key');
    const data = await response.json();
    if (data.publicKey) {
      stripe = Stripe(data.publicKey);
    } else {
      console.error("Chave pública do Stripe não encontrada:", data.error);
      alert("Erro ao carregar a chave de pagamento. Tente novamente mais tarde.");
    }
  } catch (error) {
    console.error("Erro ao buscar a chave pública do Stripe:", error);
    alert("Erro de conexão ao serviço de pagamento. Tente novamente mais tarde.");
  }

  // 2. Adicionar evento de clique ao botão de Download do Plano Pro
  if (downloadProBtn && stripe) {
    downloadProBtn.addEventListener('click', async (e) => {
      e.preventDefault();

      try {
        const response = await fetch('/api/create-checkout-session-pro', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          // body: JSON.stringify({ userId: 'user_id_aqui' }) // Opcional: enviar ID do usuário logado
        });

        const session = await response.json();

        if (session.checkout_url) {
          // Redirecionar para o Stripe Checkout
          window.location.href = session.checkout_url;
        } else if (session.error) {
          alert(session.error);
        } else {
          alert("Ocorreu um erro inesperado ao iniciar o checkout.");
        }
      } catch (error) {
        console.error("Erro ao criar sessão de checkout:", error);
        alert("Erro de conexão ao serviço de pagamento. Tente novamente mais tarde.");
      }
    });
  }
});

