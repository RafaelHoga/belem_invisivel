from django.contrib import admin
from .models import Sugestao

@admin.register(Sugestao)
class SugestaoAdmin(admin.ModelAdmin):
    list_display = ('nome_sugestao', 'id_categoria', 'status', 'data_sugestao')
    list_filter = ('status', 'id_categoria')
    search_fields = ('nome_sugestao', 'endereco')
    # Permite alterar o status direto pela lista sem precisar abrir o registro
    list_editable = ('status',)