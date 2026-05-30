from django.urls import path
from .views import home
from django.views.generic import TemplateView

urlpatterns = [
    path('', home, name='home'),
    path('login/', TemplateView.as_view(
        template_name='login_usuario/tela-login.html'
    ), name='login'),
    
]
