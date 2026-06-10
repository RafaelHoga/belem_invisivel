// =========================================================================
// 1. CARROSSEL PRINCIPAL DA TELA DE TURISMO (HOTÉIS, VER-O-PESO, DOCAS...)
// =========================================================================
const carousel = document.getElementById("carouselImages");
const slides = document.querySelectorAll(".slide");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const dotsContainer = document.getElementById("dots");

let index = 0;
let autoPlayInterval;

if (slides.length > 0) {
    // Criar as bolinhas de navegação dinamicamente
    if (dotsContainer) {
        dotsContainer.innerHTML = ""; // Limpa antes de gerar
        slides.forEach((_, i) => {
            const dot = document.createElement("span");
            if (i === 0) dot.classList.add("active");
            dot.addEventListener("click", () => {
                index = i;
                updateCarousel();
                resetAutoPlay();
            });
            dotsContainer.appendChild(dot);
        });
    }

    function updateCarousel() {
        if (carousel) {
            carousel.style.transform = `translateX(-${index * 100}%)`;
            
            // Atualiza o estado visual das bolinhas
            const dots = document.querySelectorAll(".dots span");
            dots.forEach(dot => dot.classList.remove("active"));
            if (dots[index]) dots[index].classList.add("active");
        }
    }

    // Eventos dos botões de Próximo e Anterior
    if (nextBtn) {
        nextBtn.addEventListener("click", () => {
            index = (index + 1) % slides.length;
            updateCarousel();
            resetAutoPlay();
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener("click", () => {
            index = (index - 1 + slides.length) % slides.length;
            updateCarousel();
            resetAutoPlay();
        });
    }

    // Sistema de Auto Play (Troca a cada 5 segundos)
    function startAutoPlay() {
        autoPlayInterval = setInterval(() => {
            index = (index + 1) % slides.length;
            updateCarousel();
        }, 5000);
    }

    function resetAutoPlay() {
        clearInterval(autoPlayInterval);
        startAutoPlay();
    }

    // Inicializa o carrossel
    updateCarousel();
    startAutoPlay();
}

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