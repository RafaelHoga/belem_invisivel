from django.urls import path
from . import views

urlpatterns = [
    # 1. Rotas de entrada principais do menu
    path('', views.tela_turismo, name='tela-turismo'),
    path('lista-hoteis/', views.tela_hoteis, name='tela-hoteis'),
    path('lista-restaurantes/', views.tela_restaurante, name='tela-restaurante'),

    # 2. Rotas Administrativas (CRUD unificado)
    path('novo/', views.salvar_local, name='cadastrar_ponto'),
    path('editar/<int:id_ponto>/', views.salvar_local, name='editar_ponto'),
    path('excluir/<int:id_ponto>/', views.excluir_local, name='excluir_ponto'),
    path('avaliacao/excluir/<int:id_ponto>/<int:id_usuario>/', views.excluir_avaliacao, name='excluir_avaliacao'),

    # 3. Rota Unificada de Favoritos (AJAX)
    path('favorito/<int:id_ponto>/', views.toggle_favorito, name='toggle_favorito'),

    # 4. Rotas Específicas de Detalhes (Mapeadas por ID para templates customizados)
    path('hotel-ibis/', views.detalhe_local, {'id_ponto': 1}, name='tela_hotel_ibis'),
    path('hotel-ipe/', views.detalhe_local, {'id_ponto': 2}, name='tela_hotel_ipe'),
    path('hotel-soft/', views.detalhe_local, {'id_ponto': 3}, name='tela_hotel_soft'),
    
    path('estacao-docas/', views.detalhe_local, {'id_ponto': 4}, name='tela_estacao_docas'),
    path('ilha-cotijuba/', views.detalhe_local, {'id_ponto': 5}, name='tela_ilha_cotijuba'),
    path('ilha-combu/', views.detalhe_local, {'id_ponto': 6}, name='tela_ilha_combu'),
    
    path('restaurante-onze-janelas/', views.detalhe_local, {'id_ponto': 7}, name='tela_onze_janelas'),
    path('restaurante-estilo-bistro/', views.detalhe_local, {'id_ponto': 8}, name='tela_estilo_bistro'),
    path('restaurante-familia-sicilia/', views.detalhe_local, {'id_ponto': 9}, name='tela_familia_sicilia'),
    
    path('palacete-bolonha/', views.detalhe_local, {'id_ponto': 10}, name='palacete_bolonha'),
    path('caratateua/', views.detalhe_local, {'id_ponto': 11}, name='caratateua'),
    path('trambioca/', views.detalhe_local, {'id_ponto': 12}, name='trambioca'),
    
    path('amazon-park/', views.detalhe_local, {'id_ponto': 13}, name='tela_hotel_amazon'),
    path('radisson/', views.detalhe_local, {'id_ponto': 14}, name='tela_hotel_radisson'),
    path('atrium/', views.detalhe_local, {'id_ponto': 15}, name='tela_hotel_atrium'),
    path('transamerica/', views.detalhe_local, {'id_ponto': 16}, name='tela_hotel_transamerica'),
    path('mercure/', views.detalhe_local, {'id_ponto': 17}, name='tela_hotel_mercure'),
    
    # 5. ROTA DINÂMICA GENÉRICA (Sempre no final para não interceptar as rotas nomeadas acima)
    path('<int:id_ponto>/', views.detalhe_local, name='detalhe_local'),
]