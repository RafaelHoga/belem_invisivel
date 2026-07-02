/**
 * GERENCIADOR DE AUTENTICAÇÃO - BELÉM INVISÍVEL (2026)
 * Controla os painéis deslizantes (Desktop) e abas (Mobile), além de alertas.
 */
document.addEventListener("DOMContentLoaded", () => {
    const mainContainer = document.getElementById('main-container');
    const signUpButton = document.getElementById('signUp');
    const signInButton = document.getElementById('signIn');
    
    // Elementos de alternância exclusivos para Mobile
    const switchToSignUp = document.getElementById('switchToSignUp');
    const switchToSignIn = document.getElementById('switchToSignIn');
    const signUpContainer = document.querySelector('.sign-up-container');
    const signInContainer = document.querySelector('.sign-in-container');

    // Alternar entre Login e Cadastro (Desktop)
    if (signUpButton && signInButton) {
        signUpButton.addEventListener('click', () => mainContainer.classList.add("right-panel-active"));
        signInButton.addEventListener('click', () => mainContainer.classList.remove("right-panel-active"));
    }

    // Alternar entre Login e Cadastro (Mobile)
    if (switchToSignUp && switchToSignIn) {
        switchToSignUp.addEventListener('click', () => {
            signInContainer.style.display = 'none';
            signUpContainer.style.display = 'block';
        });

        switchToSignIn.addEventListener('click', () => {
            signUpContainer.style.display = 'none';
            signInContainer.style.display = 'block';
        });
    }

    // Gerenciador de Visibilidade das Senhas (Olhinho)
    document.querySelectorAll('.toggle-password').forEach(icon => {
        icon.addEventListener('click', () => {
            const input = document.getElementById(icon.dataset.target);
            if (input) {
                const isPassword = input.type === "password";
                input.type = isPassword ? "text" : "password";
                
                // Altera as classes do FontAwesome dinamicamente
                icon.classList.toggle('fa-eye');
                icon.classList.toggle('fa-eye-slash');
            }
        });
    });

    // Sistema Dinâmico de Notificação (Django Toast) + Controle de Painel Ativo
    const msgDiv = document.getElementById('mensagem');
    if (msgDiv && msgDiv.children.length > 0) {
        const alertaText = msgDiv.innerText.toLowerCase();
        const alertBox = msgDiv.querySelector('.alert-box');

        // Se a mensagem contiver termos típicos de erro de validação ou cadastro, joga para o painel de cadastro
        if (alertaText.includes('cadastrado') || alertaText.includes('ausentes') || alertaText.includes('obrigatorios') || alertaText.includes('cadastro')) {
            if (mainContainer) {
                mainContainer.classList.add("right-panel-active");
            }
            if (signUpContainer && signInContainer && window.innerWidth <= 768) {
                signInContainer.style.display = 'none';
                signUpContainer.style.display = 'block';
            }
        }

        // Ajusta a cor para vermelho caso seja mensagem de erro/falha
        if (alertBox && (alertaText.includes('erro') || alertaText.includes('incorretos') || alertaText.includes('ausentes') || alertaText.includes('já está cadastrado') || alertaText.includes('por favor'))) {
            alertBox.style.backgroundColor = '#e74c3c';
        }

        // Exibe o toast imediatamente
        msgDiv.classList.add('show');
        setTimeout(() => msgDiv.classList.remove('show'), 5000);
    }
});

/**
 * Função Global para chamadas via Ajax caso implementado futuramente
 */
function notify(text, type = 'success') {
    const msgDiv = document.getElementById('mensagem');
    if (!msgDiv) return;

    msgDiv.innerHTML = `<div class="alert-box">${text}</div>`;
    const alertBox = msgDiv.querySelector('.alert-box');
    
    alertBox.style.backgroundColor = type === 'success' ? '#2ecc71' : '#e74c3c';
    
    msgDiv.classList.add('show');
    setTimeout(() => msgDiv.classList.remove('show'), 5000);
}