from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'index.html')

# Força o redirecionamento para o login correto caso o usuário não esteja logado
@login_required(login_url='usuario:login') 
def perfil_view(request):
    return render(request, 'tela_perfil_usuario.html')