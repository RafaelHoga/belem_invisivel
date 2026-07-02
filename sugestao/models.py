from django.db import models
from usuario.models import Usuario
from ponto_turistico.models import Categoria

from django.db import models


class Categoria(models.Model):
    id_categoria = models.AutoField(db_column='ID_categoria', primary_key=True)
    descricao_categoria = models.CharField(max_length=45)

    class Meta:
        db_table = 'CATEGORIAS'
        managed = False

    def __str__(self):
        return self.descricao_categoria


class Usuario(models.Model):
    id_usuario = models.AutoField(db_column='ID_usuario', primary_key=True)
    nome_usuario = models.CharField(max_length=75)
    email = models.EmailField(max_length=45)
    senha = models.CharField(max_length=30)
    data_nascimento = models.DateField()

    class Meta:
        db_table = 'USUARIO'
        managed = False

    def __str__(self):
        return self.nome_usuario


class Sugestao(models.Model):
    id_sugestao = models.AutoField(db_column='id_sugestao', primary_key=True)
    descricao = models.CharField(max_length=255)
    endereco = models.CharField(max_length=300)
    nome_sugestao = models.CharField(max_length=290)

    usuario = models.ForeignKey(
        Usuario,
        db_column='USUARIO_ID_usuario',
        on_delete=models.CASCADE
    )

    categoria = models.ForeignKey(
        Categoria,
        db_column='CATEGORIAS_ID_categoria',
        on_delete=models.CASCADE
    )

    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'SUGESTAO'
        managed = False
