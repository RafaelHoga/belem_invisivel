"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Telas institucionais/estáticas (temporárias ou permanentes)
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('contato/', TemplateView.as_view(template_name='contato.html'), name='contato'),
    path('novo-comentario/', TemplateView.as_view(template_name='novo_comentario.html'), name='novo-comentario'),
    
    # Rotas principais mapeadas para os seus Apps de Negócio
    path('turismo/', include('ponto_turistico.urls')), 
    path('usuario/', include('usuario.urls')),
    path('sugestao/', include('sugestao.urls')),
]

# Permite ao Django servir arquivos de mídia (Uploads) durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ==============================================================================
# CUSTOMIZAÇÃO DO PAINEL ADMINISTRATIVO (BELÉM INVISÍVEL)
# ==============================================================================
admin.site.site_header = "Painel Administrativo - Belém Invisível"
admin.site.site_title = "Belém Invisível Admin"
admin.site.index_title = "Gerenciamento do Sistema"