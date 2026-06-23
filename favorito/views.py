from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from ponto_turistico.models import PontoTuristico
from .services import alternar_favorito


@login_required
@require_POST
def toggle_favorito_view(request, ponto_id):
    """
    View para alternar o status de favorito de um ponto turístico.
    Chama o service 'alternar_favorito' para lógica de negócio.
    Suporta tanto requisições normais quanto AJAX.
    """
    # Verifica se o ponto existe e está ativo
    ponto = get_object_or_404(
        PontoTuristico.objects.filter(ativo=True),
        id_ponto_turistico=ponto_id
    )
    
    try:
        # Chama o service para alternar o favorito
        favorito, criado = alternar_favorito(
            usuario=request.user,
            ponto_id=ponto_id
        )
        
        # Define mensagem baseada na ação
        if criado:
            mensagem = f'"{ponto.nome_ponto_turistico}" adicionado aos seus favoritos!'
        else:
            mensagem = f'"{ponto.nome_ponto_turistico}" removido dos seus favoritos.'
        
        # Resposta para requisições AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'favoritou': criado,
                'mensagem': mensagem,
                'ponto_id': ponto_id
            })
        
        # Resposta para requisições normais (formulário)
        messages.success(request, mensagem)
        return redirect('ponto_turistico:detalhe', ponto_id=ponto_id)
        
    except PontoTuristico.DoesNotExist:
        erro_msg = 'Ponto turístico não encontrado.'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': erro_msg}, status=404)
        
        messages.error(request, erro_msg)
        return redirect('ponto_turistico:lista')
        
    except Exception as e:
        erro_msg = 'Ocorreu um erro ao processar seu favorito. Tente novamente.'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': erro_msg}, status=500)
        
        messages.error(request, erro_msg)
        return redirect('ponto_turistico:detalhe', ponto_id=ponto_id)