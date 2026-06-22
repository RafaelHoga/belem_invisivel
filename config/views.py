from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from usuario.models import Usuario  # Certifique-se de que o app chama 'usuario'

def index(request):
    """View para renderizar a página inicial pública."""
    return render(request, 'index.html')

def autentificacao_view(request):
    """View para lidar com a autentificação e cadastro do usuário."""
    if request.user.is_authenticated:
        return redirect('index')  # Redireciona para a home se o usuário já estiver logado
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # ------------ LÓGICA DE LOGIN ------------
        if action == 'login':
            email = request.POST.get('email', '').strip()
            senha = request.POST.get('password', '')
            
            if not email or not senha:
                messages.error(request, 'Por favor, preencha todos os campos.')
                return render(request, 'usuario/tela-login.html')
            
            # Autentica usando o e-mail (já configurado como USERNAME_FIELD no models.py)
            user = authenticate(request, username=email, password=senha)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo de volta, {user.nome_usuario}!')
                return redirect('index')
            else:
                messages.error(request, 'E-mail ou senha incorretos.')
                return render(request, 'usuario/tela-login.html')
            
        # ------------ LÓGICA DE CADASTRO ------------
        elif action == 'cadastro':
            nome = request.POST.get('nome', '').strip()
            email = request.POST.get('email', '').strip()
            senha = request.POST.get('password', '')
            
            if not nome or not email or not senha:
                messages.error(request, 'Todos os campos de cadastro são obrigatórios.')
                return render(request, 'usuario/tela-login.html')
            
            if Usuario.objects.filter(email=email).exists():
                messages.error(request, 'Já existe um usuário cadastrado com esse e-mail.')
                return render(request, 'usuario/tela-login.html')
            
            try:
                # Criação usando o seu Custom Manager (que trata a lógica de ADM/Comum automaticamente)
                user = Usuario.objects.create_user(
                    email=email,
                    nome_usuario=nome,
                    password=senha,
                    data_nascimento=None  # Configurado como NULL no banco
                )
                
                # Autentica e efetua o login imediatamente após o cadastro bem-sucedido
                user_autenticado = authenticate(request, username=email, password=senha)
                if user_autenticado:
                    login(request, user_autenticado)
                    messages.success(request, 'Conta criada com sucesso! Seja bem-vindo.')
                    return redirect('index')
                    
            except Exception as e:
                messages.error(request, f'Erro ao processar o cadastro: {e}')
                return render(request, 'usuario/tela-login.html')
        
    return render(request, 'usuario/tela-login.html')
    
def logout_view(request):
    """View para realizar o logout seguro do usuário."""
    logout(request)
    messages.info(request, 'Você saiu da sua conta com sucesso.')
    return redirect('index')