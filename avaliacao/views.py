from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ponto_turistico.models import PontoTuristico
from .forms import AvaliacaoForm
from .services import criar_avaliacao


@login_required
def criar_avaliacao_view(request, ponto_id):
    """
    View para processar o envio de uma nova avaliação.
    Chama o service 'criar_avaliacao' para lógica de negócio.
    """
    ponto = get_object_or_404(
        PontoTuristico.objects.filter(ativo=True),
        id_ponto_turistico=ponto_id
    )
    
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        form.user = request.user  # Injeta usuário para validação
        
        if form.is_valid():
            try:
                # Chama o service para criar a avaliação
                avaliacao = criar_avaliacao(
                    usuario=request.user,
                    ponto_turistico=ponto,
                    nota=form.cleaned_data['nota'],
                    comentario=form.cleaned_data.get('comentario', '')
                )
                
                messages.success(request, 'Sua avaliação foi registrada com sucesso!')
                return redirect('ponto_turistico:detalhe', ponto_id=ponto.id_ponto_turistico)
                
            except ValueError as e:
                # Erro de validação de negócio vindo do service
                messages.error(request, str(e))
            except Exception as e:
                # Erro inesperado
                messages.error(request, 'Ocorreu um erro ao salvar sua avaliação. Tente novamente.')
    else:
        # GET: exibe formulário vazio
        form = AvaliacaoForm(initial={'ponto_turistico': ponto.id_ponto_turistico})
    
    context = {
        'form': form,
        'ponto': ponto,
    }
    
    return render(request, 'avaliacao/criar.html', context)