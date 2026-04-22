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

