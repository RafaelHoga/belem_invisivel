from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import PontoTuristico, Categoria, Favorito, Avaliacao

# ==========================================
# FUNÇÃO AUXILIAR (FAVORITOS DO USUÁRIO)
# ==========================================
def obter_favoritos_usuario(request):
    """Retorna uma lista de IDs de pontos turísticos favoritados pelo usuário logado usando ORM"""
    if request.user.is_authenticated:
        return list(Favorito.objects.filter(id_usuario=request.user).values_list('id_ponto_turistico_id', flat=True))
    return []


# ==========================================
# VIEWS DE INTERAÇÃO (AJAX)
# ==========================================

@login_required
@require_POST
def toggle_favorito(request, id_ponto):
    """Adiciona ou remove o ponto turístico dos favoritos do usuário autenticado (Unificada)"""
    ponto = get_object_or_404(PontoTuristico, id_ponto_turistico=id_ponto)
    
    try:
        favoritos_existentes = Favorito.objects.filter(id_usuario=request.user, id_ponto_turistico=ponto)
        
        if favoritos_existentes.exists():
            favoritos_existentes.delete()
            return JsonResponse({'status': 'removido', 'favoritado': False}, status=200)
        
        Favorito.objects.create(id_usuario=request.user, id_ponto_turistico=ponto)
        return JsonResponse({'status': 'adicionado', 'favoritado': True}, status=200)

    except Exception as e:
        print(f"\n--- ERRO CRÍTICO NO BANCO DE DADOS (Favorito): {e} ---\n")
        return JsonResponse({'error': 'Erro interno ao processar favorito.'}, status=500)


# ==========================================
# VIEWS PÚBLICAS DO SITE
# ==========================================

def tela_turismo(request):
    """Exibe a página pública com a listagem de Pontos Turísticos"""
    locais = PontoTuristico.objects.filter(categoria__descricao_categoria="Turismo")
    context = {
        'locais': locais,
        'favoritos_ids': obter_favoritos_usuario(request)
    }
    return render(request, 'usuario/tela-turismo.html', context)


def tela_hoteis(request):
    """Exibe a página pública com a listagem de Hotéis"""
    locais = PontoTuristico.objects.filter(categoria__descricao_categoria="Hotel")
    context = {
        'locais': locais,
        'favoritos_ids': obter_favoritos_usuario(request)
    }
    return render(request, 'usuario/tela-hoteis.html', context)


def tela_restaurante(request):
    """Exibe a página pública com a listagem de Restaurantes"""
    locais = PontoTuristico.objects.filter(categoria__descricao_categoria="Restaurante")
    context = {
        'locais': locais,
        'favoritos_ids': obter_favoritos_usuario(request)
    }
    return render(request, 'usuario/tela-restaurante.html', context)


def detalhe_local(request, id_ponto):
    """Exibe os detalhes específicos de um local e gerencia avaliações via AJAX"""
    local = get_object_or_404(PontoTuristico, id_ponto_turistico=id_ponto)
    
    # 1. TRATAMENTO DO ENVIO DA AVALIAÇÃO VIA AJAX (POST)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Você precisa estar logado para avaliar.'}, status=403)

        nota = request.POST.get('nota_avaliacao')
        comentario = request.POST.get('comentario_texto')

        if not nota or not comentario or nota == '0':
            return JsonResponse({'error': 'Campos obrigatórios ausentes.'}, status=400)

        try:
            # Substituído SQL Bruto pelo ORM do Django (Mais seguro e legível)
            Avaliacao.objects.create(
                id_ponto_turistico_id=id_ponto,
                id_usuario_id=request.user.id_usuario,
                estrela=int(nota),
                mensagem=comentario.strip()
            )
            return JsonResponse({'success': True}, status=200)
            
        except Exception as e:
            print(f"Erro ao salvar avaliação via ORM: {e}")
            return JsonResponse({'error': 'Erro interno ao salvar no banco de dados.'}, status=500)

    # 2. SELEÇÃO DO TEMPLATE COM BASE NO ID_PONTO
    # NOTA: Esta é uma dívida técnica. O ideal futuro é ter um campo 'slug' ou 'template_nome' no Model.
    mapeamento_templates = {
        1: 'hoteis/tela-hotel-ibis.html',
        2: 'hoteis/tela-hotel-ipe.html',
        3: 'hoteis/tela-hotel-soft.html',
        4: 'lugares_turisticos/lugares-pop/tela-estacao-docas.html',
        5: 'lugares_turisticos/lugares-pop/tela-ilha-de-cotijuba.html',
        6: 'lugares_turisticos/lugares-pop/tela-ilha-combu.html',
        7: 'restaurantes/tela-onze-janelas.html',
        8: 'restaurantes/tela-estilo-bistro.html',
        9: 'restaurantes/tela-familia.html', 
        10: 'lugares_turisticos/lugares-inv/tela-palacete-bolonha.html',
        11: 'lugares_turisticos/lugares-inv/tela-caratateua.html',
        12: 'lugares_turisticos/lugares-inv/tela-trambioca.html',
        13: 'hoteis/tela-hotel-amazon.html',
        14: 'hoteis/tela-hotel-radisson.html',
        15: 'hoteis/tela-hotel-Atrium.html',
        16: 'hoteis/tela-hotel-transamerica.html',
        17: 'hoteis/tela-hotel-mercure.html',
    }

    template_escolhido = mapeamento_templates.get(id_ponto, 'usuario/detalhes-local.html')

    # 3. LÓGICA DE FAVORITO DINÂMICA VIA ORM
    favoritado = False
    if request.user.is_authenticated:
        favoritado = Favorito.objects.filter(id_usuario=request.user, id_ponto_turistico=local).exists()

    context = {
        'local': local,
        'favoritado': favoritado
    }
    return render(request, template_escolhido, context)


# ==========================================
# VIEWS ADMINISTRATIVAS (CRUD)
# ==========================================

@login_required
def salvar_local(request, id_ponto=None):
    if not request.user.is_staff:
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

        dados_ponto = {
            'nome_ponto_turistico': nome,
            'telefone': telefone,
            'descricao': descricao,
            'rua': rua,
            'bairro': bairro,
            'cidade': cidade,
            'imagem_url': imagem_url,
            'latitude': latitude,
            'longitude': longitude,
            'horario_funcionamento': horario,
            'categoria': categoria_obj
        }

        if ponto:
            for key, value in dados_ponto.items():
                setattr(ponto, key, value)
            ponto.save()
            messages.success(request, f'"{nome}" atualizado com sucesso!')
        else:
            PontoTuristico.objects.create(**dados_ponto)
            messages.success(request, f'"{nome}" cadastrado com sucesso!')

    return redirect('usuario:painel_admin')


@login_required
@require_POST
def excluir_local(request, id_ponto):
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado.')
        return redirect('usuario:login')

    ponto = get_object_or_404(PontoTuristico, id_ponto_turistico=id_ponto)
    nome = ponto.nome_ponto_turistico
    ponto.delete()
    messages.success(request, f'"{nome}" foi excluído com sucesso.')

    return redirect('usuario:painel_admin')


@login_required
@require_POST
def excluir_avaliacao(request, id_ponto, id_usuario):
    """Exclui uma avaliação específica usando ORM (Substitui SQL Bruto)"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado.')
        return redirect('usuario:login')

    # O ORM lida com a segurança e a query de forma otimizada
    Avaliacao.objects.filter(id_ponto_turistico_id=id_ponto, id_usuario_id=id_usuario).delete()
    messages.success(request, 'Avaliação excluída com sucesso.')
    
    return redirect('usuario:painel_admin')