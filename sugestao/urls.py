from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'sugestao'

urlpatterns = [
    path(
        'sugerir/',
        TemplateView.as_view(template_name='sugestao_ponto.html'),
        name='sugestao_ponto'
    ),
    path(
        'salvar/',
        views.salvar_sugestao,
        name='salvar_sugestao'
    ),
]
