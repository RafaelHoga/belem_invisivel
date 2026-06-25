document.getElementById('formsugestaoponto').addEventListener('submit', function(e) {
    e.preventDefault();

    // Capturando os dados conforme as colunas do seu Banco de Dados
    const dados = {
        nome_ponto_turistico: document.getElementById('nome_ponto').value,
        id_categoria: document.getElementById('id_categoria').value,
        telefone: document.getElementById('telefone').value,
        endereco: document.getElementById('endereco').value,
        numero: document.getElementById('numero').value,
        bairro: document.getElementById('bairro').value,
        cidade: document.getElementById('cidade').value
    };

    console.log("Dados prontos para o banco:", dados);

    // Captura o CSRF Token gerado pelo Django no HTML
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]') ? document.querySelector('[name=csrfmiddlewaretoken]').value : '';

    const feedback = document.getElementById('msgFeedback');

    // Fazendo a requisição assíncrona para a View do Django
    // Substitua '/pontos/sugerir/' pela URL correta configurada no seu urls.py (ou use o atributo action do form se preferir)
    fetch('/pontos/sugerir/', {
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
            // Feedback de sucesso real vindo do Django
            feedback.innerText = data.mensagem || "Ponto turístico cadastrado com sucesso!";
            feedback.style.color = "green";
            
            // Limpar formulário apenas em caso de sucesso
            this.reset();
        } else {
            // Caso o Django retorne erros de validação (ex: formulário inválido)
            feedback.innerText = data.erro || "Houve um erro ao cadastrar o ponto turístico.";
            feedback.style.color = "red";
        }
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
        feedback.innerText = "Erro de comunicação com o servidor. Tente novamente mais tarde.";
        feedback.style.color = "red";
    });
});