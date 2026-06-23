from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .services import criar_usuario


def home(request):
    """Página inicial"""
    return render(request, 'index.html')


def autentificacao_view(request):
    """
    View UNIFICADA que trata LOGIN e CADASTRO na mesma tela.
    """
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        acao = request.POST.get('action')
        
        if acao == 'cadastro':
            return _processar_cadastro(request)
        elif acao == 'login':
            return _processar_login(request)
        else:
            messages.error(request, 'Ação inválida.')
    
    # CORREÇÃO: Path completo do template
    return render(request, 'usuario/tela-login.html')


def _processar_cadastro(request):
    """
    Processa o formulário de CADASTRO.
    """
    nome_usuario = request.POST.get('nome_usuario', '').strip()
    email = request.POST.get('email', '').strip()
    senha = request.POST.get('password', '')
    data_nascimento = request.POST.get('data_nascimento') or None
    
    if not nome_usuario or not email or not senha:
        messages.error(request, 'Preencha todos os campos obrigatórios.')
        return render(request, 'usuario/tela-login.html')  # CORREÇÃO
    
    if len(senha) < 6:
        messages.error(request, 'A senha deve ter no mínimo 6 caracteres.')
        return render(request, 'usuario/tela-login.html')  # CORREÇÃO
    
    try:
        usuario = criar_usuario(
            email=email,
            nome_usuario=nome_usuario,
            senha=senha,
            data_nascimento=data_nascimento
        )
        
        messages.success(
            request,
            f'Cadastro realizado com sucesso! Bem-vindo(a), {usuario.nome_usuario}.'
        )
        
        login(request, usuario)
        return redirect('index')
        
    except ValueError as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, 'Erro ao realizar cadastro. Tente novamente.')
    
    return render(request, 'usuario/tela-login.html')  # CORREÇÃO


def _processar_login(request):
    """
    Processa o formulário de LOGIN.
    """
    email = request.POST.get('email', '').strip()
    senha = request.POST.get('password', '')
    
    if not email or not senha:
        messages.error(request, 'Preencha e-mail e senha.')
        return render(request, 'usuario/tela-login.html')  # CORREÇÃO
    
    usuario = authenticate(request, username=email, password=senha)
    
    if usuario is not None:
        login(request, usuario)
        messages.success(request, f'Bem-vindo(a), {usuario.nome_usuario}!')
        return redirect('index')
    else:
        messages.error(request, 'E-mail ou senha inválidos.')
    
    return render(request, 'usuario/tela-login.html')  # CORREÇÃO


def logout_view(request):
    """Realiza o logout do usuário"""
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('index')


@login_required(login_url='usuario:login')
def perfil_view(request):
    """Exibe o perfil do usuário logado"""
    # CORREÇÃO: Path completo do template
    return render(request, 'usuario/tela_perfil_usuario.html')