from django.urls import path
from . import views

app_name = 'usuario'

urlpatterns = [
    path('', views.home, name='index'),
    path('login/', views.autentificacao_view, name='login'),  # Mesma view trata login E cadastro
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
]