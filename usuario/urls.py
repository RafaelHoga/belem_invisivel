from django.urls import path
from .views import home
from config import views as config_views   
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', home, name='home'),
    #Ambas as rotas abaixo podem apontar para a sua view unificada
    path('login/', config_views.autentificacao_view, name='login'),
    path('logout/', config_views.logout_view, name='logout'),
]
