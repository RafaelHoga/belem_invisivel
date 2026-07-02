from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from django.http import JsonResponse
from django.utils import timezone

# Buscando os modelos de seus respectivos apps corretos
from ponto_turistico.models import Favorito, PontoTuristico
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db import connection
from django.http import JsonResponse
from datetime import datetime

# Buscando os modelos de seus respectivos apps corretos
from ponto_turistico.models import Favorito, Avaliacao, PontoTuristico, Categoria
from usuario.models import Usuario
from sugestao.models import Sugestao

def home(request):
    return render(request, 'index.html')


def perfil_usuario(request):
    # Usando a propriedade nativa e segura do Django (vinda do login())
    if not request.user.is_authenticated:
        messages.error(request, 'Por favor, faça o login para acessar o perfil.')
        return redirect('usuario:login')
        
    usuario_logado = request.user
    id_do_usuario = usuario_logado.id_usuario

    # ==========================================
    # 1. FAVORITOS (SQL Puro - Corrigido para id_ponto_turistico)
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
    # 2. AVALIAÇÕES (SQL Puro - Corrigido para id_ponto_turistico)
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
        ponto_id = line_val if (line_val := linha[0]) else None
        ponto_objeto = PontoTuristico.objects.filter(id_ponto_turistico=ponto_id).first()
        
        minhas_avaliacoes.append({
            'ponto_turistico': ponto_objeto,
            'mensagem': inline_value if (inline_value := linha[1]) else '',      
            'estrela': inline_value if (inline_value := inline_val_star if (inline_val_star := linha[2]) else 0) else 0,       
            'data_avaliacao': linha[3]  
        })

    # ==========================================
    # 3. SUGESTÕES (SQL Puro)
    # 3. SUGESTÕES (SQL Puro - Corrigido para id_usuario)
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
            'nome_sugestao': inline_value if (inline_value := linha[0]) else '',
            'descricao': linha[1],
            'status': linha[2] if len(linha) > 2 else "Pendente"
        })
    
    context = {
        'favoritos': meus_favoritos,
        'favoritos_ids': favoritos_ids,  # Enviando IDs para verificação em locais globais
        'sugestoes': minhas_sugestoes,
        'avaliacoes': minhas_avaliacoes,
    }
    
    return render(request, 'usuario/tela_perfil_usuario.html', context)
    return render(request, 'tela_perfil_usuario.html', context)


@user_passes_test(lambda u: u.is_staff, login_url='usuario:login')
def painel_admin(request):
    # Contadores rápidos em SQL puro para alimentar os cards do Dashboard
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM ponto_turistico")
        total_pontos = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM avaliacao")
        total_avaliacoes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM sugestao WHERE status = 'Pendente'")
        sugestoes_pendentes = cursor.fetchone()[0]

        # BUSCA DE CATEGORIAS
        cursor.execute("SELECT id_categoria, descricao_categoria FROM categoria")
        linhas_categorias = cursor.fetchall()
        
        # ====================================================================
        # CORRIGIDO: Removido ID inexistente e ordenado por data_avaliacao
        # ====================================================================
        cursor.execute("""
            SELECT 
                a.estrela,
                a.mensagem,
                u.nome_usuario,
                p.nome_ponto_turistico,
                p.id_categoria,
                a.id_ponto_turistico,
                a.id_usuario
            FROM avaliacao a
            INNER JOIN usuario u ON a.id_usuario = u.id_usuario
            INNER JOIN ponto_turistico p ON a.id_ponto_turistico = p.id_ponto_turistico
            ORDER BY a.data_avaliacao DESC
        """)
        linhas_avaliacoes = cursor.fetchall()
        
    categories_list = [
        {'id_categoria': linha[0], 'descricao_categoria': inline_val if (inline_val := linha[1]) else ''}
        for linha in linhas_categorias
    ]

    # Tratando o retorno do SQL sem ID único para o formato do template
    avaliacoes_list = []
    for linha in linhas_avaliacoes:
        avaliacoes_list.append({
            'estrela': linha[0],
            'mensagem': linha[1] if linha[1] else '',
            'id_usuario': {
                'username': linha[2],
                'id_usuario': linha[6] # Guardamos o ID do usuário para usar na exclusão se necessário
            },
            'id_ponto_turistico': {
                'nome_ponto_turistico': linha[3],
                'id_ponto_turistico': linha[5], # Guardamos o ID do ponto para usar na exclusão
                'id_categoria': {
                    'id_categoria': linha[4]
                }
            }
        })

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
            
    return render(request, 'tela-login.html')


