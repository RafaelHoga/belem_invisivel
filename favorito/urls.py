from django.urls import path
from . import views

app_name = 'favorito'

urlpatterns = [
    path('ponto/<int:ponto_id>/toggle/', views.toggle_favorito_view, name='toggle'),
]