from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime  # Tratamento do formato de data exigido pelo MySQL

# Buscando os modelos de seus respectivos apps corretos
from ponto_turistico.models import Favorito, Avaliacao
from usuario.models import Usuario
from sugestao.models import Sugestao

def home(request):
    return render(request, 'index.html')


def perfil_usuario(request):
    # Usando a propriedade nativa e segura do Django (vinda do login())
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
                # O método authenticate do Django traduz o USERNAME_FIELD ('email') 
                # e faz a verificação matemática comparando o hash criptográfico na coluna 'password'
                usuario_autenticado = authenticate(request, username=email_recebido, password=senha_recebida)

                if usuario_autenticado is not None:
                    # Inicia a sessão nativa criptografada no Django
                    login(request, usuario_autenticado)
                    
                    # Alimenta as variáveis que a sua NAVBAR antiga/atual exige
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


def cadastro_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome_usuario')
        email = request.POST.get('email_usuario')
        senha = request.POST.get('senha_usuario')
        data_nasc = request.POST.get('data_nascimento')

        # === LOG DE DIAGNÓSTICO PARA O SEU TERMINAL ===
        print("\n=== DADOS RECEBIDOS NO FORMULÁRIO ===")
        print(f"Nome: {nome} | E-mail: {email} | Senha: {senha} | Data Nasc: {data_nasc}\n")

        # Verificação explícita campo a campo para evitar falhas silenciosas
        if not (nome and email and senha and data_nasc):
            campos_faltantes = []
            if not nome: campos_faltantes.append("Nome")
            if not email: campos_faltantes.append("E-mail")
            if not senha: campos_faltantes.append("Senha")
            if not data_nasc: campos_faltantes.append("Data de Nascimento")
            
            messages.error(request, f'Campos obrigatórios ausentes: {", ".join(campos_faltantes)}.')
            return render(request, 'usuario/tela-login.html')

        # Validação preventiva de duplicidade de e-mail
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Este endereço de e-mail já está cadastrado.')
            return render(request, 'usuario/tela-login.html')

        # === TRATAMENTO DINÂMICO DO FORMATO DE DATA ===
        try:
            # Se o input HTML enviar no formato BR (DD/MM/AAAA), converte para o padrão MySQL (AAAA-MM-DD)
            if data_nasc and '/' in data_nasc:
                data_nasc = datetime.strptime(data_nasc, '%d/%m/%Y').strftime('%Y-%m-%d')
        except Exception as data_err:
            print(f"!!! ERRO AO CONVERTER DATA DE NASCIMENTO: {data_err} !!!")
            messages.error(request, 'Formato de data inválido. Use o padrão DD/MM/AAAA ou AAAA-MM-DD.')
            return render(request, 'usuario/tela-login.html')

        try:
            # Criação utilizando a lógica centralizada no UsuarioManager
            Usuario.objects.create_user(
                email=email,
                nome_usuario=nome,
                password=senha,
                data_nascimento=data_nasc
            )
            
            print(">>> SUCESSO: Usuário registrado no MySQL Workbench! <<<")
            messages.success(request, 'Cadastro realizado com sucesso! Faça seu login.')
            return redirect('usuario:login')
            
        except Exception as e:
            # === PEGA O ERRO EXATO DIRETO DO DRIVER MYSQL NO SEU TERMINAL ===
            print(f"\n!!! ERRO CRÍTICO ENVIADO PELO BANCO DE DADOS: {e} !!!\n")
            messages.error(request, f'Erro ao processar o cadastro no banco: {e}')
            return render(request, 'usuario/tela-login.html')

    # Se a requisição for GET (carregamento inicial da página)
    return render(request, 'usuario/tela-login.html')


def logout_usuario(request):
    logout(request)  # Limpa os cookies e destrói a sessão atual com segurança
    messages.success(request, 'Sessão encerrada com sucesso.')
    return redirect('/')


def atualizar_foto(request):
    """Nova view responsável por receber o arquivo de imagem do formulário e salvar no banco."""
    if not request.user.is_authenticated:
        return redirect('usuario:login')

    if request.method == 'POST' and request.FILES.get('nova_foto'):
        usuario = request.user
        
        # Remove fisicamente a foto antiga do computador para evitar arquivos acumulados sem uso
        if usuario.foto_perfil:
            usuario.foto_perfil.delete(save=False)
            
        usuario.foto_perfil = request.FILES['nova_foto']
        usuario.save()
        messages.success(request, 'Foto de perfil atualizada com sucesso!')
        
    return redirect('usuario:perfil')