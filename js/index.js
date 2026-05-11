 var map = L.map('map').setView([-1.45502, -48.5024], 13);

 var marker = L.marker([1.455, -48.484]).addTo(map);

 L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

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

