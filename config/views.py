from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Se você precisar importar o modelo Usuario dentro das suas views de autenticação:
from usuario.models import Usuario 

def autentificacao_view(request):
    """
    Sua view de login atual. 
    (Cole aqui a lógica interna que você já tinha desenvolvido para autenticar o usuário)
    """
    if request.method == 'POST':
        # Exemplo da lógica que deve estar aqui dentro:
        email = request.POST.get('email')
        senha = request.POST.get('password')
        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "E-mail ou senha incorretos.")
            
    return render(request, 'usuario/tela-login.html') # Ajuste o caminho do template se necessário


def logout_view(request):
    """
    Sua view de logout.
    """
    logout(request)
    return redirect('usuario:login')  # Redireciona para a página de perfil após logout (ajuste se necessário)