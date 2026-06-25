from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ponto_turistico.models import Avaliacao

@login_required(login_url='login')
def perfil_view(request):
    # Busca as avaliações do usuário logado trazendo os dados do ponto turístico associado
    minhas_avaliacoes = Avaliacao.objects.filter(usuario=request.user).select_related('ponto_turistico')
    
    context = {
        'avaliacoes': minhas_avaliacoes
    }
    # CORRIGIDO: Adicionado o dicionário 'context' como terceiro parâmetro!
    return render(request, 'tela_perfil_usuario.html', context)