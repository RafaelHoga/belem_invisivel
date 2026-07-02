from django.contrib import admin
from .models import Sugestao

@admin.register(Sugestao)
class SugestaoAdmin(admin.ModelAdmin):
    list_display = (
        'nome_sugestao',
        'categoria',
        'usuario',
        'status',
    )

    list_filter = (
        'status',
        'categoria',
    )

    search_fields = (
        'nome_sugestao',
        'endereco',
    )

    list_editable = (
        'status',
    )