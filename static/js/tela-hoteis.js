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

    // 2. FILTRO DE BUSCA (Mantido exclusivo da listagem de hotéis)
    const searchInput = document.getElementById("searchInput");
    const cards = document.querySelectorAll("#hotelGrid .card-padrao");

    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            const value = e.target.value.toLowerCase();
            cards.forEach(card => {
                const hotelName = card.getAttribute("data-name") ? card.getAttribute("data-name").toLowerCase() : "";
                if (hotelName.includes(value)) {
                    card.style.display = "flex";
                } else {
                    card.style.display = "none";
                }
            });
        });
    }
});