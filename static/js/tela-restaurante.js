// =========================================================================
// LOGICA INTERATIVA EXCLUSIVA DA TELA DE RESTAURANTES
// =========================================================================
document.addEventListener("DOMContentLoaded", () => {
    
    // 1. SISTEMA DE FAVORITOS (ON/OFF NOS CARDS)
    const botoesFavorito = document.querySelectorAll(".favorito");

    botoesFavorito.forEach(botao => {
        // Define o tempo e a transição do efeito de pulso
        botao.style.transition = "transform 0.2s ease, color 0.2s ease";
        
        botao.addEventListener("click", (e) => {
            e.preventDefault(); // Impede que o clique recarregue a página ou submeta algo
            
            if (botao.classList.contains("active")) {
                // Estado: Desfavoritado
                botao.classList.remove("active");
                botao.style.color = "#ccc"; // Volta para o cinza padrão
                botao.style.transform = "scale(1)";
            } else {
                // Estado: Favoritado
                botao.classList.add("active");
                botao.style.color = "red"; // Vermelho vibrante
                
                // Efeito sutil de pulso (cresce e volta ao normal)
                botao.style.transform = "scale(1.2)";
                setTimeout(() => {
                    botao.style.transform = "scale(1)";
                }, 200);
            }
        });
    });

});