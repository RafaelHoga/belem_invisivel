/**
 * GERENCIADOR DA INTERFACE DE PERFIL - PARABOOK (2026)
 * Controla a alternância fluida entre os painéis de dados do usuário.
 */
document.addEventListener("DOMContentLoaded", function () {
    const botoesAba = document.querySelectorAll(".aba-btn");
    const paineisAba = document.querySelectorAll(".aba-painel");

    botoesAba.forEach(botao => {
        botao.addEventListener("click", () => {
            // Captura o ID do painel alvo associado ao botão clicado
            const idAbaAlvo = botao.getAttribute("data-aba");
            const painelAlvo = document.getElementById(idAbaAlvo);

            if (painelAlvo) {
                // Remove a classe de atividade de todas as abas e painéis
                botoesAba.forEach(b => b.classList.remove("active"));
                paineisAba.forEach(p => p.classList.remove("active"));

                // Ativa exclusivamente a aba clicada e seu respectivo painel
                botao.classList.add("active");
                painelAlvo.classList.add("active");
            }
        });
    });
});