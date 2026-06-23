from django.urls import path
from . import views

app_name = 'categoria'

urlpatterns = [
    path('', views.lista_categorias, name='lista'),
    path('<int:categoria_id>/pontos/', views.pontos_por_categoria, name='pontos'),
]