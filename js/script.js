    const form = document.getElementById("formContato");

    window.addEventListener("load", () => {
    const dados = JSON.parse(localStorage.getItem("contato"));

    if (dados) {
        document.getElementById("nome").value = dados.nome || "";
        document.getElementById("email").value = dados.email || "";
        document.getElementById("telefone").value = dados.telefone || "";
        document.getElementById("mensagem").value = dados.mensagem || "";
    }
    });

    form.addEventListener("submit", function(e) {
    e.preventDefault();

    const nome = document.getElementById("nome");
    const email = document.getElementById("email");
    const telefone = document.getElementById("telefone");
    const mensagem = document.getElementById("mensagem");
    const status = document.getElementById("status");

    let valido = true;

    document.querySelectorAll(".erro").forEach(e => e.innerText = "");

    if (nome.value.trim().length < 3) {
        nome.nextElementSibling.innerText = "Nome inválido";
        valido = false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.value)) {
        email.nextElementSibling.innerText = "Email inválido";
        valido = false;
    }

    if (telefone.value.trim().length < 10) {
        telefone.nextElementSibling.innerText = "Telefone inválido";
        valido = false;
    }

    if (mensagem.value.trim().length < 10) {
        mensagem.nextElementSibling.innerText = "Mensagem muito curta";
        valido = false;
    }

    if (!valido) return;

    const dados = {
        nome: nome.value,
        email: email.value,
        telefone: telefone.value,
        mensagem: mensagem.value
    };

    localStorage.setItem("contato", JSON.stringify(dados));

    status.innerText = "Mensagem salva no navegador!";
    form.reset();
    });