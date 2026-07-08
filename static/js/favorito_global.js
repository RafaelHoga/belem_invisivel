document.addEventListener("DOMContentLoaded", () => {
    const botoesFavorito = document.querySelectorAll(".favorito");

    botoesFavorito.forEach(botao => {
        botao.addEventListener("click", (e) => {
            e.preventDefault();
            
            const pontoId = botao.getAttribute("data-id");
            if (!pontoId) return;

            const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
            const csrftoken = tokenInput ? tokenInput.value : '';

            // Inteligência de Rota: Detecta dinamicamente se o projeto usa prefixos como /pontos/ ou /turismo/
            let baseRoute = "/";
            const currentPath = window.location.pathname;
            if (currentPath.includes("/pontos/")) {
                baseRoute = "/pontos/";
            } else if (currentPath.includes("/turismo/")) {
                baseRoute = "/turismo/";
            }

            const urlFinal = `${baseRoute}favoritar/${pontoId}/`;

            fetch(urlFinal, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "Content-Type": "application/json",
                },
            })
            .then(response => {
                if (response.status === 401) {
                    alert("Você precisa estar logado para favoritar!");
                    window.location.href = "/usuario/login/"; 
                    throw new Error("Não autenticado");
                }
                if (!response.ok) {
                    throw new Error("Erro no servidor");
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'sucesso') {
                    const icone = botao.querySelector('i');
                    
                    if (data.favoritado) {
                        botao.classList.add("active");
                        // Suporta tanto FontAwesome 5 (fas/far) quanto FontAwesome 6 (fa-solid/fa-regular)
                        icone.classList.remove("far", "fa-regular");
                        icone.classList.add("fas", "fa-solid");
                        
                        // Feedback visual de clique
                        botao.style.transform = "scale(1.2)";
                        setTimeout(() => botao.style.transform = "scale(1)", 200);
                    } else {
                        botao.classList.remove("active");
                        icone.classList.remove("fas", "fa-solid");
                        icone.classList.add("far", "fa-regular");
                        
                        botao.style.transform = "scale(0.9)";
                        setTimeout(() => botao.style.transform = "scale(1)", 200);
                    }
                }
            })
            .catch(error => console.error("Erro ao processar favorito:", error));
        });
    });
});