def cadastro_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome_usuario')
        email = request.POST.get('email_usuario')
        senha = request.POST.get('senha_usuario')
        data_nasc = request.POST.get('data_nascimento')

        if not (nome and email and senha and data_nasc):
            campos_faltantes = []
            if not nome: campos_faltantes.append("Nome")
            if not email: campos_faltantes.append("E-mail")
            if not senha: campos_faltantes.append("Senha")
            if not data_nasc: campos_faltantes.append("Data de Nascimento")
            
            messages.error(request, f'Campos obrigatórios ausentes: {", ".join(campos_faltantes)}.')
            return render(request, 'tela-login.html')

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
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Este endereço de e-mail já está cadastrado.')
            return render(request, 'tela-login.html')

        try:
            if data_nasc and '/' in data_nasc:
                data_nasc = datetime.strptime(data_nasc, '%d/%m/%Y').strftime('%Y-%m-%d')
        except Exception as data_err:
            messages.error(request, 'Formato de data inválido. Use o padrão DD/MM/AAAA ou AAAA-MM-DD.')
            return render(request, 'tela-login.html')

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


def atualizar_foto(request):
    if not request.user.is_authenticated:
        return redirect('usuario:login')

    if request.method == 'POST' and request.FILES.get('nova_foto'):
        usuario = request.user
        
        if usuario.foto_perfil:
            usuario.foto_perfil.delete(save=False)
            
        usuario.foto_perfil = request.FILES['nova_foto']
        usuario.save()
        messages.success(request, 'Foto de perfil updated com sucesso!')
        
    return redirect('usuario:perfil')


def cadastrar_categoria(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao_categoria')
        
        if descricao:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO categoria (descricao_categoria) 
                        VALUES (%s)
                    """, [descricao])
                
                messages.success(request, f'Categoria "{descricao}" cadastrada com sucesso!')
            except Exception as e:
                messages.error(request, f'Erro ao salvar no banco de dados: {e}')
        else:
            messages.error(request, 'O nome da categoria não pode estar vazio.')
            
    return redirect('usuario:painel_admin')


@user_passes_test(lambda u: u.is_staff, login_url='usuario:login')
def excluir_categoria(request, id_categoria):
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM categoria WHERE id_categoria = %s", [id_categoria])
        messages.success(request, 'Categoria excluída com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao excluir categoria do banco de dados: {e}')
        
    return redirect('usuario:painel_admin')


@login_required(login_url='usuario:login')
def alternar_favorito(request, ponto_id):
    if request.method == 'POST':
        id_do_usuario = request.user.id_usuario
        
        with connection.cursor() as cursor:
            # Verifica se já está favoritado
            cursor.execute("""
                SELECT 1 FROM favorito WHERE id_usuario = %s AND id_ponto_turistico = %s
            """, [id_do_usuario, ponto_id])
            existe = cursor.fetchone()
            
            if existe:
                # Remove o favorito
                cursor.execute("""
                    DELETE FROM favorito WHERE id_usuario = %s AND id_ponto_turistico = %s
                """, [id_do_usuario, ponto_id])
                favoritado = False
            else:
                # Adiciona o favorito
                cursor.execute("""
                    INSERT INTO favorito (id_usuario, id_ponto_turistico) VALUES (%s, %s)
                """, [id_do_usuario, ponto_id])
                favoritado = True
                
        return JsonResponse({'status': 'sucesso', 'favoritado': favoritado})
    return JsonResponse({'status': 'erro', 'message': 'Método inválido'}, status=400)