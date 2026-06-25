from django.db import models
from usuario.models import Usuario      # Importa a model do app usuario
from categoria.models import Categoria  # Importa a model do app categoria

class Sugestao(models.Model):
    id_sugestao = models.AutoField(primary_key=True)
    nome_sugestao = models.CharField(max_length=290)
    descricao = models.CharField(max_length=255)
    endereco = models.CharField(max_length=300)
    status = models.CharField(max_length=20)
    
    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.DO_NOTHING, 
        db_column='USUARIO_ID_usuario'
    )
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.DO_NOTHING, 
        db_column='CATEGORIAS_ID_categoria'
    )

    class Meta:
        db_table = 'SUGESTAO'
        verbose_name = 'Sugestão'
        verbose_name_plural = 'Sugestões'

    def __str__(self):
        return self.nome_sugestao
