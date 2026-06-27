document.addEventListener("DOMContentLoaded", function () {
    const estrelas = document.querySelectorAll("#ratingStars i");
    const inputNota = document.getElementById("nota_avaliacao");
    const form = document.getElementById("formAvaliacao");
    const feedback = document.getElementById("feedbackAvaliacao");

    if (!form || !inputNota || !feedback) return;

    // Lógica para acender as estrelas no clique
    estrelas.forEach(estrela => {
        estrela.addEventListener("click", function () {
            const notaSelecionada = parseInt(this.getAttribute("data-value"), 10);
            
            // Salva a nota no input hidden
            inputNota.value = notaSelecionada;

            // Atualiza visualmente as estrelas
            atualizarEstrelas(notaSelecionada);
        });

        // Efeito visual ao passar o mouse
        estrela.addEventListener("mouseover", function () {
            const valorHover = parseInt(this.getAttribute("data-value"), 10);
            atualizarEstrelas(valorHover);
        });
    });

    // Quando o mouse sai da área das estrelas, volta para a nota real selecionada
    const ratingStarsContainer = document.getElementById("ratingStars");
    if (ratingStarsContainer) {
        ratingStarsContainer.addEventListener("mouseleave", function () {
            const notaAtual = parseInt(inputNota.value, 10) || 0;
            atualizarEstrelas(notaAtual);
        });
    }

    // Função auxiliar que acende as estrelas até a posição indicada
    function atualizarEstrelas(valor) {
        estrelas.forEach(estrela => {
            const valorEstrela = parseInt(estrela.getAttribute("data-value"), 10);
            if (valorEstrela <= valor) {
                estrela.classList.remove("fa-regular");
                estrela.classList.add("fa-solid", "active");
            } else {
                estrela.classList.remove("fa-solid", "active");
                estrela.classList.add("fa-regular");
            }
        });
    }

    // Envio do formulário com a validação corrigida contra erros de propriedade nula
    form.addEventListener("submit", function (e) {
        // Correção da imagem: convertemos o valor explicitamente para string e limpamos espaços
        const valorNota = inputNota ? String(inputNota.value).trim() : "0";

        if (valorNota === "0" || valorNota === "") {
            e.preventDefault(); // Bloqueia o envio se o usuário não escolheu nenhuma estrela
            feedback.innerText = "Por favor, selecione uma nota de 1 a 5 estrelas.";
            feedback.style.color = "#d9534f"; // Tom de vermelho
            return;
        }

        // Se passou da validação, o formulário segue o fluxo natural para o Django salvar no MySQL
        feedback.innerText = "Enviando avaliação...";
        feedback.style.color = "#41836d"; // Verde-escuro do projeto
    });
});