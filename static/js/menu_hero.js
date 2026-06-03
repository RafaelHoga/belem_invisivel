function configurarMenuHamburguer() {
    const hamburguer = document.getElementById("hamburguer");
    const menu = document.getElementById("menu");

    if (hamburguer && menu) {
        hamburguer.addEventListener("click", function () {
            menu.classList.toggle("active");

            // Alterna o ícone de forma limpa usando Font Awesome 6
            if (menu.classList.contains("active")) {
                hamburguer.innerHTML = '<i class="fa-solid fa-xmark"></i>';
            } else {
                hamburguer.innerHTML = '<i class="fa-solid fa-bars"></i>';
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", configurarMenuHamburguer);