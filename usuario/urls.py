from django.urls import path
from config import views as config_views 
from . import views

# Definimos o app_name para criar o namespace 'usuario'
app_name = 'usuario'

urlpatterns = [
    path('', views.home, name='index'), 
    path('login/', config_views.autentificacao_view, name='login'),
    path('logout/', config_views.logout_view, name='logout'),
    # Removido a linha do include('perfil.urls') que estava duplicada aqui!
]