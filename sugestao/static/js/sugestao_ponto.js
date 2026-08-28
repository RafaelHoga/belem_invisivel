document.getElementById('formsugestaoponto').addEventListener('submit', function(e) {
    e.preventDefault();

    // FormData captura todos os inputs do formulário automaticamente (textos e arquivos)
    const formData = new FormData(this);

    // Captura o CSRF Token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]') ? document.querySelector('[name=csrfmiddlewaretoken]').value : '';
    const feedback = document.getElementById('msgFeedback');

    const urlEnvio = '/sugestao/sugerir/';

    fetch(urlEnvio, {
        method: 'POST',
        headers: {
            // NUNCA defina 'Content-Type' ao usar FormData!
            // O próprio navegador define o 'multipart/form-data' com os limites (boundary) corretos.
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro na resposta do servidor.');
        }
        return response.json();
    })
    .then(data => {
        if (data.sucesso) {
            if (feedback) {
                feedback.innerText = data.mensagem || "Sugestão enviada com sucesso!";
                feedback.style.color = "green";
            } else {
                alert(data.mensagem || "Sugestão enviada com sucesso!");
            }
            this.reset(); // Limpa o formulário e a seleção da imagem em caso de sucesso
        } else {
            if (feedback) {
                feedback.innerText = data.erro || "Houve um erro ao cadastrar a sugestão.";
                feedback.style.color = "red";
            } else {
                alert(data.erro || "Houve um erro ao cadastrar a sugestão.");
            }
        }
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
        if (feedback) {
            feedback.innerText = "Erro de comunicação com o servidor. Tente novamente mais tarde.";
            feedback.style.color = "red";
        }
    });
});