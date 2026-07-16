from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime

# Models
from ponto_turistico.models import Favorito, Avaliacao, PontoTuristico, Categoria
from usuario.models import Usuario
from sugestao.models import Sugestao


def home(request):
    """Página inicial pública"""
    return render(request, 'index.html')


@login_required
def perfil_usuario(request):
    """Exibe o perfil do usuário com favoritos, avaliações e sugestões"""
    usuario_logado = request.user
    
    # 1. FAVORITOS (usando ORM com select_related para performance)
    meus_favoritos = PontoTuristico.objects.filter(
        ponto_favoritos_set__id_usuario=usuario_logado
    ).select_related('categoria')
    
    favoritos_ids = list(meus_favoritos.values_list('id_ponto_turistico', flat=True))
    
    # 2. AVALIAÇÕES (usando ORM com select_related)
    minhas_avaliacoes_qs = Avaliacao.objects.filter(
        id_usuario=usuario_logado
    ).select_related('id_ponto_turistico').order_by('-data_avaliacao')
    
    minhas_avaliacoes = [
        {
            'ponto_turistico': avaliacao.id_ponto_turistico,
            'mensagem': avaliacao.mensagem,
            'estrela': avaliacao.estrela,
            'data_avaliacao': avaliacao.data_avaliacao
        }
        for avaliacao in minhas_avaliacoes_qs
    ]
    
    # 3. SUGESTÕES (usando ORM)
    minhas_sugestoes_qs = Sugestao.objects.filter(id_usuario=usuario_logado)
    
    minhas_sugestoes = [
        {
            'nome_sugestao': sugestao.nome_sugestao or "Sem nome",
            'descricao': sugestao.descricao,
            'status': sugestao.status if hasattr(sugestao, 'status') else "Pendente"
        }
        for sugestao in minhas_sugestoes_qs
    ]
    
    context = {
        'favoritos': meus_favoritos,
        'favoritos_ids': favoritos_ids,
        'sugestoes': minhas_sugestoes,
        'avaliacoes': minhas_avaliacoes,
    }
    
    return render(request, 'usuario/tela_perfil_usuario.html', context)


@user_passes_test(lambda u: u.is_staff, login_url='usuario:login')
def painel_admin(request):
    """Painel administrativo com contadores e listagens"""
    # Contadores usando ORM (mais eficiente que SQL puro)
    total_pontos = PontoTuristico.objects.count()
    total_avaliacoes = Avaliacao.objects.count()
    sugestoes_pendentes = Sugestao.objects.filter(status='Pendente').count()
    
    # Categorias
    categories_list = list(Categoria.objects.values('id_categoria', 'descricao_categoria'))
    
    # Avaliações com dados relacionados (usando select_related para performance)
    avaliacoes_qs = Avaliacao.objects.select_related(
        'id_usuario', 'id_ponto_turistico', 'id_ponto_turistico__categoria'
    ).order_by('-data_avaliacao')
    
    avaliacoes_list = [
        {
            'estrela': avaliacao.estrela,
            'mensagem': avaliacao.mensagem or '',
            'id_usuario': {
                'username': avaliacao.id_usuario.nome_usuario,
                'id_usuario': avaliacao.id_usuario.id_usuario
            },
            'id_ponto_turistico': {
                'nome_ponto_turistico': avaliacao.id_ponto_turistico.nome_ponto_turistico,
                'id_ponto_turistico': avaliacao.id_ponto_turistico.id_ponto_turistico,
                'id_categoria': {
                    'id_categoria': avaliacao.id_ponto_turistico.categoria.id_categoria
                }
            }
        }
        for avaliacao in avaliacoes_qs
    ]
    
    # Locais completos e sugestões
    locais_completos = PontoTuristico.objects.select_related('categoria').all()
    lista_sugestoes = Sugestao.objects.all()
    
    context = {
        'total_pontos': total_pontos,
        'total_avaliacoes': total_avaliacoes,
        'sugestoes_pendentes': sugestoes_pendentes,
        'categories_list': categories_list,
        'locais_cadastrados': locais_completos,
        'sugestoes': lista_sugestoes,
        'avaliacoes_list': avaliacoes_list,
    }
    return render(request, 'usuario/painel_admin.html', context)


def login_usuario(request):
    """Autenticação de usuário"""
    if request.method == 'POST':
        email_recebido = request.POST.get('email_usuario')
        senha_recebida = request.POST.get('senha_usuario')

        if email_recebido and senha_recebida:
            try:
                usuario_autenticado = authenticate(
                    request, 
                    username=email_recebido, 
                    password=senha_recebida
                )

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
            
    return render(request, 'tela-login.html')


