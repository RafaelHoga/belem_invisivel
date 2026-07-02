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

    # Lugares Turísticos Populares
    path('estacao-docas/', TemplateView.as_view(template_name='lugares_turisticos/lugares-pop/tela-estacao-docas.html'), name='tela_estacao_docas'),
    path('ilha-cotijuba/', TemplateView.as_view(template_name='lugares_turisticos/lugares-pop/tela-ilha-de-cotijuba.html'), name='tela_ilha_cotijuba'),
    path('ilha-combu/', TemplateView.as_view(template_name='lugares_turisticos/lugares-pop/tela-ilha-combu.html'), name='tela_ilha_combu'),

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

    # Restaurantes individuais
    path('casa-saulo/', TemplateView.as_view(template_name='restaurantes/tela-onze-janelas.html'), name='tela_onze_janelas'),
    path('estilo-bistro/', TemplateView.as_view(template_name='restaurantes/tela-estilo-bistro.html'), name='tela_estilo_bistro'),
    path('familia-sicilia/', TemplateView.as_view(template_name='restaurantes/tela-familia.html'), name='tela_familia_sicilia'),
]