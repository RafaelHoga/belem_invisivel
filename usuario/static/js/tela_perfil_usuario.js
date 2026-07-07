/**
 * GERENCIADOR DA INTERFACE DE PERFIL - PARABOOK (2026)
 * Controla abas e as telas flutuantes (modais).
 */
document.addEventListener("DOMContentLoaded", function () {
    
    // --- LÓGICA DO SISTEMA DE ABAS ---
    const botoesAba = document.querySelectorAll(".aba-btn");
    const paineisAba = document.querySelectorAll(".aba-painel");

    botoesAba.forEach(botao => {
        botao.addEventListener("click", () => {
            const idAbaAlvo = botao.getAttribute("data-aba");
            const painelAlvo = document.getElementById(idAbaAlvo);

            if (painelAlvo) {
                botoesAba.forEach(b => b.classList.remove("active"));
                paineisAba.forEach(p => p.classList.remove("active"));

                botao.classList.add("active");
                painelAlvo.classList.add("active");
            }
        });
    });

    // --- LÓGICA DO MODAL: EDITAR DADOS PESSOAIS ---
    const modalEdicao = document.getElementById("painelEdicaoOverlay");
    const btnAbrirEdicao = document.getElementById("btnAbrirEdicao");
    const btnFecharX = document.getElementById("btnFecharX");
    const btnCancelarEdicao = document.getElementById("btnCancelarEdicao");

    // Função para abrir o modal
    function abrirModal() {
        modalEdicao.classList.add("mostrar-modal");
        document.body.style.overflow = "hidden"; // Impede scroll do fundo
    }

    // Função para fechar o modal
    function fecharModal() {
        modalEdicao.classList.remove("mostrar-modal");
        document.body.style.overflow = "auto"; // Reativa o scroll
    }

    // Ouvintes de evento (Clicks)
    if (btnAbrirEdicao) btnAbrirEdicao.addEventListener("click", abrirModal);
    if (btnFecharX) btnFecharX.addEventListener("click", fecharModal);
    if (btnCancelarEdicao) btnCancelarEdicao.addEventListener("click", fecharModal);

    // Fechar se o usuário clicar fora da caixa branca (no fundo escuro)
    window.addEventListener("click", function (event) {
        if (event.target === modalEdicao) {
            fecharModal();
        }
    });
});