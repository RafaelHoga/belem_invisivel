from django.contrib import admin
from .models import Usuario

# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    # Exibe dados chave na tabela de usuários (id_perfil removido)
    list_display = ('nome_usuario', 'email', 'data_nascimento')
    
    # Filtros rápidos (id_perfil removido temporariamente)
    list_filter = ('data_nascimento',)
    
    search_fields = ('nome_usuario', 'email')
    
    # Campos que podem ser editados (id_perfil removido)
    fields = ('nome_usuario', 'email', 'data_nascimento', 'foto_perfil')

    # Injeta o CSS customizado com segurança de forma nativa
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }