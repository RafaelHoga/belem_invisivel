/**
 * GERENCIADOR DE CARROSSEIS FLUIDOS - BELÉM INVISÍVEL (2026)
 * Suporta múltiplos slides simultâneos, paginação inteligente e toque mobile.
 */
function inicializarCarrossel(idCarrossel, idImagens, idPrev, idNext, idDots) {
    // Tenta buscar pelo ID específico ou pela classe genérica padrão para mitigar erros
    let container = document.getElementById(idCarrossel);
    if (!container) {
        container = document.querySelector(".carousel");
    }
    if (!container) return; // Fail-silent caso a página atual não possua carrossel

    const carousel = container.querySelector(`#${idImagens}`) || container.querySelector(".carousel-images");
    const slides = container.querySelectorAll(".slide");
    const prevBtn = document.getElementById(idPrev);
    const nextBtn = document.getElementById(idNext);
    const dotsContainer = document.getElementById(idDots);
    
    let index = 0;
    let interval;

    if (slides.length === 0 || !carousel) return;

    // Gerar marcadores de paginação dinâmicos (dots)
    if (dotsContainer) {
        dotsContainer.innerHTML = "";
        slides.forEach((_, i) => {
            const dot = document.createElement("span");
            if (i === 0) dot.classList.add("active");
            dot.setAttribute("aria-label", `Ir para o slide ${i + 1}`);
            dot.addEventListener("click", () => { movePara(i); });
            dotsContainer.appendChild(dot);
        });
    }

    function updateVisual() {
        carousel.style.transform = `translateX(-${index * 100}%)`;
        const dots = dotsContainer?.querySelectorAll("span");
        dots?.forEach((dot, i) => {
            dot.classList.toggle("active", i === index);
        });
    }

    function movePara(novoIndex) {
        index = (novoIndex + slides.length) % slides.length;
        updateVisual();
        resetAuto();
    }

    // Ouvintes de Eventos Seguros com Operador Coalescente (?.)
    nextBtn?.addEventListener("click", (e) => { e.preventDefault(); movePara(index + 1); });
    prevBtn?.addEventListener("click", (e) => { e.preventDefault(); movePara(index - 1); });

    // Autoplay Otimizado
    function startAuto() { 
        interval = setInterval(() => movePara(index + 1), 6000); 
    }
    function resetAuto() { 
        clearInterval(interval); 
        startAuto(); 
    }

    // Suporte a gestos Touch (Melhoria drástica para Responsividade Mobile)
    let startX = 0;
    container.addEventListener("touchstart", (e) => { startX = e.touches[0].clientX; }, { passive: true });
    container.addEventListener("touchend", (e) => {
        let diffX = startX - e.changedTouches[0].clientX;
        if (Math.abs(diffX) > 50) { // Limiar mínimo de arraste de 50px
            if (diffX > 0) movePara(index + 1); // Arrastou para a esquerda
            else movePara(index - 1);           // Arrastou para a direita
        }
    }, { passive: true });

    startAuto();
    updateVisual(); // Força o alinhamento inicial do layout renderizado
}

// Inicialização automática robusta combinando os IDs herdados e novos do index.html
document.addEventListener("DOMContentLoaded", () => {
    inicializarCarrossel("mainCarousel", "carouselImages", "prevBtn", "nextBtn", "dots");
});

// =========================================================================
// FUNÇÃO GLOBAL REUTILIZÁVEL PARA OS MINI CARROSSEIS INTERNOS DOS CARDS
// =========================================================================
window.moveLocalSlide = function(button, direction) {
    const carouselContainer = button.parentElement;
    if (!carouselContainer) return;
    
    const slides = carouselContainer.querySelectorAll(".card-slide");
    if (slides.length === 0) return;

    let activeIndex = 0;
    slides.forEach((slide, i) => {
        if (slide.classList.contains("active")) activeIndex = i;
    });

    slides[activeIndex].classList.remove("active");
    let nextIndex = (activeIndex + direction + slides.length) % slides.length;
    slides[nextIndex].classList.add("active");
};