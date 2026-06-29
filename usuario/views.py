from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from django.http import JsonResponse
from django.utils import timezone

# Buscando os modelos de seus respectivos apps corretos
from ponto_turistico.models import Favorito, PontoTuristico
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
            SELECT id_ponto_turistico 
            FROM favorito 
            WHERE id_usuario = %s
        """, [id_do_usuario])
        favoritos_ids = [row[0] for row in cursor.fetchall()]
    
    if favoritos_ids:
        meus_favoritos = PontoTuristico.objects.filter(id_ponto_turistico__in=favoritos_ids)
    
    # ==========================================
    # 2. AVALIAÇÕES (SQL Puro)
    # ==========================================
    minhas_avaliacoes = []
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_ponto_turistico, mensagem, estrela, data_avaliacao 
            FROM avaliacao 
            WHERE id_usuario = %s
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
            WHERE id_usuario = %s
        """, [id_do_usuario])
        linhas_sugestoes = cursor.fetchall()

    for linha in linhas_sugestoes:
        minhas_sugestoes.append({
            'nome_sugestao': inline_nome if (inline_nome := linha[0]) else "Sem nome",
            'descricao': linha[1],
            'status': linha[2] if len(linha) > 2 else "Pendente"
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
                id_perfil = 1 if email.lower().endswith('@beleminvisivel.com') else 2

                usuario_temp = Usuario(email=email, nome_usuario=nome)
                usuario_temp.set_password(senha)
                senha_criptografada = usuario_temp.password

                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO usuario (nome_usuario, email, password, data_nascimento, id_perfil, is_superuser, is_staff, is_active)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, [nome, email, senha_criptografada, data_nasc, id_perfil, 0, 0, 1])
                
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('usuario:login')
                
            except Exception as e:
                messages.error(request, f'Erro ao processar o cadastro: {e}')
        else:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')

    return render(request, 'usuario/tela-login.html')


def salvar_avaliacao(request, id_ponto):
    if not request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Você precisa estar logado para avaliar.'}, status=403)
        return redirect('usuario:login')

    if request.method == 'POST':
        nota = request.POST.get('nota_avaliacao')
        comentario = request.POST.get('comentario') or request.POST.get('comentario_texto')

        if nota and nota != "0" and comentario:
            try:
                id_usuario_atual = int(request.user.id_usuario)
                id_ponto_alvo = int(id_ponto)
                nota_num = int(nota)

                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO avaliacao (id_usuario, id_ponto_turistico, estrela, mensagem, data_avaliacao)
                        VALUES (%s, %s, %s, %s, NOW())
                    """, [id_usuario_atual, id_ponto_alvo, nota_num, comentario])
                
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'sucesso'})
                
            except Exception as e:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'error': f'Erro no banco de dados: {str(e)}'}, status=500)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Por favor, selecione uma nota e digite um comentário.'}, status=400)

    return redirect(request.META.get('HTTP_REFERER', '/'))


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from django.http import JsonResponse
from django.utils import timezone

# Buscando os modelos de seus respectivos apps corretos
from ponto_turistico.models import Favorito, PontoTuristico
from usuario.models import Usuario
from sugestao.models import Sugestao

# ... mantenha suas funções home, perfil_usuario, login, cadastro, avaliar existentes ...

def editar_perfil(request):
    """
    Função dedicada para receber os dados do POST de alteração de informações pessoais
    e realizar o UPDATE direto no MySQL legado usando SQL Puro.
    """
    # Garante que apenas usuários logados acessem a lógica de alteração
    if not request.user.is_authenticated:
        return redirect('usuario:login')

    id_usuario_atual = request.user.id_usuario

    if request.method == 'POST':
        novo_nome = request.POST.get('nome_usuario')
        nova_data_nasc = request.POST.get('data_nascimento')

        # Validação simples
        if not novo_nome:
            messages.error(request, "O campo nome não pode ficar vazio.")
            return redirect('usuario:perfil')

        try:
            # --- SQL PURO PARA ATUALIZAR OS DADOS DO USUÁRIO ---
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE usuario 
                    SET nome_usuario = %s, data_nascimento = %s 
                    WHERE id_usuario = %s
                """, [novo_nome, nova_data_nasc if nova_data_nasc else None, id_usuario_atual])
            
            messages.success(request, "Informações atualizadas com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao atualizar no banco legado: {str(e)}")
        
        return redirect('usuario:perfil') # Redireciona de volta para a página de perfil já com os dados novos

    # Se por acaso o usuário acessar GET nessa URL, redireciona para o perfil
    return redirect('usuario:perfil')




def logout_usuario(request):
    logout(request)
    messages.success(request, 'Sessão encerrada com sucesso.')
    return redirect('/')