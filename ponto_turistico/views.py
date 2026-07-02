from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import connection
from .models import PontoTuristico, Categoria

# ==========================================
# FUNÇÃO AUXILIAR (FAVORITOS DO USUÁRIO)
# ==========================================
def obter_favoritos_usuario(request):
    """Retorna uma lista de IDs de pontos turísticos favoritados pelo usuário logado"""
    if request.user.is_authenticated:
        id_do_usuario = request.user.id_usuario
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_ponto_turistico 
                FROM favorito 
                WHERE id_usuario = %s
            """, [id_do_usuario])
            return [row[0] for row in cursor.fetchall()]
    return []

# ==========================================
# VIEWS PÚBLICAS DO SITE
# ==========================================

def tela_turismo(request):
    """Exibe a página pública com a listagem de Pontos Turísticos"""
    locais = PontoTuristico.objects.filter(categoria__descricao_categoria="Turismo")
    favoritos_ids = obter_favoritos_usuario(request)
    
    context = {
        'locais': locais,
        'favoritos_ids': favoritos_ids
    }
    return render(request, 'usuario/tela-turismo.html', context)


def tela_hoteis(request):
    """Exibe a página pública com a listagem de Hotéis"""
    locais = PontoTuristico.objects.filter(categoria__descricao_categoria="Hotel")
    favoritos_ids = obter_favoritos_usuario(request)
    
    context = {
        'locais': locais,
        'favoritos_ids': favoritos_ids
    }
    return render(request, 'usuario/tela-hoteis.html', context)


def tela_restaurante(request):
    """Exibe a página pública com a listagem de Restaurantes"""
    locais = PontoTuristico.objects.filter(categoria__descricao_categoria="Restaurante")
    favoritos_ids = obter_favoritos_usuario(request)
    
    context = {
        'locais': locais,
        'favoritos_ids': favoritos_ids
    }
    return render(request, 'usuario/tela-restaurante.html', context)


from django.http import JsonResponse  # Certifique-se de ter esse import no topo do arquivo

def detalhe_local(request, id_ponto):
    """Exibe os detalhes específicos de um local e processa suas avaliações de forma dinâmica"""
    local = get_object_or_404(PontoTuristico, id_ponto_turistico=id_ponto)
    
    # =======================================================
    # 1. TRATAMENTO DO ENVIO DA AVALIAÇÃO VIA AJAX (POST)
    # =======================================================
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Você precisa estar logado para avaliar.'}, status=403)

        nota = request.POST.get('nota_avaliacao')
        comentario = request.POST.get('comentario_texto')
        id_do_usuario = request.user.id_usuario 

        if not nota or not comentario or nota == '0':
            return JsonResponse({'error': 'Campos obrigatórios ausentes.'}, status=400)

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO avaliacao (id_ponto_turistico, id_usuario, mensagem, estrela)
                    VALUES (%s, %s, %s, %s)
                """, [id_ponto, id_do_usuario, comentario.strip(), int(nota)])
            
            return JsonResponse({'success': True}, status=200)
            
        except Exception as e:
            print(f"Erro ao salvar avaliação no MySQL: {e}")
            return JsonResponse({'error': 'Erro interno ao salvar no banco de dados.'}, status=500)

    # =======================================================
    # 2. SELEÇÃO DO TEMPLATE CORRETO COM BASE NO ID (GET)
    # =======================================================
    # Mapeia o ID do banco de dados para o arquivo HTML correspondente
    mapeamento_templates = {
        1: 'lugares_turisticos/lugares-pop/tela-estacao-docas.html',
        2: 'lugares_turisticos/lugares-pop/tela-ilha-de-cotijuba.html',
        5: 'lugares_turisticos/lugares-pop/tela-ilha-combu.html',
        6: 'hoteis/tela-hotel-ibis.html',
        # Adicione os outros locais aqui conforme os IDs do banco, por exemplo:
        
    }

    # Se o ID não estiver no mapeamento, usa um template genérico padrão
    template_escolhido = mapeamento_templates.get(id_ponto, 'usuario/detalhes-local.html')

    # Lógica de Favorito
    favoritado = False
    if request.user.is_authenticated:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 1 FROM favorito 
                WHERE id_usuario = %s AND id_ponto_turistico = %s
            """, [request.user.id_usuario, id_ponto])
            favoritado = cursor.fetchone() is not None

    context = {
        'local': local,
        'favoritado': favoritado
    }
    return render(request, template_escolhido, context)

# ==========================================
# VIEWS ADMINISTRATIVAS (CRUD)
# ==========================================

def salvar_local(request, id_ponto=None):
    """Cria ou atualiza qualquer Ponto Turístico, Hotel ou Restaurante"""
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'Acesso negado.')
        return redirect('usuario:login')

    ponto = get_object_or_404(PontoTuristico, id_ponto_turistico=id_ponto) if id_ponto else None

    if request.method == 'POST':
        nome = request.POST.get('nome_ponto_turistico')
        telefone = request.POST.get('telefone')
        descricao = request.POST.get('descricao')
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade', 'Belém')
        imagem_url = request.POST.get('imagem_url')
        latitude = request.POST.get('latitude') or None
        longitude = request.POST.get('longitude') or None
        horario = request.POST.get('horario_funcionamento')
        id_categoria = request.POST.get('id_categoria')

        categoria_obj = get_object_or_404(Categoria, id_categoria=id_categoria)

        if ponto:
            ponto.nome_ponto_turistico = nome
            ponto.telefone = telefone
            ponto.descricao = descricao
            ponto.rua = rua
            ponto.bairro = bairro
            ponto.cidade = city if (city := cidade) else 'Belém'
            ponto.imagem_url = imagem_url
            ponto.latitude = latitude
            ponto.longitude = longitude
            ponto.horario_funcionamento = horario
            ponto.categoria = categoria_obj
            ponto.save()
            messages.success(request, f'"{nome}" atualizado com sucesso!')
        else:
            PontoTuristico.objects.create(
                nome_ponto_turistico=nome,
                telefone=telefone,
                descricao=descricao,
                rua=rua,
                bairro=bairro,
                cidade=cidade,
                imagem_url=imagem_url,
                latitude=latitude,
                longitude=longitude,
                horario_funcionamento=horario,
                categoria=categoria_obj
            )
            messages.success(request, f'"{nome}" cadastrado com sucesso!')

    return redirect('usuario:painel_admin')


def excluir_local(request, id_ponto):
    """Remove permanentemente o local do banco de dados"""
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'Acesso negado.')
        return redirect('usuario:login')

    if request.method == 'POST':
        ponto = get_object_or_404(PontoTuristico, id_ponto_turistico=id_ponto)
        nome = ponto.nome_ponto_turistico
        ponto.delete()
        messages.success(request, f'"{nome}" foi excluído com sucesso.')

    return redirect('usuario:painel_admin')