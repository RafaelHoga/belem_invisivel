console.log("modal carregou");
document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("modal");
    const abrir = document.getElementById("abrir-modal");
    const fechar = document.querySelector(".fechar");

    abrir.addEventListener("click", () => {
        modal.style.display = "flex";
    });

    fechar.addEventListener("click", () => {
        modal.style.display = "none";
    });

    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });

});