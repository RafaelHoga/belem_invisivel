from django.urls import path
from .views import home
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
