document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll("#ratingStars i");
    const notaInput = document.getElementById("nota_avaliacao");
    const form = document.getElementById("formAvaliacao");

    // 1. Gerencia o clique visual nas estrelas interativas
    stars.forEach(star => {
        star.addEventListener("click", function () {
            const value = this.getAttribute("data-value");
            notaInput.value = value; // Atualiza o valor do input hidden

            // Atualiza o preenchimento visual das estrelas
            stars.forEach(s => {
                if (s.getAttribute("data-value") <= value) {
                    s.classList.remove("fa-regular");
                    s.classList.add("fa-solid");
                } else {
                    s.classList.remove("fa-solid");
                    s.classList.add("fa-regular");
                }
            });
        });
    });

    // 2. Controla o envio do formulário sem travar o processamento do Django
    form.addEventListener("submit", function (e) {
        if (notaInput.value === "0") {
            e.preventDefault(); // Impede o envio se não escolheu estrelas
            const feedback = document.getElementById("feedbackAvaliacao");
            feedback.innerText = "Por favor, selecione pelo menos 1 estrela para avaliar.";
            feedback.style.color = "red";
        }
        // Deixa o evento seguir o fluxo natural para o Django receber o POST!
    });
});