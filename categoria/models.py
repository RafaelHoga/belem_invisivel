from django.db import models


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nome_categoria = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    icone = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="Nome do ícone (ex: 'church', 'museum', 'park')"
    )
    
    # Campos de auditoria
    criado_em = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome_categoria']
    
    def __str__(self):
        return self.nome_categoria