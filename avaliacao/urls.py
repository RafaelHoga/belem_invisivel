from django.urls import path
from . import views

app_name = 'avaliacao'

urlpatterns = [
    path('ponto/<int:ponto_id>/avaliar/', views.criar_avaliacao_view, name='criar'),
]