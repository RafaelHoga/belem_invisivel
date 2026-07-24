from django.urls import path
from . import views

# CORREÇÃO: Mantido para não quebrar o contato.html e outros templates
app_name = 'sugestao'

urlpatterns = [
    path('sugerir/', views.enviar_sugestao, name='sugestao_ponto'),
    path('sugestao-ponto/', views.sugestao_ponto_page, name='sugestao_ponto_page'),
]