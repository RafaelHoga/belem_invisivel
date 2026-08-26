document.addEventListener("DOMContentLoaded", () => {
    const mainContainer = document.getElementById('main-container');
    const signUpButton = document.getElementById('signUp');
    const signInButton = document.getElementById('signIn');
    
    const switchToSignUp = document.getElementById('switchToSignUp');
    const switchToSignIn = document.getElementById('switchToSignIn');
    const signUpContainer = document.querySelector('.sign-up-container');
    const signInContainer = document.querySelector('.sign-in-container');

    // Troca de painéis (Desktop)
    if (signUpButton && signInButton) {
        signUpButton.addEventListener('click', () => mainContainer.classList.add("right-panel-active"));
        signInButton.addEventListener('click', () => mainContainer.classList.remove("right-panel-active"));
    }

    // Troca de painéis (Mobile)
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

    // Visibilidade da Senha
    document.querySelectorAll('.toggle-password').forEach(icon => {
        icon.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            const parentGroup = icon.closest('.input-group');
            const input = parentGroup ? parentGroup.querySelector('input') : null;
            
            if (input) {
                if (input.type === "password") {
                    input.type = "text";
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                } else {
                    input.type = "password";
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }
            }
        });
    });

    // Inicialização do Flatpickr
    if (document.getElementById('cadDataNascimento')) {
        flatpickr("#cadDataNascimento", {
            locale: "pt",
            dateFormat: "Y-m-d",
            altInput: true,
            altFormat: "d/m/Y",
            maxDate: "today",
            disableMobile: "true"
        });
    }

    // Notificações Toast
    const msgDiv = document.getElementById('mensagem');
    if (msgDiv && msgDiv.children.length > 0) {
        const alertaText = msgDiv.innerText.toLowerCase();
        const alertBox = msgDiv.querySelector('.alert-box');

        if (alertaText.includes('cadastrado') || alertaText.includes('ausentes') || alertaText.includes('obrigatorios') || alertaText.includes('cadastro')) {
            if (mainContainer) mainContainer.classList.add("right-panel-active");
            if (signUpContainer && signInContainer && window.innerWidth <= 768) {
                signInContainer.style.display = 'none';
                signUpContainer.style.display = 'block';
            }
        }

        if (alertBox && (alertaText.includes('erro') || alertaText.includes('incorretos') || alertaText.includes('ausentes') || alertaText.includes('já está cadastrado') || alertaText.includes('por favor'))) {
            alertBox.style.backgroundColor = '#e74c3c';
        }

        msgDiv.classList.add('show');
        setTimeout(() => msgDiv.classList.remove('show'), 5000);
    }
});