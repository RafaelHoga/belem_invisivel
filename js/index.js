// MENU HAMBURGUER

let hamburguer = document.getElementById("hamburguer");
let menu = document.getElementById("menu");

hamburguer.addEventListener("click", function () {

  menu.classList.toggle("active");

  // Troca ícone
  if (menu.classList.contains("active")) {
    hamburguer.innerText = "✖";
  } else {
    hamburguer.innerText = "☰";
  }
});


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