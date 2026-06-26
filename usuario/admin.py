from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    # Exibe dados chave na tabela de usuários
    list_display = ('nome_usuario', 'email', 'id_perfil', 'data_nascimento')
    
    # Filtra rapidamente quem é Admin (1) ou Usuário Comum (2)
    list_filter = ('id_perfil',)
    
    search_fields = ('nome_usuario', 'email')
    
    # Evita que a senha criptografada seja exibida em texto aberto ou editada de forma incorreta por aqui
    fields = ('nome_usuario', 'email', 'data_nascimento', 'id_perfil', 'foto_perfil')

    # Injeta o CSS customizado com segurança de forma nativa
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }