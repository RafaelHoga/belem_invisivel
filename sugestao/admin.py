from django.contrib import admin
from .models import Sugestao


@admin.register(Sugestao)
class SugestaoAdmin(admin.ModelAdmin):
    list_display = ('nome_sugestao', 'id_categoria', 'id_usuario', 'status', 'data_sugestao')
    list_filter = ('status', 'id_categoria', 'data_sugestao')
    search_fields = ('nome_sugestao', 'endereco', 'id_usuario__nome_usuario')
    
    # Permite alterar o status direto pela lista sem precisar abrir o registro
    list_editable = ('status',)
    
    # Ordenação padrão por data (mais recentes primeiro)
    ordering = ('-data_sugestao',)
    
    # Paginação
    list_per_page = 50
    
    # Navegação por datas
    date_hierarchy = 'data_sugestao'
    
    # Melhora performance ao usar raw_id_fields para FKs
    raw_id_fields = ('id_usuario', 'id_categoria')