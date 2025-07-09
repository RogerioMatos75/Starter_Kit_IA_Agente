document.addEventListener("DOMContentLoaded", async () => {
  console.log("landing.js: DOMContentLoaded - Script iniciado.");

  // Elementos do Popup (para o plano Starter)
  const paymentPopup = document.getElementById("payment-popup");
  const closePopupBtn = document.getElementById("close-popup-btn");
  const popupOverlay = document.getElementById("popup-overlay");
  const triggerButtons = document.querySelectorAll(".btn-open-popup");
  const checkoutButton = document.getElementById("checkout-button");
  const emailInput = document.getElementById("email-for-payment");

  // Botão de Download do Plano Pro
  const downloadProBtn = document.getElementById("downloadProBtn");
  console.log("landing.js: downloadProBtn encontrado?", downloadProBtn);

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
    console.log("landing.js: Buscando chave pública do Stripe...");
    const response = await fetch('/api/stripe-public-key');
    const data = await response.json();
    if (data.publicKey) {
      stripe = Stripe(data.publicKey);
      console.log("landing.js: Chave pública do Stripe carregada com sucesso.", data.publicKey);
      console.log("landing.js: Tipo de Stripe:", typeof Stripe);
    } else {
      console.error("landing.js: Chave pública do Stripe não encontrada:", data.error);
      alert("Erro ao carregar a chave de pagamento. Tente novamente mais tarde.");
    }
  } catch (error) {
    console.error("landing.js: Erro ao buscar a chave pública do Stripe:", error);
    alert("Erro de conexão ao serviço de pagamento. Tente novamente mais tarde.");
  }

  // 2. Adicionar evento de clique ao botão de Download do Plano Pro
  if (downloadProBtn && stripe) {
    console.log("landing.js: Adicionando event listener ao downloadProBtn.");
    downloadProBtn.addEventListener('click', async (e) => {
      console.log("landing.js: Clique no downloadProBtn detectado.");
      e.preventDefault();

      try {
        console.log("landing.js: Iniciando fetch para create-checkout-session-pro.");
        const response = await fetch('/api/create-checkout-session-pro', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          // body: JSON.stringify({ userId: 'user_id_aqui' }) // Opcional: enviar ID do usuário logado
        });

        const session = await response.json();
        console.log("landing.js: Resposta da sessão de checkout:", session);

        if (session.checkout_url) {
          // Redirecionar para o Stripe Checkout
          console.log("landing.js: Redirecionando para o Stripe Checkout:", session.checkout_url);
          window.location.href = session.checkout_url;
        } else if (session.error) {
          alert(session.error);
          console.error("landing.js: Erro na sessão de checkout:", session.error);
        } else {
          alert("Ocorreu um erro inesperado ao iniciar o checkout.");
          console.error("landing.js: Erro inesperado na sessão de checkout.");
        }
      } catch (error) {
        console.error("landing.js: Erro ao criar sessão de checkout:", error);
        alert("Erro de conexão ao serviço de pagamento. Tente novamente mais tarde.");
      }
    });
  } else {
    console.log("landing.js: Não foi possível adicionar event listener ao downloadProBtn. downloadProBtn:", downloadProBtn, "stripe:", stripe);
  }
});

