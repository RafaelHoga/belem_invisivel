from django.contrib import admin
from .models import Categoria, PontoTuristico, Favorito, Avaliacao

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id_categoria', 'descricao_categoria')
    search_fields = ('descricao_categoria',)


# Permite visualizar e deletar avaliações diretamente de dentro da página do Ponto Turístico
class AvaliacaoInline(admin.TabularInline):
    model = Avaliacao
    extra = 0
    fields = ('id_usuario', 'estrela', 'mensagem', 'data_avaliacao')
    readonly_fields = ('data_avaliacao',)


@admin.register(PontoTuristico)
class PontoTuristicoAdmin(admin.ModelAdmin):
    # O que vai aparecer na listagem principal
    list_display = ('nome_ponto_turistico', 'categoria', 'bairro', 'cidade', 'telefone')
    
    # Filtros laterais inteligentes para o projeto Belém Invisível
    list_filter = ('categoria', 'bairro')
    
    # Barra de pesquisa por nome, bairro ou descrição do local
    search_fields = ('nome_ponto_turistico', 'bairro', 'descricao')
    
    # Organização visual dos campos ao abrir um ponto turístico
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome_ponto_turistico', 'categoria', 'descricao', 'imagem_url')
        }),
        ('Localização', {
            'fields': ('rua', 'bairro', 'cidade', 'latitude', 'longitude')
        }),
        ('Contato e Atendimento', {
            'fields': ('telefone', 'horario_funcionamento')
        }),
    )
    
    inlines = [AvaliacaoInline]

    # Injeta o CSS customizado com segurança de forma nativa
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('id_ponto_turistico', 'id_usuario', 'data_favorito')
    list_filter = ('data_favorito',)


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('id_ponto_turistico', 'id_usuario', 'estrela', 'data_avaliacao')
    list_filter = ('estrela', 'data_avaliacao')
    search_fields = ('mensagem',)