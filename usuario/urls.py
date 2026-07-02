# from django.urls import path
# from .views import home
# from config import views as config_views   
# from . import views
# from django.views.generic import TemplateView

# urlpatterns = [
#     path('', home, name='index'),
#     #Ambas as rotas abaixo podem apontar para a sua view unificada
#     path('login/', config_views.autentificacao_view, name='login'),
#     path('logout/', config_views.logout_view, name='logout'),
# ]
from django.urls import path
from . import views

app_name = 'usuario'

urlpatterns = [
    path('', views.home, name='index'), 
    path('login/', views.login_usuario, name='login'),
    path('cadastro/', views.cadastro_usuario, name='cadastro'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('ponto/<int:id_ponto>/avaliar/', views.salvar_avaliacao, name='salvar_avaliacao'),
    # NOVA ROTA: Adicionada para o funcionamento do botão "Sair"
    path('painel/', views.painel_admin, name='painel_admin'),
    path('painel/categoria/nova/', views.cadastrar_categoria, name='cadastrar_categoria'),
    path('painel/categoria/excluir/<int:id_categoria>/', views.excluir_categoria, name='excluir_categoria'),
    path('perfil/atualizar-foto/', views.atualizar_foto, name='atualizar_foto'),
    path('logout/', views.logout_usuario, name='logout'),
    
    # ROTA CORRIGIDA: Permite salvar/remover favoritos via AJAX na interface
    path('favorito/alternar/<int:ponto_id>/', views.alternar_favorito, name='alternar_favorito'),
]