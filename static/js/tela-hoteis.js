// tela-hoteis.js - Apenas comportamento exclusivo de busca da tela
document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    const cards = document.querySelectorAll("#hotelGrid .custom-card");

    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            const value = e.target.value.toLowerCase();
            cards.forEach(card => {
                const hotelName = card.getAttribute("data-name") ? card.getAttribute("data-name").toLowerCase() : "";
                if (hotelName.includes(value)) {
                    card.style.display = ""; // Restaura o comportamento padrão do CSS (Grid item)
                } else {
                    card.style.display = "none";
                }
            });
        });
    }
});