let mainContainer = document.getElementById('main-container');
let signUpButton = document.getElementById('signUp');
let signInButton = document.getElementById('signIn');

// Alternar entre Login e Cadastro
// O JS adiciona ou remove uma etiqueta (classe) no elemento pai.
// O CSS é quem lê essa etiqueta e faz a transição visual.
signUpButton.addEventListener('click', () => mainContainer.classList.add("right-panel-active")); //Coração  () =>(função sem nome)
signInButton.addEventListener('click', () => mainContainer.classList.remove("right-panel-active"));

// Exibir Senha
document.querySelectorAll('.toggle-password').forEach(icon => {
  icon.addEventListener('click', () => {
    let input = document.getElementById(icon.dataset.target);
    let isPassword = input.type === "password";
    input.type = isPassword ? "text" : "password"; // O uso do Operador Ternário é uma ótima oportunidade para ensinar uma forma elegante de escrever if/else.
    icon.classList.toggle('fa-eye');
    icon.classList.toggle('fa-eye-slash');
  });
});

// Sistema de Mensagens
function notify(text, type = 'success') {
  let msgDiv = document.getElementById('mensagem');
  msgDiv.textContent = text;
  msgDiv.style.backgroundColor = type === 'success' ? '#2ecc71' : '#e74c3c';
  msgDiv.classList.add('show');
  setTimeout(() => msgDiv.classList.remove('show'), 3000);
}