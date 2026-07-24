"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

# CORREÇÃO: Importar as views do app ponto_turistico para usar na home
from ponto_turistico import views as ponto_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # CORREÇÃO CRÍTICA: Usar a view dinâmica 'index' em vez de TemplateView.
    # Isso permite que o index.html receba o contexto (hoteis_destaque, etc.)
    path('', ponto_views.index, name='index'),
    
    path('contato/', TemplateView.as_view(template_name='contato.html'), name='contato'),
    
    # Nota: 'novo-comentario' geralmente é processado por uma view POST, 
    # mas mantive conforme seu original. O ideal é que esteja nas urls do app.
    path('novo-comentario/', TemplateView.as_view(template_name='novo_comentario.html'), name='novo-comentario'),
    
    # Rotas principais mapeadas para os seus Apps de Negócio
    path('turismo/', include('ponto_turistico.urls')), 
    path('usuario/', include('usuario.urls')),
    path('sugestao/', include('sugestao.urls')),
]

# Permite ao Django servir arquivos de mídia (Uploads) durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Adicionado STATIC_ROOT para garantir que CSS/JS carreguem em dev se necessário
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ==============================================================================
# CUSTOMIZAÇÃO DO PAINEL ADMINISTRATIVO (BELÉM INVISÍVEL)
# ==============================================================================
admin.site.site_header = "Painel Administrativo - Belém Invisível"
admin.site.site_title = "Belém Invisível Admin"
admin.site.index_title = "Gerenciamento do Sistema"