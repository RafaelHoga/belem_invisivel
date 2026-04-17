// Chama a função ao carregar a página
document.addEventListener('DOMContentLoaded', carregarHeader);

function carregarHeader() {
    fetch('header_menu_hero.html')
        .then(response => response.text())
        .then(data => {
            // 1. Insere o conteúdo no placeholder
            document.getElementById('header-placeholder').innerHTML = data;

            // 2. CHAMA A FUNÇÃO DO MENU SOMENTE APÓS O HTML EXISTIR
            configurarMenuHamburguer();
        })
        .catch(error => console.error('Erro ao carregar o header:', error));
}

function configurarMenuHamburguer() {
    const hamburguer = document.getElementById("hamburguer");
    const menu = document.getElementById("menu");

    // Verifica se os elementos realmente existem para evitar novos erros
    if (hamburguer && menu) {
        hamburguer.addEventListener("click", function () {
            menu.classList.toggle("active");

            // Lógica de troca de ícone
            if (menu.classList.contains("active")) {
                hamburguer.innerText = "✖";
            } else {
                // Se você usa FontAwesome, o ideal é voltar o ícone original
                hamburguer.innerHTML = '<i class="fa fa-bars" aria-hidden="true"></i>';
            }
        });
    }
}

// Inicia o processo quando a página carregar
document.addEventListener('DOMContentLoaded', carregarHeader);