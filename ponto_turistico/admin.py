from django.contrib import admin
from .models import Categoria, PontoTuristico, Favorito, Avaliacao


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id_categoria", "descricao_categoria")
    search_fields = ("descricao_categoria",)


class AvaliacaoInline(admin.TabularInline):
    model = Avaliacao
    extra = 0
    fields = ("usuario", "estrela", "mensagem", "data_avaliacao")
    readonly_fields = ("data_avaliacao",)


@admin.register(PontoTuristico)
class PontoTuristicoAdmin(admin.ModelAdmin):
    list_display = (
        "nome_ponto_turistico",
        "categoria",
        "bairro",
        "cidade",
        "telefone",
    )

    list_filter = ("categoria", "bairro")

    search_fields = (
        "nome_ponto_turistico",
        "bairro",
        "descricao",
    )

    fieldsets = (
        ("Informações Básicas", {
            "fields": (
                "nome_ponto_turistico",
                "categoria",
                "descricao",
                "imagem_url",
            )
        }),
        ("Localização", {
            "fields": (
                "rua",
                "bairro",
                "cidade",
                "latitude",
                "longitude",
            )
        }),
        ("Contato", {
            "fields": (
                "telefone",
                "horario_funcionamento",
            )
        }),
    )

    inlines = [AvaliacaoInline]


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ("ponto_turistico", "usuario", "data_favorito")
    list_filter = ("data_favorito",)


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = (
        "ponto_turistico",
        "usuario",
        "estrela",
        "data_avaliacao",
    )

    list_filter = (
        "estrela",
        "data_avaliacao",
    )

    search_fields = ("mensagem",)