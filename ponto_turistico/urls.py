from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Rotas de entrada principais do menu
    path('', views.tela_turismo, name='tela-turismo'),
    path('lista-hoteis/', views.tela_hoteis, name='tela-hoteis'),
    path('lista-restaurantes/', views.tela_restaurante, name='tela-restaurante'),

    # ROTA DINÂMICA UNIFICADA: Exibe os detalhes de qualquer local puxando do banco de dados
    path('<int:id_ponto>/', views.detalhe_local, name='detalhe_local'),

    # Rotas Administrativas (CRUD unificado)
    path('novo/', views.salvar_local, name='cadastrar_ponto'),
    path('editar/<int:id_ponto>/', views.salvar_local, name='editar_ponto'),
    path('excluir/<int:id_ponto>/', views.excluir_local, name='excluir_ponto'),
    # Coloque junto com as outras rotas administrativas:
    path('avaliacao/excluir/<int:id_ponto>/<int:id_usuario>/', views.excluir_avaliacao, name='excluir_avaliacao'),

    # =========================================================================
    # ROTAS ESTÁTICAS ANTIGAS (Mantidas para compatibilidade temporária)
    # =========================================================================
    # Hotéis
    path('hotel-ibis/', TemplateView.as_view(template_name='hoteis/tela-hotel-ibis.html'), name='tela_hotel_ibis'),
    path('hotel-ipe/', TemplateView.as_view(template_name='hoteis/tela-hotel-ipe.html'), name='tela_hotel_ipe'),
    path('hotel-soft/', TemplateView.as_view(template_name='hoteis/tela-hotel-soft.html'), name='tela_hotel_soft'),
    path('amazon-park/', TemplateView.as_view(template_name='hoteis/tela-hotel-amazon.html'), name='tela_hotel_amazon'),
    path('radisson/', TemplateView.as_view(template_name='hoteis/tela-hotel-radisson.html'), name='tela_hotel_radisson'),
    path('atrium/', TemplateView.as_view(template_name='hoteis/tela-hotel-atrium.html'), name='tela_hotel_atrium'),
    path('transamerica/', TemplateView.as_view(template_name='hoteis/tela-hotel-transamerica.html'), name='tela_hotel_transamerica'),
    path('mercure/', TemplateView.as_view(template_name='hoteis/tela-hotel-mercure.html'), name='tela_hotel_mercure'),


    #Pontos Turísticos Populares
    path('estacao-docas/', views.detalhe_local, {'id_ponto': 1}, name='tela_estacao_docas'),
    path('ilha-cotijuba/', views.detalhe_local, {'id_ponto': 2}, name='tela_ilha_cotijuba'),
    path('ilha-combu/', views.detalhe_local, {'id_ponto': 3}, name='tela_ilha_combu'),
    #Pontos Turísticos Menos Conhecidos
    path('palacete-bolonha/', views.detalhe_local, {'id_ponto': 4}, name='tela_palacete_bolonha'),
    path('caratateua/', views.detalhe_local, {'id_ponto': 5}, name='tela_caratateua'),
    path('trambioca/', views.detalhe_local, {'id_ponto': 6}, name='tela_trambioca'),

    # Restaurantes Populares
    path('onze-janelas/', views.detalhe_local, {'id_ponto': 7}, name='tela_onze_janelas'),
    path('estilo-bistro/', views.detalhe_local, {'id_ponto': 8}, name='estilo_bistro'),
    path('familia-sicilia/', views.detalhe_local, {'id_ponto': 9}, name='familia_sicilia'),
    
    
    

    # ROTA DINÂMICA UNIFICADA (Mantenha ela como está para links que usem ID numérico direto)
    
    path('<int:id_ponto>/', views.detalhe_local, name='detalhe_local'),
    

    path('ilha-combu/', TemplateView.as_view(
        template_name='lugares_turisticos/lugares-pop/tela-ilha-combu.html'
    ), name='tela_ilha_combu'),

    path('utinga/', TemplateView.as_view(
        template_name='lugares_turisticos/lugares-inv/tela-utinga.html'
    ), name='tela_utinga'),

    path('museu-presepio/', TemplateView.as_view(
        template_name='lugares_turisticos/lugares-inv/tela-museu-presepio.html'
    ), name='tela_museu_presepio'),

    path('arte-sacra/', TemplateView.as_view(
        template_name='lugares_turisticos/lugares-inv/tela-arte-sacra.html' 
    ), name='tela_arte_sacra'),

    path('remanso-peixe/', TemplateView.as_view(
        template_name='restaurantes/restaurantes-inv/tela-remanso-peixe.html'
    ), name='tela_remanso_peixe'),

    path('tomaz-culinaria/', TemplateView.as_view(
        template_name='restaurantes/restaurantes-inv/tela-tomaz-culinaria.html'
    ), name='tela_tomaz_culinaria'),

    path('recanto-paraibano/', TemplateView.as_view(
        template_name='restaurantes/restaurantes-inv/tela-recanto-paraibano.html'
    ), name='tela_recanto_paraibano'),

    path('casa-saulo/', TemplateView.as_view(
        template_name='restaurantes/restaurantes-pop/tela-onze-janelas.html'
    ), name='tela_onze_janelas'),

    path('estilo-bistro/', TemplateView.as_view(
        template_name='restaurantes/restaurantes-pop/tela-estilo-bistro.html'
    ), name='tela_estilo_bistro'),

    path('familia-sicilia/', TemplateView.as_view(
        template_name='restaurantes/restaurantes-pop/tela-familia.html'
    ), name='tela_familia_sicilia'),

    path('amazon-park/', TemplateView.as_view(
        template_name='hoteis/tela-hotel-amazon.html'
    ), name='tela_hotel_amazon'),

    path('radisson/', TemplateView.as_view(
        template_name='hoteis/tela-hotel-radisson.html'
    ), name='tela_hotel_radisson'),

    path('atrium/', TemplateView.as_view(
        template_name='hoteis/tela-hotel-atrium.html'
    ), name='tela_hotel_atrium'),

    path('transamerica/', TemplateView.as_view(
        template_name='hoteis/tela-hotel-transamerica.html'
    ), name='tela_hotel_transamerica'),

    path('mercure/', TemplateView.as_view(
        template_name='hoteis/tela-hotel-mercure.html'
    ), name='tela_hotel_mercure'),
    
    path('palacete-bolonha/', TemplateView.as_view(
        template_name='lugares_turisticos/lugares-inv/tela-palacete-bolonha.html'
    ), name='palacete_bolonha'),
    
    path('caratateua/', TemplateView.as_view(
        template_name='lugares_turisticos/lugares-inv/tela-caratateua.html'
    ), name='caratateua'),
    
    path('trambioca/', TemplateView.as_view(
        template_name='lugares_turisticos/lugares-inv/tela-trambioca.html'
    ), name='trambioca'),
    # Lugares Turísticos Invisíveis / Menos Conhecidos
    path('caratateua/', TemplateView.as_view(template_name='lugares_turisticos/lugares-inv/tela-caratateua.html'), name='caratateua'),
    path('trambioca/', TemplateView.as_view(template_name='lugares_turisticos/lugares-inv/tela-trambioca.html'), name='trambioca'),

    # Restaurantes individuais

    path('estilo-bistro/', TemplateView.as_view(template_name='restaurantes/tela-estilo-bistro.html'), name='tela_estilo_bistro'),
    path('familia-sicilia/', TemplateView.as_view(template_name='restaurantes/tela-familia.html'), name='tela_familia_sicilia'),
]