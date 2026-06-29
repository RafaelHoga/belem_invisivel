document.addEventListener("DOMContentLoaded", () => {
    const botoesFavorito = document.querySelectorAll(".favorito");

    botoesFavorito.forEach(botao => {
        botao.addEventListener("click", (e) => {
            e.preventDefault(); // Evita comportamento de link/submit
            
            // Pega o ID do ponto salvo no atributo HTML data-id
            const pontoId = botao.getAttribute("data-id");
            if (!pontoId) return;

            // Busca o CSRF Token gerado na página pelo Django
            const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
            const csrftoken = tokenInput ? tokenInput.value : '';

            // Envia os dados de forma assíncrona (Fetch API) para a View do Python
            fetch(`/usuario/favoritar/${pontoId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "Content-Type": "application/json"
                }
            })
            .then(response => {
                // Se o usuário cair no redirect de não autenticado
                if (response.redirected || response.status === 401) {
                    alert("Você precisa estar logado para favoritar este local!");
                    window.location.href = "/usuario/login/"; // Ajuste o caminho se necessário
                    return;
                }
                return response.json();
            })
            .then(data => {
                if (data && data.status === "sucesso") {
                    // Alterna a classe .active baseado na resposta real do banco de dados
                    if (data.favoritado) {
                        botao.classList.add("active");
                        // Efeito de pulo (Pop) ao ativar
                        botao.style.transform = "scale(1.2)";
                        setTimeout(() => { 
                            botao.style.transform = ""; 
                        }, 200);
                    } else {
                        botao.classList.remove("active");
                        botao.style.transform = "";
                    }
                }
            })
            .catch(error => {
                console.error("Erro na requisição de favoritos:", error);
            });
        });
    });
});