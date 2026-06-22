// Função reutilizável que não gera conflito de escopo
function inicializarCarrossel(idCarrossel, idImagens, idPrev, idNext, idDots) {
    const container = document.getElementById(idCarrossel);
    if (!container) return; // Se não existir o carrossel na tela, ignora silenciosamente

    const carousel = document.getElementById(idImagens);
    const slides = container.querySelectorAll(".slide");
    const prevBtn = document.getElementById(idPrev);
    const nextBtn = document.getElementById(idNext);
    const dotsContainer = document.getElementById(idDots);
    
    let index = 0;
    let interval;

    if (slides.length === 0) return;

    // Gerar bolinhas
    if (dotsContainer) {
        dotsContainer.innerHTML = "";
        slides.forEach((_, i) => {
            const dot = document.createElement("span");
            if (i === 0) dot.classList.add("active");
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

    nextBtn?.addEventListener("click", () => movePara(index + 1));
    prevBtn?.addEventListener("click", () => movePara(index - 1));

    function startAuto() { interval = setInterval(() => movePara(index + 1), 5000); }
    function resetAuto() { clearInterval(interval); startAuto(); }

    startAuto();
}

// Inicializa automaticamente apontando para os IDs corretos de cada página
document.addEventListener("DOMContentLoaded", () => {
    inicializarCarrossel("mainCarousel", "carouselImages", "prevBtn", "nextBtn", "dots");
});

// =========================================================================
// FUNÇÃO GLOBAL PARA OS MINI CARROSSEIS INTERNOS DOS CARDS
// =========================================================================
window.moveLocalSlide = function(button, direction) {
    const carouselContainer = button.parentElement;
    const slides = carouselContainer.querySelectorAll(".card-slide");
    
    if (slides.length === 0) return;

    let activeIndex = 0;
    slides.forEach((slide, i) => {
        if (slide.classList.contains("active")) activeIndex = i;
    });

    slides[activeIndex].classList.remove("active");
    let nextIndex = (activeIndex + direction + slides.length) % slides.length;
    slides[nextIndex].classList.add("active");
}