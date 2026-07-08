document.getElementById('formsugestaoponto').addEventListener('submit', function(e) {
    e.preventDefault();

    // Referência direta ao formulário para evitar problemas de escopo (this)
    const formulario = e.target;

    // Capturando as variáveis individuais do formulário
    const logradouro = document.getElementById('endereco').value.trim();
    const numero = document.getElementById('numero').value.trim() || 'S/N';
    const bairro = document.getElementById('bairro').value.trim();
    const city = document.getElementById('cidade').value.trim();

    // Formata a string completa de endereço para gravar corretamente no varchar(300) do MySQL
    const enderecoCompleto = `${logradouro}, Nº ${numero}, Bairro: ${bairro} - ${city}`;

    // Capturando os dados do formulário
    const dados = {
        nome_sugestao: document.getElementById('nome_ponto').value.trim(),
        categoria: document.getElementById('id_categoria').value,
        endereco: enderecoCompleto, 
        descricao: document.getElementById('descricao').value.trim(),
        
        // Mantido para compatibilidade ou uso futuro:
        telefone: document.getElementById('telefone').value.trim(),
        numero: numero,
        bairro: bairro,
        cidade: city
    };

    console.log("Dados prontos para o banco:", dados);

    // Captura o CSRF Token de forma segura
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrfToken = csrfInput ? csrfInput.value : '';
    const feedback = document.getElementById('msgFeedback');

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
            formulario.reset(); // CORREÇÃO: Limpa o formulário usando a referência segura
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