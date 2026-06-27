document.addEventListener("DOMContentLoaded", () => {
    // 1. SISTEMA DE FAVORITOS UNIFICADO (DRY)
    const botoesFavorito = document.querySelectorAll(".favorito");
    botoesFavorito.forEach(botao => {
        botao.style.transition = "transform 0.2s ease, color 0.2s ease";
        botao.addEventListener("click", (e) => {
            e.preventDefault();
            if (botao.classList.contains("active")) {
                botao.classList.remove("active");
                botao.style.color = "#ccc";
                botao.style.transform = "scale(1)";
            } else {
                botao.classList.add("active");
                botao.style.color = "red";
                botao.style.transform = "scale(1.2)";
                setTimeout(() => { botao.style.transform = "scale(1)"; }, 200);
            }
        });
    });
});