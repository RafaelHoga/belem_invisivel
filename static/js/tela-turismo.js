
// =========================================================================
// 2. SISTEMA INTERATIVO DE FAVORITOS (ON/OFF NOS CARDS)
// =========================================================================
document.addEventListener("DOMContentLoaded", () => {
    const botoesFavorito = document.querySelectorAll(".favorito");

    botoesFavorito.forEach(botao => {
        // Define um estilo inicial padrão (coração vazio ou transparente se preferir)
        botao.style.transition = "transform 0.2s ease, color 0.2s ease";
        
        botao.addEventListener("click", (e) => {
            e.preventDefault(); // Evita qualquer comportamento inesperado
            
            // Alterna a classe ativado ou muda a cor diretamente de forma simples
            if (botao.classList.contains("active")) {
                botao.classList.remove("active");
                botao.style.color = "#ccc"; // Cor cinza de desativado
                botao.style.transform = "scale(1)";
            } else {
                botao.classList.add("active");
                botao.style.color = "red"; // Vermelho vibrante de favoritado
                
                // Efeito sutil de pulso ao clicar
                botao.style.transform = "scale(1.2)";
                setTimeout(() => {
                    botao.style.transform = "scale(1)";
                }, 200);
            }
        });
    });
});