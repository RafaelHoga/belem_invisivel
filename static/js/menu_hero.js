/**
 * SISTEMA DE NAVEGAÇÃO RESPONSIVA - BELÉM INVISÍVEL (2026)
 * Gerencia a abertura, fechamento e acessibilidade do menu hamburguer.
 */
function configurarMenuHamburguer() {
    const hamburguer = document.getElementById("hamburguer");
    // Mitigação de Risco: Busca o novo id estrutural 'nav-links' ou o antigo 'menu'
    const menu = document.getElementById("nav-links") || document.getElementById("menu");

    if (hamburguer && menu) {
        hamburguer.addEventListener("click", function (e) {
            e.stopPropagation(); // Evita propagação imediata para o documento
            
            menu.classList.toggle("active");
            
            // Controle de acessibilidade ARIA expandido para interfaces modernas
            const isActive = menu.classList.contains("active");
            hamburguer.setAttribute("aria-expanded", isActive);

            // Alterna o ícone de forma limpa usando a hierarquia estável do Font Awesome 6/7
            if (isActive) {
                hamburguer.innerHTML = '<i class="fa-solid fa-xmark"></i>';
                // Adiciona uma classe ao corpo para travar o scroll se necessário em celulares
                document.body.style.overflowY = 'hidden';
            } else {
                hamburguer.innerHTML = '<i class="fa-solid fa-bars"></i>';
                document.body.style.overflowY = 'auto';
            }
        });

        // Microinteração SaaS: Fecha o menu automaticamente se o usuário clicar fora dele
        document.addEventListener("click", function (e) {
            if (menu.classList.contains("active") && !menu.contains(e.target) && !hamburguer.contains(e.target)) {
                menu.classList.remove("active");
                hamburguer.innerHTML = '<i class="fa-solid fa-bars"></i>';
                document.body.style.overflowY = 'auto';
            }
        });
    }
}

// Inicialização segura garantindo o carregamento completo da DOM do Django
document.addEventListener("DOMContentLoaded", configurarMenuHamburguer);