def cadastro_usuario(request):
    """Cadastro de novo usuário"""
    if request.method == 'POST':
        nome = request.POST.get('nome_usuario')
        email = request.POST.get('email_usuario')
        senha = request.POST.get('senha_usuario')
        data_nasc = request.POST.get('data_nascimento')

        # 1. Validação de campos obrigatórios
        if not (nome and email and senha and data_nasc):
            campos_faltantes = []
            if not nome: campos_faltantes.append("Nome")
            if not email: campos_faltantes.append("E-mail")
            if not senha: campos_faltantes.append("Senha")
            if not data_nasc: campos_faltantes.append("Data de Nascimento")
            
            messages.error(request, f'Campos obrigatórios ausentes: {", ".join(campos_faltantes)}.')
            return render(request, 'tela-login.html')

        # 2. Verifica se o e-mail já existe
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Este endereço de e-mail já está cadastrado.')
            return render(request, 'tela-login.html')

        # 3. Tratamento e formatação da data de nascimento
        try:
            if '/' in data_nasc:
                data_nasc = datetime.strptime(data_nasc, '%d/%m/%Y').strftime('%Y-%m-%d')
        except Exception:
            messages.error(request, 'Formato de data inválido. Use o padrão DD/MM/AAAA ou AAAA-MM-DD.')
            return render(request, 'tela-login.html')

        # 4. Criação do Usuário usando o manager customizado
        try:
            Usuario.objects.create_user(
                email=email,
                nome_usuario=nome,
                password=senha,
                data_nascimento=data_nasc
            )
            messages.success(request, 'Cadastro realizado com sucesso! Faça seu login.')
            return redirect('usuario:login')
            
        except Exception as e:
            messages.error(request, f'Erro ao processar o cadastro no banco: {e}')
            return render(request, 'tela-login.html')

    return render(request, 'tela-login.html')


@login_required
def salvar_avaliacao(request, id_ponto):
    """Salva avaliação de um ponto turístico via POST"""
    if request.method == 'POST':
        nota = request.POST.get('nota_avaliacao')
        comentario = request.POST.get('comentario') or request.POST.get('comentario_texto')

        if nota and nota != "0" and comentario:
            try:
                # Usando ORM ao invés de SQL puro
                Avaliacao.objects.create(
                    id_usuario=request.user,
                    id_ponto_turistico_id=id_ponto,
                    estrela=int(nota),
                    mensagem=comentario.strip()
                )
                
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'sucesso'})
                
            except Exception as e:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'error': f'Erro ao salvar avaliação: {str(e)}'}, status=500)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Por favor, selecione uma nota e digite um comentário.'}, status=400)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def editar_perfil(request):
    """Atualiza informações pessoais do usuário"""
    if request.method == 'POST':
        novo_nome = request.POST.get('nome_usuario')
        nova_data_nasc = request.POST.get('data_nascimento')

        if not novo_nome:
            messages.error(request, "O campo nome não pode ficar vazio.")
            return redirect('usuario:perfil')

        try:
            # Usando ORM ao invés de SQL puro
            usuario = request.user
            usuario.nome_usuario = novo_nome
            
            if nova_data_nasc:
                # Formata a data se necessário
                if '/' in nova_data_nasc:
                    nova_data_nasc = datetime.strptime(nova_data_nasc, '%d/%m/%Y').strftime('%Y-%m-%d')
                usuario.data_nascimento = nova_data_nasc
            else:
                usuario.data_nascimento = None
            
            usuario.save()
            messages.success(request, "Informações atualizadas com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao atualizar informações: {str(e)}")
        
        return redirect('usuario:perfil')

    return redirect('usuario:perfil')


def logout_usuario(request):
    """Encerra a sessão do usuário"""
    logout(request)  
    messages.success(request, 'Sessão encerrada com sucesso.')
    return redirect('/')


@login_required
def atualizar_foto(request):
    """Atualiza a foto de perfil do usuário"""
    if request.method == 'POST' and request.FILES.get('nova_foto'):
        usuario = request.user
        
        if usuario.foto_perfil:
            usuario.foto_perfil.delete(save=False)
            
        usuario.foto_perfil = request.FILES['nova_foto']
        usuario.save()
        messages.success(request, 'Foto de perfil atualizada com sucesso!')
        
    return redirect('usuario:perfil')


@user_passes_test(lambda u: u.is_staff, login_url='usuario:login')
def cadastrar_categoria(request):
    """Cadastra nova categoria (apenas staff)"""
    if request.method == 'POST':
        descricao = request.POST.get('descricao_categoria')
        
        if descricao:
            try:
                # Usando ORM ao invés de SQL puro
                Categoria.objects.create(descricao_categoria=descricao)
                messages.success(request, f'Categoria "{descricao}" cadastrada com sucesso!')
            except Exception as e:
                messages.error(request, f'Erro ao salvar categoria: {e}')
        else:
            messages.error(request, 'O nome da categoria não pode estar vazio.')
            
    return redirect('usuario:painel_admin')


@user_passes_test(lambda u: u.is_staff, login_url='usuario:login')
def excluir_categoria(request, id_categoria):
    """Exclui categoria (apenas staff)"""
    try:
        # Usando ORM ao invés de SQL puro
        categoria = get_object_or_404(Categoria, id_categoria=id_categoria)
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao excluir categoria: {e}')
        
    return redirect('usuario:painel_admin')


@login_required
def alternar_favorito(request, ponto_id):
    """Adiciona ou remove ponto turístico dos favoritos via AJAX"""
    if request.method == 'POST':
        try:
            ponto = get_object_or_404(PontoTuristico, id_ponto_turistico=ponto_id)
            
            # Usando ORM ao invés de SQL puro
            favorito_existente = Favorito.objects.filter(
                id_usuario=request.user, 
                id_ponto_turistico=ponto
            )
            
            if favorito_existente.exists():
                favorito_existente.delete()
                favoritado = False
            else:
                Favorito.objects.create(
                    id_usuario=request.user, 
                    id_ponto_turistico=ponto
                )
                favoritado = True
                
            return JsonResponse({'status': 'sucesso', 'favoritado': favoritado})
        except Exception as e:
            return JsonResponse({'error': f'Erro ao processar favorito: {str(e)}'}, status=500)
    
    return JsonResponse({'status': 'erro', 'message': 'Método inválido'}, status=400)