from django.db import models

# Create your models here.
from django.db import models
from categoria.models import Categoria


class PontoTuristico(models.Model):
    id_ponto_turistico = models.AutoField(primary_key=True)
    nome_ponto_turistico = models.CharField(max_length=45)
    telefone = models.CharField(max_length=20)
    descricao = models.TextField()
    rua = models.CharField(max_length=150, blank=True, null=True)
    cidade = models.CharField(max_length=100)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nome_ponto_turistico