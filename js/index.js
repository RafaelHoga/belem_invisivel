// FORMULÁRIO

let form = document.getElementById("formContato");

form.addEventListener("submit", function (event) {

  event.preventDefault();

  let nome = document.getElementById("nome").value.trim();
  let email = document.getElementById("email").value.trim();
  let mensagem = document.getElementById("mensagem").value.trim();

  let feedback = document.getElementById("feedback");

  if (nome === "" || email === "" || mensagem === "") {
    feedback.innerText = "Preencha todos os campos!";
    feedback.style.color = "red";
    return;
  }

  feedback.innerText = "Mensagem enviada com sucesso! 🐶";
  feedback.style.color = "green";

  form.reset();
});