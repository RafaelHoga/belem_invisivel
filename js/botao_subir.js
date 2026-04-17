// Espera o DOM carregar
document.addEventListener("DOMContentLoaded", function() {
    // 1. Cria o botão dinamicamente
    const btn = document.createElement("button");
    btn.id = "backToTop";
    btn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    btn.title = "Voltar ao topo";
    document.body.appendChild(btn);

    // 2. Lógica de mostrar/esconder
    window.onscroll = function() {
        if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
            btn.style.display = "block";
        } else {
            btn.style.display = "none";
        }
    };

    // 3. Lógica de clique
    btn.onclick = function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };
});