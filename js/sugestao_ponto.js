document.getElementById('formsugestaoPonto').addEventListener('submit', function(e) {
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

    // Simulação de feedback
    const feedback = document.getElementById('msgFeedback');
    feedback.innerText = "Ponto turístico cadastrado com sucesso!";
    feedback.style.color = "green";

    // Limpar formulário
    this.reset();
});
