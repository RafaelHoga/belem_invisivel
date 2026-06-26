from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Buscando os modelos de seus respectivos apps corretos
from ponto_turistico.models import Favorito, Avaliacao
from usuario.models import Usuario
from sugestao.models import Sugestao

def home(request):
    return render(request, 'index.html')


def perfil_usuario(request):
    # CORREÇÃO: Usando a propriedade nativa e segura do Django (vinda do login())
    if not request.user.is_authenticated:
        messages.error(request, 'Por favor, faça o login para acessar o perfil.')
        return redirect('usuario:login')
        
    # Pega a instância do usuário logado diretamente do request
    usuario_logado = request.user
    
    # Consultas utilizando o atributo correto do seu model (id_usuario)
    meus_favoritos = Favorito.objects.filter(id_usuario=usuario_logado.id_usuario).select_related('id_ponto_turistico')
    minhas_sugestoes = Sugestao.objects.filter(id_usuario=usuario_logado.id_usuario)
    minhas_avaliacoes = Avaliacao.objects.filter(id_usuario=usuario_logado.id_usuario).select_related('id_ponto_turistico')
    
    context = {
        'favoritos': meus_favoritos,
        'sugestoes': minhas_sugestoes,
        'avaliacoes': minhas_avaliacoes,
    }
    
    return render(request, 'tela_perfil_usuario.html', context)


def login_usuario(request):
    if request.method == 'POST':
        email_recebido = request.POST.get('email_usuario')
        senha_recebida = request.POST.get('senha_usuario')

        if email_recebido and senha_recebida:
            try:
                usuario_autenticado = authenticate(request, username=email_recebido, password=senha_recebida)

                if usuario_autenticado is not None:
                    # Inicia a sessão nativa criptografada no Django
                    login(request, usuario_autenticado)
                    
                    # CORREÇÃO: Alimenta manualmente as variáveis que a sua NAVBAR atual exige
                    request.session['usuario_id'] = usuario_autenticado.id_usuario
                    request.session['usuario_nome'] = usuario_autenticado.nome_usuario
                    
                    messages.success(request, f'Bem-vindo de volta, {usuario_autenticado.nome_usuario}!')
                    return redirect('/')  
                else:
                    messages.error(request, 'E-mail ou senha incorretos.')
                    
            except Exception as e:
                messages.error(request, f'Erro interno ao processar login: {e}')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')
            
    return render(request, 'usuario/tela-login.html')


# FUNÇÃO DE CADASTRO REFEITA UTILIZANDO O ORM SEGURO (MÉTODO SET_PASSWORD EMBUTIDO)
def cadastro_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome_usuario')
        email = request.POST.get('email_usuario')
        senha = request.POST.get('senha_usuario')
        data_nasc = request.POST.get('data_nascimento')

        if nome and email and senha and data_nasc:
            # Validação preventiva de duplicidade de e-mail no escopo da aplicação
            if Usuario.objects.filter(email=email).exists():
                messages.error(request, 'Este endereço de e-mail já está cadastrado.')
                return render(request, 'usuario/tela-login.html')

            try:
                # Criação segura usando a lógica centralizada no UsuarioManager
                Usuario.objects.create_user(
                    email=email,
                    nome_usuario=nome,
                    password=senha,
                    data_nascimento=data_nasc
                )
                
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('usuario:login')
                
            except Exception as e:
                messages.error(request, f'Erro ao processar o cadastro: {e}')
        else:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')

    return render(request, 'usuario/tela-login.html')


# FUNÇÃO DE LOGIN ADAPTADA AO AUTHENTICATE DO DJANGO (CORRIGE O ERRO DE COLUNA 'SENHA')
def login_usuario(request):
    if request.method == 'POST':
        email_recebido = request.POST.get('email_usuario')
        senha_recebida = request.POST.get('senha_usuario')

        if email_recebido and senha_recebida:
            try:
                # O método authenticate do Django traduz o USERNAME_FIELD ('email') 
                # e faz a verificação matemática comparando o hash criptográfico na coluna 'password'
                usuario_autenticado = authenticate(request, username=email_recebido, password=senha_recebida)

                if usuario_autenticado is not None:
                    # Inicia a sessão nativa criptografada no navegador do cliente
                    login(request, usuario_autenticado)
                    
                    messages.success(request, f'Bem-vindo de volta, {usuario_autenticado.nome_usuario}!')
                    return redirect('/')  
                else:
                    messages.error(request, 'E-mail ou senha incorretos.')
                    
            except Exception as e:
                messages.error(request, f'Erro interno ao processar login: {e}')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')
            
    return render(request, 'usuario/tela-login.html')


# LOGOUT ADAPTADO AO MOTOR NATIVO DO DJANGO
def logout_usuario(request):
    logout(request)  # Limpa os cookies, chaves criptográficas e destrói a sessão atual com segurança
    messages.success(request, 'Sessão encerrada com sucesso.')
    return redirect('/')