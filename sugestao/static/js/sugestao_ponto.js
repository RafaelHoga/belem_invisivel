document.getElementById('formsugestaoponto').addEventListener('submit', function(e) {
    e.preventDefault();

    // Capturando os dados do formulário
    const dados = {
        nome_sugestao: document.getElementById('nome_ponto').value,
        categoria: document.getElementById('id_categoria').value,
        endereco: document.getElementById('endereco').value,
        // Campos extras caso queira usar futuramente no banco:
        telefone: document.getElementById('telefone').value,
        numero: document.getElementById('numero').value,
        bairro: document.getElementById('bairro').value,
        cidade: document.getElementById('cidade').value
    };

    console.log("Dados prontos para o banco:", dados);

    // Captura o CSRF Token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]') ? document.querySelector('[name=csrfmiddlewaretoken]').value : '';
    const feedback = document.getElementById('msgFeedback');

    // AJUSTE: Rota direta com barra final para respeitar o app_name do Django sem dar 404
    const urlEnvio = '/sugestao/sugerir/';

    fetch(urlEnvio, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(dados)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro na resposta do servidor.');
        }
        return response.json();
    })
    .then(data => {
        if (data.sucesso) {
            feedback.innerText = data.mensagem || "Sugestão enviada com sucesso!";
            feedback.style.color = "green";
            this.reset(); // Limpa o formulário em caso de sucesso
        } else {
            feedback.innerText = data.erro || "Houve um erro ao cadastrar a sugestão.";
            feedback.style.color = "red";
        }
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
        feedback.innerText = "Erro de comunicação com o servidor. Tente novamente mais tarde.";
        feedback.style.color = "red";
    });
});