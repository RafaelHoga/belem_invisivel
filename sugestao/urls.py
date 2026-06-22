# sugestao/urls.py
from django.urls import path
from django.views.generic import TemplateView

# O app_name define o NAMESPACE que o erro apontou!
app_name = 'sugestao'

urlpatterns = [
    # Mapeia a URL /sugestao/sugerir/ para renderizar o seu template
    path('sugerir/', TemplateView.as_view(template_name='sugestao_ponto.html'), name='sugestao_ponto'),
]