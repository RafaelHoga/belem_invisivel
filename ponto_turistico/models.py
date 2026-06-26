from django.db import models
from usuario.models import Usuario

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    descricao_categoria = models.CharField(max_length=45)

    def __str__(self):
        return self.descricao_categoria

    class Meta:
        db_table = 'CATEGORIA'


class PontoTuristico(models.Model):
    id_ponto_turistico = models.AutoField(primary_key=True)
    nome_ponto_turistico = models.CharField(max_length=100) 
    telefone = models.CharField(max_length=20, blank=True, null=True)
    descricao = models.TextField()
    rua = models.CharField(max_length=150, blank=True, null=True)
    bairro = models.CharField(max_length=50, blank=True, null=True) 
    cidade = models.CharField(max_length=100, default='Belém')
    imagem_url = models.CharField(max_length=255, blank=True, null=True) 
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    horario_funcionamento = models.CharField(max_length=100, blank=True, null=True)
    
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.RESTRICT, 
        db_column='id_categoria'
    )

    def __str__(self):
        return self.nome_ponto_turistico

    class Meta:
        db_table = 'PONTO_TURISTICO'


class Favorito(models.Model):
    # CORREÇÃO: Usando related_name para isolar as chamadas deste app e evitar conflitos
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario', related_name='ponto_favoritos')
    id_ponto_turistico = models.ForeignKey(PontoTuristico, on_delete=models.CASCADE, db_column='id_ponto_turistico', related_name='ponto_favoritados')
    data_favorito = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'FAVORITO'
        unique_together = (('id_usuario', 'id_ponto_turistico'),)


class Avaliacao(models.Model):
    # CORREÇÃO: Usando related_name para isolar as chamadas deste app e evitar conflitos
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario', related_name='ponto_avaliacoes')
    id_ponto_turistico = models.ForeignKey(PontoTuristico, on_delete=models.CASCADE, db_column='id_ponto_turistico', related_name='ponto_avaliados')
    mensagem = models.TextField()
    estrela = models.IntegerField()
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'AVALIACAO'
        unique_together = (('id_usuario', 'id_ponto_turistico'),)