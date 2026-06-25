
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PontoTuristico, Avaliacao

def estacao_docas_view(request):
    # Obtém o objeto da Estação das Docas do banco de dados de forma segura
    ponto = get_object_or_404(PontoTuristico, nome_ponto_turistico__icontains='Estação das Docas')
    
    if request.method == 'POST':
        # Bloqueia o envio se o usuário não estiver logado
        if not request.user.is_authenticated:
            return redirect('login')
            
        nota = request.POST.get('nota')  # Captura o valor do input de estrelas
        comentario = request.POST.get('comentario')  # Captura o texto digitado
        
        if nota and comentario:
            # Salva diretamente no MySQL utilizando o modelo mapeado
            Avaliacao.objects.create(
                usuario=request.user,
                ponto_turistico=ponto,
                nota=int(nota),
                comentario=comentario
            )
            # Redireciona para recarregar a página e limpar os campos do formulário
            return redirect(request.path)

    # Recupera todas as avaliações feitas exclusivamente para este ponto turístico
    avaliacoes = ponto.avaliacoes.all()

    context = {
        'ponto': ponto,
        'avaliacoes': avaliacoes
    }
    return render(request, 'lugares_turisticos/lugares-pop/tela-estacao-docas.html', context)