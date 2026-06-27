from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import connection

# Buscando os modelos de seus respectivos apps corretos
from ponto_turistico.models import Favorito, Avaliacao, PontoTuristico
from usuario.models import Usuario
from sugestao.models import Sugestao

def home(request):
    return render(request, 'index.html')


def perfil_usuario(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Por favor, faça o login para acessar o perfil.')
        return redirect('usuario:login')
        
    usuario_logado = request.user
    id_do_usuario = usuario_logado.id_usuario

    # ==========================================
    # 1. FAVORITOS (SQL Puro)
    # ==========================================
    meus_favoritos = []
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT PONTO_TURISTICO_ID_ponto_turistico 
            FROM favorito 
            WHERE USUARIO_ID_usuario = %s
        """, [id_do_usuario])
        favoritos_ids = [row[0] for row in cursor.fetchall()]
    
    if favoritos_ids:
        meus_favoritos = PontoTuristico.objects.filter(id_ponto_turistico__in=favoritos_ids)
    
    # ==========================================
    # 2. AVALIAÇÕES (SQL Puro - data_avaliacao incluída)
    # ==========================================
    minhas_avaliacoes = []
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT PONTO_TURISTICO_ID_ponto_turistico, mensagem, estrela, data_avaliacao 
            FROM avaliacao 
            WHERE USUARIO_ID_usuario = %s
        """, [id_do_usuario])
        linhas_avaliacoes = cursor.fetchall()
        
    for linha in linhas_avaliacoes:
        ponto_id = linha[0]
        ponto_objeto = PontoTuristico.objects.filter(id_ponto_turistico=ponto_id).first()
        
        minhas_avaliacoes.append({
            'ponto_turistico': ponto_objeto,
            'mensagem': linha[1],      
            'estrela': linha[2],       
            'data_avaliacao': linha[3]  
        })

    # ==========================================
    # 3. SUGESTÕES (SQL Puro)
    # ==========================================
    minhas_sugestoes = []
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT nome_sugestao, descricao, status 
            FROM sugestao 
            WHERE USUARIO_ID_usuario = %s
        """, [id_do_usuario])
        linhas_sugestoes = cursor.fetchall()

    for linha in linhas_sugestoes:
        minhas_sugestoes.append({
            'nome_sugestao': linha[0],
            'descricao': linha[1],
            'status': linha[2]
        })
    
    context = {
        'favoritos': meus_favoritos,
        'sugestoes': minhas_sugestoes,
        'avaliacoes': minhas_avaliacoes,
    }
    
    return render(request, 'usuario/tela_perfil_usuario.html', context)


def login_usuario(request):
    if request.method == 'POST':
        email_recebido = request.POST.get('email_usuario')
        senha_recebida = request.POST.get('senha_usuario')

        if email_recebido and senha_recebida:
            try:
                usuario_autenticado = authenticate(request, username=email_recebido, password=senha_recebida)

                if usuario_autenticado is not None:
                    login(request, usuario_autenticado)
                    
                    # Alimenta manualmente as variáveis da sessão para a NAVBAR
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

        if nome and email and senha and data_nasc:
            if Usuario.objects.filter(email=email).exists():
                messages.error(request, 'Este endereço de e-mail já está cadastrado.')
                return render(request, 'usuario/tela-login.html')

            try:
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


def salvar_avaliacao(request, id_ponto):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para avaliar.')
        return redirect('usuario:login')

    if request.method == 'POST':
        nota = request.POST.get('nota_avaliacao')
        comentario = request.POST.get('comentario')

        if nota and nota != "0" and comentario:
            try:
                # SOLUÇÃO USANDO O DJANGO ORM CORRIGIDO:
                # Usamos o sufixo _id para passar o ID numérico diretamente sem disparar erro de instância!
                Avaliacao.objects.create(
                    id_usuario_id=request.user.id_usuario,
                    id_ponto_turistico_id=int(id_ponto),
                    estrela=int(nota),
                    mensagem=comentario
                )
                
                messages.success(request, 'Obrigado! Sua avaliação foi enviada com sucesso.')
            except Exception as e:
                messages.error(request, f'Erro ao salvar avaliação: {e}')
        else:
            messages.error(request, 'Por favor, preencha todos os campos da avaliação.')

    return redirect(request.META.get('HTTP_REFERER', '/'))


def logout_usuario(request):
    logout(request)
    messages.success(request, 'Sessão encerrada com sucesso.')
    return redirect('/')