from django.urls import path
from . import views

# CORREÇÃO: Mantido para não quebrar o contato.html e outros templates
app_name = 'sugestao'

urlpatterns = [
    path('sugerir/', views.enviar_sugestao, name='sugestao_ponto'),
]