from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ponto_turistico.models import Avaliacao

@login_required(login_url='login')
def perfil_view(request):
    # Busca todas as avaliações que pertencem unicamente ao usuário logado
    minhas_avaliacoes = Avaliacao.objects.filter(usuario=request.user)
    
    context = {
        'avaliacoes': minhas_avaliacoes
    }
    # O Django já injeta o 'request.user' automaticamente no template
    return render(request, 'tela_perfil_usuario.html')
