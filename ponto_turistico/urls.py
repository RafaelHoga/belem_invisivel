from django.urls import path
from . import views

app_name = 'ponto_turistico'

urlpatterns = [
    # 1. Rotas de listagem (Menus)
    # CORREÇÃO: Alterado de 'tela-turismo' para 'tela_turismo' (underscore)
    path('', views.tela_turismo, name='tela_turismo'),
    path('lista-hoteis/', views.tela_hoteis, name='tela_hoteis'),
    path('lista-restaurantes/', views.tela_restaurante, name='tela_restaurante'),

    # 2. Rota de Favoritos (AJAX)
    path('favorito/<int:id_ponto>/', views.toggle_favorito, name='toggle_favorito'),
    
    # 3. ROTA DINÂMICA GENÉRICA (Única rota de detalhes necessária)
    path('<int:id_ponto>/', views.detalhe_local, name='detalhe_local'),
    
    # 4. NOVA ROTA: Cadastro de Ponto Turístico
    path('cadastrar/', views.cadastrar_ponto, name='cadastrar_ponto'),
    path('novo/', views.cadastrar_ponto, name='cadastrar_ponto_novo'),
    
    # 5. Edição de Ponto Turístico e Exclusão de Avaliação
    path('editar/<int:id_ponto>/', views.editar_ponto, name='editar_ponto'),
    path('avaliacao/excluir/<int:id_ponto>/<int:id_usuario>/', views.excluir_avaliacao, name='excluir_avaliacao'),
]