from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils.html import format_html
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    # Exibe dados chave na tabela de usuários
    list_display = ('nome_usuario', 'email', 'perfil', 'data_nascimento', 'is_active', 'date_joined')
    
    # Filtros rápidos
    list_filter = ('perfil', 'is_active', 'is_staff', 'data_nascimento')
    
    search_fields = ('nome_usuario', 'email')
    
    # Ordenação padrão por nome
    ordering = ('nome_usuario',)
    
    # Paginação para melhor performance
    list_per_page = 50
    
    # Campos que podem ser editados
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome_usuario', 'data_nascimento', 'foto_perfil', 'perfil')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Campos readonly
    readonly_fields = ('last_login', 'date_joined')
    
    # Campos para criação de usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome_usuario', 'password1', 'password2', 'perfil', 'data_nascimento'),
        }),
    )

    # Injeta o CSS customizado com segurança de forma nativa
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }