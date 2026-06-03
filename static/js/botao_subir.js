// Removemos a criação dinâmica e deixamos apenas o monitoramento do Scroll
window.addEventListener("scroll", function() {
    const btn = document.getElementById("backToTop");
    if (btn) {
        if (window.scrollY > 300 || document.documentElement.scrollTop > 300) {
            btn.classList.add("visible");
        } else {
            btn.classList.remove("visible");
        }
    }
});

// Ação de clique suave
document.addEventListener("DOMContentLoaded", function() {
    const btn = document.getElementById("backToTop");
    if (btn) {
        btn.onclick = function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        };
    }
});