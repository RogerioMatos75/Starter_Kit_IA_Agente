document.addEventListener("DOMContentLoaded", () => {
  // Elementos do Popup
  const paymentPopup = document.getElementById("payment-popup");
  const closePopupBtn = document.getElementById("close-popup-btn");
  const popupOverlay = document.getElementById("popup-overlay");
  const triggerButtons = document.querySelectorAll(".btn-open-popup");
  const checkoutButton = document.getElementById("checkout-button");
  const emailInput = document.getElementById("email-for-payment");

  // Função para abrir o popup
  function openPopup() {
    if (paymentPopup) {
      paymentPopup.classList.remove("hidden");
    }
  }

  // Função para fechar o popup
  function closePopup() {
    if (paymentPopup) {
      paymentPopup.classList.add("hidden");
    }
  }

  // Adiciona o evento de clique a todos os botões que devem abrir o popup
  triggerButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault(); // Previne a navegação padrão do link '#'
      openPopup();
    });
  });

  // Eventos para fechar o popup
  if (closePopupBtn) {
    closePopupBtn.addEventListener("click", closePopup);
  }
  if (popupOverlay) {
    popupOverlay.addEventListener("click", closePopup);
  }

  // Lógica do botão de checkout (exemplo)
  if (checkoutButton) {
    checkoutButton.addEventListener("click", () => {
      const email = emailInput.value;
      if (!email || !email.includes("@")) {
        alert("Por favor, insira um e-mail válido.");
        emailInput.focus();
        return;
      }
      
      // AQUI ENTRARIA A LÓGICA DE PAGAMENTO
      // 1. Fazer um fetch para o seu backend (ex: /api/create-checkout-session)
      // 2. O backend se comunica com o Stripe/MercadoPago e retorna um link de pagamento
      // 3. Redirecionar o usuário para o link de pagamento
      alert(`Iniciando processo de pagamento para: ${email}.\n(Esta é uma simulação. A integração com o backend é necessária.)`);
    });
  }
});

