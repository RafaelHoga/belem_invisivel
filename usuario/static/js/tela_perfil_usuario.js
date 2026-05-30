document.addEventListener("DOMContentLoaded", function () {
    const botoesAba = document.querySelectorAll(".aba-btn");
    const paineisAba = document.querySelectorAll(".aba-painel");

    botoesAba.forEach(botao => {
        botao.addEventListener("click", () => {
            // Remove active de todos os botões
            botoesAba.forEach(b => b.classList.remove("active"));
            // Adiciona active no clicado
            botao.classList.add("active");

            // Esconde todos os painéis
            paineisAba.forEach(painel => painel.classList.remove("active"));
            
            // Mostra o painel correto com base no atributo data-aba
            const idAba = botao.getAttribute("data-aba");
            document.getElementById(idAba).classList.add("active");
        });
    });
});