document.addEventListener("DOMContentLoaded", () => {
    const botoesFavorito = document.querySelectorAll(".favorito");

    // Função robusta para obter o CSRF Token do cookie (Padrão oficial do Django)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    botoesFavorito.forEach(botao => {
        botao.addEventListener("click", async (e) => {
            e.preventDefault();
            
            const pontoId = botao.getAttribute("data-id");
            if (!pontoId) {
                console.error("Erro: ID do ponto turístico não encontrado no botão.");
                return;
            }

            // Rota definitiva baseada no config/urls.py (app ponto_turistico incluído em 'turismo/')
            const urlFinal = `/turismo/favorito/${pontoId}/`;
            const csrftoken = getCookie('csrftoken');

            try {
                const response = await fetch(urlFinal, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrftoken,
                        "Content-Type": "application/json",
                        "X-Requested-With": "XMLHttpRequest" // Identifica a requisição como AJAX no Django
                    },
                });

                // Tratamento de não autenticado (401) ou proibido (403)
                if (response.status === 401 || response.status === 403) {
                    alert("Você precisa estar logado para favoritar!");
                    window.location.href = "/usuario/login/"; 
                    return;
                }

                // Tratamento de outros erros de servidor
                if (!response.ok) {
                    throw new Error(`Erro no servidor: ${response.status}`);
                }

                const data = await response.json();

                const icone = botao.querySelector('i');

                // Lógica de UI baseada nos retornos da view toggle_favorito
                if (data.status === 'adicionado' || data.status === 'sucesso') {
                    botao.classList.add("active");
                    icone.classList.remove("fa-regular", "far");
                    icone.classList.add("fa-solid", "fas");
                    
                    // Feedback visual de clique (animação)
                    botao.style.transform = "scale(1.2)";
                    setTimeout(() => botao.style.transform = "scale(1)", 200);
                    
                } else if (data.status === 'removido') {
                    botao.classList.remove("active");
                    icone.classList.remove("fa-solid", "fas");
                    icone.classList.add("fa-regular", "far");
                    
                    // Feedback visual de clique (animação)
                    botao.style.transform = "scale(0.9)";
                    setTimeout(() => botao.style.transform = "scale(1)", 200);
                }

            } catch (error) {
                console.error("Erro ao processar favorito:", error);
                alert("Ocorreu um erro de conexão ao processar sua solicitação. Tente novamente.");
            }
        });
    });
});