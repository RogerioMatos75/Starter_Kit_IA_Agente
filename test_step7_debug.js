// Script de debug para testar a Etapa 7 (Deploy)
console.log("=== DEBUG ETAPA 7 ===");

// Verificar se o elemento step-7-content existe
const step7Content = document.getElementById("step-7-content");
console.log("step-7-content element:", step7Content);

if (step7Content) {
  console.log("Classes do step-7-content:", step7Content.className);
  console.log(
    "step-7-content está visível?",
    !step7Content.classList.contains("hidden"),
  );
} else {
  console.error("ERRO: step-7-content não encontrado!");
}

// Verificar se o botão da sidebar existe
const sidebarStep7 = document.getElementById("sidebar-step-deploy");
console.log("sidebar-step-deploy element:", sidebarStep7);

if (sidebarStep7) {
  console.log("data-step:", sidebarStep7.dataset.step);
  console.log("onclick:", sidebarStep7.getAttribute("onclick"));
}

// Verificar se a função showStep está disponível
console.log("showStep function:", typeof showStep);

// Testar a função showStep(7)
if (typeof showStep === "function") {
  console.log("Tentando executar showStep(7)...");
  try {
    showStep(7);

    // Verificar novamente se ficou visível
    setTimeout(() => {
      const step7AfterShow = document.getElementById("step-7-content");
      console.log(
        "Após showStep(7), step-7-content visível?",
        step7AfterShow && !step7AfterShow.classList.contains("hidden"),
      );
    }, 100);
  } catch (error) {
    console.error("Erro ao executar showStep(7):", error);
  }
} else {
  console.error("showStep function não está disponível!");
}

// Verificar todas as seções de content
const allContentSections = document.querySelectorAll(".content-section");
console.log(
  "Total de content-sections encontradas:",
  allContentSections.length,
);
allContentSections.forEach((section, index) => {
  console.log(
    `Section ${index + 1}:`,
    section.id,
    section.classList.contains("hidden") ? "HIDDEN" : "VISIBLE",
  );
});

// Verificar se há problemas de CSS
const mainContent = document.querySelector(".main-content");
console.log("main-content element:", mainContent);
if (mainContent) {
  console.log("main-content styles:", {
    marginLeft: getComputedStyle(mainContent).marginLeft,
    width: getComputedStyle(mainContent).width,
    overflow: getComputedStyle(mainContent).overflow,
  });
}
