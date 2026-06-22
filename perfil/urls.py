from django.urls import path
from usuario.views import perfil_view  # Importa a view protegida que você criou

app_name = 'perfil'

urlpatterns = [
    # Quando o usuário acessar /perfil/, ele cai direto aqui
    path('', perfil_view, name='perfil'), 
]