from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='login')
def perfil_view(request):
    # O Django já injeta o 'request.user' automaticamente no template
    return render(request, 'perfil.html')
