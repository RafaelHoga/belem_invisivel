// Chama a função ao carregar a página
document.addEventListener('DOMContentLoaded', carregarHeader);

function carregarHeader() {
    fetch('novo-comentario.html')
        .then(response => response.text())
        .then(data => {
            // 1. Insere o conteúdo no placeholder
            document.getElementById('nova_avaliacao').innerHTML = data;

            // 2. CHAMA A FUNÇÃO DO MENU SOMENTE APÓS O HTML EXISTIR
            configurarMenuHamburguer();
        })
        .catch(error => console.error('Erro ao carregar o header:', error));
}

document.addEventListener("DOMContentLoaded", function () {
    const estrelas = document.querySelectorAll("#ratingStars i");
    const inputNota = document.getElementById("nota_avaliacao");
    const form = document.getElementById("formAvaliacao");
    const feedback = document.getElementById("feedbackAvaliacao");

    // Lógica para acender as estrelas no clique
    estrelas.forEach(estrela => {
        estrela.addEventListener("click", function () {
            const notaSelecionada = parseInt(this.getAttribute("data-value"));
            
            // Salva a nota no input hidden
            inputNota.value = notaSelecionada;

            // Atualiza visualmente as estrelas
            atualizarEstrelas(notaSelecionada);
        });

        // Efeito visual ao passar o mouse (opcional, melhora a experiência)
        estrela.addEventListener("mouseover", function () {
            const valorHover = parseInt(this.getAttribute("data-value"));
            atualizarEstrelas(valorHover);
        });
    });

    // Quando o mouse sai da área das estrelas, volta para a nota real selecionada
    document.getElementById("ratingStars").addEventListener("mouseleave", function () {
        const notaAtual = parseInt(inputNota.value);
        atualizarEstrelas(notaAtual);
    });

    // Função auxiliar que acende as estrelas até a posição indicada
    function atualizarEstrelas(valor) {
        estrelas.forEach(estrela => {
            const valorEstrela = parseInt(estrela.getAttribute("data-value"));
            if (valorEstrela <= valor) {
                // Transforma em estrela preenchida e adiciona classe ativa
                estrela.classList.remove("fa-regular");
                estrela.classList.add("fa-solid", "active");
            } else {
                // Mantém apenas o contorno da estrela vazia
                estrela.classList.remove("fa-solid", "active");
                estrela.classList.add("fa-regular");
            }
        });
    }

    // Envio do formulário (preparado para integrar com o Banco de Dados)
    form.addEventListener("submit", function (e) {
        e.preventDefault();

        if (inputNota.value === "0") {
            feedback.innerText = "Por favor, selecione uma nota de 1 a 5 estrelas.";
            feedback.style.color = "red";
            return;
        }

        // Objeto estruturado com os dados da avaliação
        const dadosAvaliacao = {
            nota: inputNota.value,
            comentario: document.getElementById("comentario_texto").value,
            data_envio: new Date().toLocaleDateString('pt-BR')
        };

        console.log("Pronto para enviar para o servidor:", dadosAvaliacao);

        // Feedback positivo de sucesso temporário
        feedback.innerText = "Obrigado! Sua avaliação foi enviada com sucesso.";
        feedback.style.color = "green";

        // Reseta o formulário
        form.reset();
        atualizarEstrelas(0);
        inputNota.value = "0";
    });
});