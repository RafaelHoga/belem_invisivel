from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from usuario.models import Usuario

def index(request):
    """View para renderizar a página inicial pública."""
    return render(request, 'index.html')

def autenticacao_view(request):
    """View para lidar com a autenticação do usuário."""
    if request.user.is_authenticated:
        return redirect('index')  # Redireciona para a página inicial se o usuário já estiver autenticado
    
    if request.method == 'POST':
        # Identificar qual formulário foi submetido usando o nome do botão/input de submit
        action = request.POST.get('action')
        
        # ------------ LÓGICA DE LOGIN ------------
        if action == 'login':
            email = request.POST.get('email', '').strip()
            senha = request.POST.get('password', '')
            
            if not email or not senha:
                messages.error(request, 'Por favor, preencha todos os campos.')
                return render(request, 'tela-login.html')
            
            # O Django por padrão autentica usando o 'username', mas nosso modelo usa 'email' como USERNAME_FIELD
            # Como seu formulário pede Email, vamos buscar o username atrelado a esse email.
                
            user = authenticate(request, username=email, password=senha)
            
            if user is not None:
                login(request, user)
                messages.sucess(request, f'Bem-vindo, {user.username}!Bem vindo de volta, {user.first_name or user.username}!')
                return redirect('index')
            else:
                messages.error(request, 'Email ou senha incorretos')
        
        # ------------ LÓGICA DE CADASTRO ------------
        elif action == 'cadastro':
            nome =  request.POST.get('nome', '').strip()
            email = request.POST.get('email', '').strip()
            senha = request.POST.get('password', '')
            
            if not nome or not email or not senha:
                messages.error(request, 'Todos os campos de cadastro são obrigatórios.')
                return render(request, 'login_usuario/tela-login.html')
            
            if Usuario.objects.filter(email=email).exists():
                messages.error(request, 'Já existe um usuário cadastrado com esse email.')
                return render(request, 'login_usuario/tela-login.html')
            
            # Criação do User padrão do Django(Usaremos o emial como username)
            user = Usuario.objects.create_user(
                username=email,
                email=email,
                password=senha,
                nome_usuario=nome,
                data_nascimento=None  # Você pode ajustar isso para pegar a data de nascimento do formulário se desejar
            )
            
            
            # Autentica e loga o usuário automaticamente após se cadastrar
            user_autenticado = authenticate(request, username=email, password=senha)
            if user_autenticado:
                login(request, user_autenticado)
                messages.success(request, 'Conta criada com sucesso! Seja bem-vindo.')
                return redirect('index')
        
        return render(request, 'tela-login.html')
    
# def logout_view(request):
#     """View para realizar o logout seguro do usuário."""
#     logout(request)
#     messages.info(request, 'Você saiu da sua conta com sucesso.')
#     return redirect('index')
