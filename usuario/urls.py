from django.urls import path
from . import views
from django.views.generic import TemplateView

# Definimos o app_name para criar o namespace 'usuario'
app_name = 'usuario'

urlpatterns = [
    # Rota para a página inicial
    path('', views.home, name='index'), 
    
    # Rota para a view de login dentro do app usuario
    path('login/', views.login_usuario, name='login'),
    
    # Rota de cadastro esperada pelo HTML
    path('cadastro/', views.cadastro_usuario, name='cadastro'),
    
    # CORREÇÃO: Mantendo o name como 'perfil' para bater com o padrão curto
    path('perfil/', views.perfil_usuario, name='perfil'),
    # path('perfil/', TemplateView.as_view(template_name='usuario/tela_perfil_usuario.html'), name='perfil'),
    
    # NOVA ROTA: Adicionada para o funcionamento do botão "Sair"
    path('logout/', views.logout_usuario, name='logout'),
]