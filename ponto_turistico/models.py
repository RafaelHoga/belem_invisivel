from django.db import models
from usuario.models import Usuario


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    descricao_categoria = models.CharField(max_length=45)

    class Meta:
        db_table = 'categoria'
        managed = False

    def __str__(self):
        return self.descricao_categoria


class PontoTuristico(models.Model):
    id_ponto_turistico = models.AutoField(primary_key=True)
    nome_ponto_turistico = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    descricao = models.TextField()
    rua = models.CharField(max_length=150, null=True, blank=True)
    bairro = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=100)
    imagem_url = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    horario_funcionamento = models.CharField(max_length=100, null=True, blank=True)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        db_column='id_categoria'
    )

    class Meta:
        db_table = 'ponto_turistico'
        managed = False

    def __str__(self):
        return self.nome_ponto_turistico


class Favorito(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario'
    )

    ponto_turistico = models.ForeignKey(
        PontoTuristico,
        on_delete=models.CASCADE,
        db_column='id_ponto_turistico'
    )

    data_favorito = models.DateTimeField()

    class Meta:
        db_table = 'favorito'
        managed = False
        unique_together = ('usuario', 'ponto_turistico')


class Avaliacao(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario'
    )

    ponto_turistico = models.ForeignKey(
        PontoTuristico,
        on_delete=models.CASCADE,
        db_column='id_ponto_turistico'
    )

    mensagem = models.TextField()
    estrela = models.IntegerField()
    data_avaliacao = models.DateTimeField()

    class Meta:
        db_table = 'avaliacao'
        managed = False
        unique_together = ('usuario', 'ponto_turistico')