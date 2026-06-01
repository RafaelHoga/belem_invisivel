function configurarMenuHamburguer() {
    const hamburguer = document.getElementById("hamburguer");
    const menu = document.getElementById("menu");

    if (hamburguer && menu) {
        hamburguer.addEventListener("click", function () {
            menu.classList.toggle("active");

            if (menu.classList.contains("active")) {
                hamburguer.innerText = "✖";
            } else {
                hamburguer.innerHTML = '<i class="fa fa-bars" aria-hidden="true"></i>';
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", configurarMenuHamburguer);

