from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import PontoTuristico, Favorito

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