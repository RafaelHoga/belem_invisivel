function abrirDetalhes(chave) {

    const item = detalhesCards[chave];

    if (!item) return;

    document.getElementById("tituloModal").innerText =
        item.titulo;

    document.getElementById("textoModal").innerText =
        item.texto;

    document.getElementById("modalDetalhes")
        .style.display = "flex";
}

function fecharDetalhes() {
    document.getElementById("modalDetalhes")
        .style.display = "none";
}

function abrirDetalhes(chave) {

    const item = detalhesCards[chave];

    if (!item) {
        console.error("Detalhe não encontrado:", chave);
        return;
    }

    document.getElementById("tituloModal").innerText =
        item.titulo;

    document.getElementById("textoModal").innerText =
        item.texto;

    document.getElementById("modalDetalhes")
        .style.display = "flex";
}

function fecharDetalhes() {

    document.getElementById("modalDetalhes")
        .style.display = "none";
}

window.onclick = function(event) {

    const modal =
        document.getElementById("modalDetalhes");

    if (event.target === modal) {
        fecharDetalhes();
    }
}