from django.db import models
from usuario.models import Usuario
from ponto_turistico.models import Categoria


class Sugestao(models.Model):
    id_sugestao = models.AutoField(primary_key=True, db_column='id_sugestao')
    nome_sugestao = models.CharField(max_length=200)
    descricao = models.TextField()
    endereco = models.CharField(max_length=300)

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario'
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        db_column='id_categoria'
    )

    status = models.CharField(max_length=20, default='Pendente')
    data_sugestao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sugestao'
        managed = False