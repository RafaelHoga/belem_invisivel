/**
 * SISTEMA DE NAVEGAÇÃO RESPONSIVA - BELÉM INVISÍVEL (2026)
 * Gerencia a abertura, fechamento e acessibilidade do menu hamburguer.
 */
function configurarMenuHamburguer() {
    const hamburguer = document.getElementById("hamburguer");
    // CORREÇÃO: Mapeia o menu diretamente pela classe estrutural do header.css
    const menu = document.querySelector(".nav-navigation");

    if (hamburguer && menu) {
        hamburguer.addEventListener("click", function (e) {
            e.stopPropagation(); // Evita fechar imediatamente ao clicar no próprio botão
            
            menu.classList.toggle("active");
            
            const isActive = menu.classList.contains("active");
            hamburguer.setAttribute("aria-expanded", isActive);

            // Alterna o ícone de forma limpa usando Font Awesome
            if (isActive) {
                hamburguer.innerHTML = '<i class="fa-solid fa-xmark"></i>';
                document.body.style.overflowY = 'hidden'; // Bloqueia scroll de fundo no mobile
            } else {
                hamburguer.innerHTML = '<i class="fa-solid fa-bars"></i>';
                document.body.style.overflowY = 'auto';
            }
        });

        // Microinteração: Fecha o menu se clicar em qualquer lugar fora dele
        document.addEventListener("click", function (e) {
            if (menu.classList.contains("active") && !menu.contains(e.target) && !hamburguer.contains(e.target)) {
                menu.classList.remove("active");
                hamburguer.innerHTML = '<i class="fa-solid fa-bars"></i>';
                document.body.style.overflowY = 'auto';
            }
        });
    }
}

// Inicialização segura garantindo o carregamento completo da DOM
document.addEventListener("DOMContentLoaded", configurarMenuHamburguer);