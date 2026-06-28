document.addEventListener("DOMContentLoaded", () => {
    const botoesFavorito = document.querySelectorAll(".favorito");

    botoesFavorito.forEach(botao => {
        botao.addEventListener("click", (e) => {
            e.preventDefault(); // Evita comportamento de link/submit
            
            // Alterna a classe .active (adiciona se não tiver, remove se tiver)
            botao.classList.toggle("active");

            // Efeito de pulo (Pop) ao ativar
            if (botao.classList.contains("active")) {
                botao.style.transform = "scale(1.2)";
                setTimeout(() => { 
                    botao.style.transform = ""; 
                }, 200);
            } else {
                botao.style.transform = "";
            }
        });
    });
});