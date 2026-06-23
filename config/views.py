from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from usuario.models import Usuario 

def autentificacao_view(request):
    if request.method == 'POST':
        acao = request.POST.get('action')

        # --- LÓGICA DE CADASTRO ---
        if acao == 'cadastro':
            nome = request.POST.get('nome_usuario')
            email = request.POST.get('email')
            senha = request.POST.get('password')
            data_nasc = request.POST.get('data_nascimento')

            # Verifica se o e-mail já está em uso
            if Usuario.objects.filter(email=email).exists():
                messages.error(request, "Este e-mail já está cadastrado.")
                return render(request, 'usuario/tela-login.html')

            try:
                # Cria o usuário usando o UserManager customizado
                Usuario.objects.create_user(
                    email=email,
                    nome_usuario=nome,
                    password=senha,
                    data_nascimento=data_nasc if data_nasc else None
                )
                messages.success(request, "Cadastro realizado com sucesso! Faça seu login.")
            except Exception as e:
                messages.error(request, f"Erro ao cadastrar: {e}")
            
            return render(request, 'usuario/tela-login.html')

        # --- LÓGICA DE LOGIN ---
        elif acao == 'login':
            email = request.POST.get('email')
            senha = request.POST.get('password')
            
            # O Django exige o argumento nomeado 'username', mas passamos a variável 'email' nele
            user = authenticate(request, username=email, password=senha)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Bem-vindo, {user.nome_usuario}!")
                return redirect('index')
            else:
                messages.error(request, "E-mail ou senha incorretos.")
                
    return render(request, 'usuario/tela-login.html')

def logout_view(request):
    logout(request)
    return redirect('usuario:login')