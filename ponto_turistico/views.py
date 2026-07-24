from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import PontoTuristico, Favorito, Categoria, Avaliacao
from django.contrib import messages

# ==========================================
# FUNÇÃO AUXILIAR
# ==========================================
def obter_favoritos_usuario(request):
    if request.user.is_authenticated:
        return list(Favorito.objects.filter(id_usuario=request.user).values_list('id_ponto_turistico_id', flat=True))
    return []


# ==========================================
# VIEWS PÚBLICAS
# ==========================================
def tela_turismo(request):
    locais = PontoTuristico.objects.filter(categoria__descricao_categoria="Turismo")
    context = {
        'locais': locais,
        'favoritos_ids': obter_favoritos_usuario(request)
    }
    return render(request, 'usuario/tela-turismo.html', context)


def tela_hoteis(request):
    locais = PontoTuristico.objects.filter(categoria__descricao_categoria="Hotel")
    context = {
        'locais': locais,
        'favoritos_ids': obter_favoritos_usuario(request)
    }
    return render(request, 'usuario/tela-hoteis.html', context)


def tela_restaurante(request):
    locais = PontoTuristico.objects.filter(categoria__descricao_categoria="Restaurante")
    context = {
        'locais': locais,
        'favoritos_ids': obter_favoritos_usuario(request)
    }
    return render(request, 'usuario/tela-restaurante.html', context)


def detalhe_local(request, id_ponto):
    """
    View genérica e unificada para exibir detalhes de QUALQUER ponto turístico.
    Elimina a necessidade de mapeamento de templates por ID.
    """
    local = get_object_or_404(PontoTuristico, id_ponto_turistico=id_ponto)
    
    # Verifica se o usuário logado já favoritou este local
    favoritado = False
    if request.user.is_authenticated:
        favoritado = Favorito.objects.filter(
            id_usuario=request.user, 
            id_ponto_turistico=local
        ).exists()

    context = {
        'local': local,
        'favoritado': favoritado
    }
    
    # Renderiza o único template genérico para todos os locais
    return render(request, 'ponto_turistico/detalhe_local.html', context)


# ==========================================
# VIEWS DE INTERAÇÃO (AJAX)
# ==========================================
@login_required
@require_POST
def toggle_favorito(request, id_ponto):
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
    
@login_required
@require_POST
def cadastrar_ponto(request):
    """
    Processa o formulário de cadastro de um novo local/ponto turístico.
    """
    try:
        nome = request.POST.get('nome_ponto_turistico', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        categoria_id = request.POST.get('id_categoria')
        descricao = request.POST.get('descricao', '').strip()
        rua = request.POST.get('rua', '').strip()
        bairro = request.POST.get('bairro', '').strip()
        cidade = request.POST.get('cidade', 'Belém').strip()
        horario = request.POST.get('horario_funcionamento', '').strip()
        imagem_url = request.POST.get('imagem_url', '').strip()
        
        latitude = request.POST.get('latitude')
        latitude = float(latitude) if latitude else None
        longitude = request.POST.get('longitude')
        longitude = float(longitude) if longitude else None
        
        if not nome:
            messages.error(request, 'O nome do local é obrigatório.')
            return redirect('usuario:painel_admin')
            
        if not categoria_id:
            messages.error(request, 'A categoria do local é obrigatória.')
            return redirect('usuario:painel_admin')

        PontoTuristico.objects.create(
            nome_ponto_turistico=nome,
            telefone=telefone,
            categoria_id=int(categoria_id),
            descricao=descricao,
            rua=rua,
            bairro=bairro,
            cidade=cidade,
            horario_funcionamento=horario,
            latitude=latitude,
            longitude=longitude,
            imagem_url=imagem_url
        )

        messages.success(request, f'O local "{nome}" foi cadastrado com sucesso!')
        
    except Exception as e:
        print(f"--- ERRO AO CADASTRAR PONTO: {e} ---")
        messages.error(request, f'Ocorreu um erro ao salvar o local: {e}')

    return redirect('usuario:painel_admin')


@login_required
@require_POST
def editar_ponto(request, id_ponto):
    """
    Processa a edição de um local/ponto turístico existente.
    """
    ponto = get_object_or_404(PontoTuristico, id_ponto_turistico=id_ponto)
    try:
        nome = request.POST.get('nome_ponto_turistico', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        categoria_id = request.POST.get('id_categoria')
        descricao = request.POST.get('descricao', '').strip()
        rua = request.POST.get('rua', '').strip()
        bairro = request.POST.get('bairro', '').strip()
        cidade = request.POST.get('cidade', 'Belém').strip()
        horario = request.POST.get('horario_funcionamento', '').strip()
        imagem_url = request.POST.get('imagem_url', '').strip()
        
        latitude = request.POST.get('latitude')
        latitude = float(latitude) if latitude else None
        longitude = request.POST.get('longitude')
        longitude = float(longitude) if longitude else None
        
        if not nome:
            messages.error(request, 'O nome do local é obrigatório.')
            return redirect('usuario:painel_admin')
            
        if not categoria_id:
            messages.error(request, 'A categoria do local é obrigatória.')
            return redirect('usuario:painel_admin')

        ponto.nome_ponto_turistico = nome
        ponto.telefone = telefone
        ponto.categoria_id = int(categoria_id)
        ponto.descricao = descricao
        ponto.rua = rua
        ponto.bairro = bairro
        ponto.cidade = cidade
        ponto.horario_funcionamento = horario
        ponto.latitude = latitude
        ponto.longitude = longitude
        ponto.imagem_url = imagem_url
        ponto.save()

        messages.success(request, f'O local "{nome}" foi editado com sucesso!')
        
    except Exception as e:
        print(f"--- ERRO AO EDITAR PONTO: {e} ---")
        messages.error(request, f'Ocorreu um erro ao editar o local: {e}')

    return redirect('usuario:painel_admin')


@login_required
def excluir_avaliacao(request, id_ponto, id_usuario):
    """
    Exclui uma avaliação (apenas staff)
    """
    if not request.user.is_staff:
        messages.error(request, "Permissão negada.")
        return redirect('usuario:painel_admin')
        
    try:
        avaliacao = get_object_or_404(Avaliacao, id_ponto_turistico_id=id_ponto, id_usuario_id=id_usuario)
        avaliacao.delete()
        messages.success(request, "Avaliação excluída com sucesso.")
    except Exception as e:
        messages.error(request, f"Erro ao excluir avaliação: {e}")
        
    return redirect('usuario:painel_admin')