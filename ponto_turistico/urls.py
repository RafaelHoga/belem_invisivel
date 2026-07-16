from django.urls import path
from . import views

urlpatterns = [
    # 1. Rotas de listagem (Menus)
    path('', views.tela_turismo, name='tela-turismo'),
    path('lista-hoteis/', views.tela_hoteis, name='tela-hoteis'),
    path('lista-restaurantes/', views.tela_restaurante, name='tela-restaurante'),

    # 2. Rota de Favoritos (AJAX)
    path('favorito/<int:id_ponto>/', views.toggle_favorito, name='toggle_favorito'),
    
    # 3. ROTA DINÂMICA GENÉRICA (Única rota de detalhes necessária)
    # Ex: /turismo/1/, /turismo/15/, etc.
    path('<int:id_ponto>/', views.detalhe_local, name='detalhe_local'),
]