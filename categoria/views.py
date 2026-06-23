from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Categoria
from ponto_turistico.models import PontoTuristico


def lista_categorias(request):
    """
    View para listar todas as categorias ativas.
    Inclui contagem de pontos turísticos por categoria.
    """
    # Usa annotate para contar pontos turísticos por categoria
    categorias = Categoria.objects.filter(
        ativo=True
    ).annotate(
        total_pontos=Count('pontos_turisticos', filter=models.Q(pontos_turisticos__ativo=True))
    ).order_by('nome_categoria')
    
    context = {
        'categorias': categorias,
    }
    
    return render(request, 'categoria/lista.html', context)


def pontos_por_categoria(request, categoria_id):
    """
    View para listar pontos turísticos de uma categoria específica.
    """
    categoria = get_object_or_404(
        Categoria.objects.filter(ativo=True),
        id_categoria=categoria_id
    )
    
    # Busca pontos turísticos da categoria com otimização
    pontos = PontoTuristico.objects.filter(
        categoria=categoria,
        ativo=True
    ).select_related(
        'categoria'
    ).order_by('-media_avaliacoes', 'nome_ponto_turistico')
    
    context = {
        'categoria': categoria,
        'pontos': pontos,
    }
    
    return render(request, 'categoria/pontos_por_categoria.html', context)