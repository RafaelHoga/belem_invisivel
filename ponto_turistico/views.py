from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import PontoTuristico
from avaliacao.services import criar_avaliacao
from avaliacao.forms import AvaliacaoForm
from favorito.services import alternar_favorito, usuario_favoritou


def lista_pontos_turisticos(request):
    """
    View para listar pontos turísticos.
    """
    pontos = PontoTuristico.objects.select_related('categoria').all()
    return render(request, 'ponto_turistico/lista.html', {'pontos': pontos})


def detalhe_ponto_turistico(request, ponto_id):
    """
    View para exibir detalhes de um ponto turístico.
    Mostra se o usuário atual favoritou o ponto.
    """
    ponto = get_object_or_404(
        PontoTuristico.objects.select_related('categoria'),
        id=ponto_id
    )
    
    # Verifica se o usuário favoritou (apenas se autenticado)
    favoritou = False
    if request.user.is_authenticated:
        favoritou = usuario_favoritou(request.user, ponto_id)
    
    context = {
        'ponto': ponto,
        'favoritou': favoritou,
    }
    
    return render(request, 'ponto_turistico/detalhe.html', context)


@login_required
def avaliar_ponto_turistico(request, ponto_id):
    """
    View para avaliar um ponto turístico.
    Consome o service de avaliação de forma limpa.
    """
    ponto = get_object_or_404(PontoTuristico, id=ponto_id)
    
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        form.user = request.user  # Injeta o usuário para validação
        
        if form.is_valid():
            try:
                # Usa o service para criar a avaliação
                avaliacao = criar_avaliacao(
                    usuario=request.user,
                    ponto_turistico=ponto,
                    nota=form.cleaned_data['nota'],
                    comentario=form.cleaned_data.get('comentario', '')
                )
                
                messages.success(request, 'Avaliação registrada com sucesso!')
                return redirect('ponto_turistico:detalhe', ponto_id=ponto.id)
                
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = AvaliacaoForm(initial={'ponto_turistico': ponto.id})
    
    return render(request, 'avaliacao/form.html', {
        'form': form,
        'ponto': ponto
    })


@login_required
def toggle_favorito(request, ponto_id):
    """
    View para adicionar/remover ponto dos favoritos.
    Consome o service de favorito de forma limpa.
    Suporta tanto requisições POST quanto AJAX.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    try:
        # Usa o service para alternar o favorito
        favorito, criado = alternar_favorito(request.user, ponto_id)
        
        mensagem = 'Ponto adicionado aos favoritos!' if criado else 'Ponto removido dos favoritos!'
        
        # Resposta para AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'favoritou': criado,
                'mensagem': mensagem
            })
        
        # Resposta para formulário normal
        messages.success(request, mensagem)
        return redirect('ponto_turistico:detalhe', ponto_id=ponto_id)
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': str(e)}, status=400)
        
        messages.error(request, f'Erro ao processar favorito: {str(e)}')
        return redirect('ponto_turistico:detalhe', ponto_id=ponto_id)