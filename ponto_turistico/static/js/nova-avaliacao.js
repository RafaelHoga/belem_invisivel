document.addEventListener("DOMContentLoaded", function () {
    const estrelas = document.querySelectorAll("#ratingStars i");
    const inputNota = document.getElementById("nota_avaliacao");
    const form = document.getElementById("formAvaliacao");
    const feedback = document.getElementById("feedbackAvaliacao");

    if (!form || !inputNota || !feedback) return;

    // Lógica para acender as estrelas ao clicar ou passar o mouse
    estrelas.forEach((estrela, index) => {
        estrela.addEventListener("click", function () {
            const notaSelecionada = index + 1;
            inputNota.value = notaSelecionada;
            atualizarEstrelas(notaSelecionada);
        });

        estrela.addEventListener("mouseover", function () {
            const valorHover = index + 1;
            atualizarEstrelas(valorHover);
        });
    });

    const ratingStarsContainer = document.getElementById("ratingStars");
    if (ratingStarsContainer) {
        ratingStarsContainer.addEventListener("mouseleave", function () {
            const notaAtual = parseInt(inputNota.value, 10) || 0;
            atualizarEstrelas(notaAtual);
        });
    }

    function atualizarEstrelas(valor) {
        estrelas.forEach((estrela, index) => {
            const valorOrdinalEstrela = index + 1;
            if (valorOrdinalEstrela <= valor) {
                estrela.classList.remove("fa-regular");
                estrela.classList.add("fa-solid", "active");
            } else {
                estrela.classList.remove("fa-solid", "active");
                estrela.classList.add("fa-regular");
            }
        });
    }

    // ==========================================
    // ENVIAR VIA AJAX (SEM RECARREGAR MANUALMENTE)
    // ==========================================
    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Impede o envio padrão e mantém o foco na tela

        const valorNota = String(inputNota.value).trim();
        const comentarioTexto = document.getElementById("comentario_texto").value.trim();

        if (valorNota === "0" || valorNota === "") {
            feedback.innerText = "Por favor, selecione uma nota de 1 a 5 estrelas.";
            feedback.style.color = "#d9534f"; 
            return;
        }

        if (comentarioTexto === "") {
            feedback.innerText = "Por favor, preencha o campo de comentário.";
            feedback.style.color = "#d9534f";
            return;
        }

        feedback.innerText = "Enviando avaliação...";
        feedback.style.color = "#41836d";

        const formData = new FormData(form);
        const urlDestino = form.getAttribute("action");

        fetch(urlDestino, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest" 
            }
        })
        .then(response => {
            if (response.ok) {
                feedback.innerText = "Sua avaliação foi enviada com sucesso!";
                feedback.style.color = "#2ecc71";
                
                // Reseta o formulário limpando o texto e as estrelas
                form.reset();
                inputNota.value = "0";
                atualizarEstrelas(0);
                
                // Recarrega a página após 1 segundo para atualizar a lista do Django
                // e mostrar a nova avaliação somada a todas as anteriores
                setTimeout(() => {
                    window.location.reload();
                }, 1000);

            } else {
                feedback.innerText = "Erro ao processar o salvamento no servidor.";
                feedback.style.color = "#e74c3c";
            }
        })
        .catch(error => {
            console.error("Erro:", error);
            feedback.innerText = "Erro de conexão ao enviar a avaliação.";
            feedback.style.color = "#e74c3c";
        });
    });
});