// tela-turismo.js - Deixe APENAS isso:
document.addEventListener("DOMContentLoaded", () => {
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

// 2. FUNÇÃO GLOBAL PARA MOVIMENTAR OS SLIDES DOS CARDS (Chamada pelo onclick do HTML)
function moveLocalSlide(button, direction) {
    // Encontra o container do carrossel onde o botão foi clicado
    const carousel = button.parentElement;
    const slides = carousel.querySelectorAll('.card-slide');
    
    if (slides.length === 0) return;

    // Descobre qual imagem está ativa no momento
    let activeIndex = Array.from(slides).findIndex(slide => slide.classList.contains('active'));
    
    // Remove o estado ativo da imagem atual
    slides[activeIndex].classList.remove('active');

    // Calcula o próximo índice (com efeito infinito/circular)
    activeIndex += direction;
    if (activeIndex >= slides.length) {
        activeIndex = 0;
    } else if (activeIndex < 0) {
        activeIndex = slides.length - 1;
    }

    // Adiciona a classe ativa na nova imagem
    slides[activeIndex].classList.add('active');
}