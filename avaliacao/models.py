from django.db import models
from usuario.models import Usuario                  # Importa do app usuario
from ponto_turistico.models import PontoTuristico  # Importa do app ponto_turistico

class Avaliacao(models.Model):
    ponto_turistico = models.ForeignKey(
        PontoTuristico, 
        on_delete=models.DO_NOTHING, 
        db_column='PONTO_TURISTICO_ID_ponto_turistico'
    )
    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.DO_NOTHING, 
        db_column='USUARIO_ID_usuario'
    )
    mensagem = models.CharField(max_length=300)
    estrela = models.IntegerField()

    class Meta:
        db_table = 'AVALIACAO'
        unique_together = (('ponto_turistico', 'usuario'),)
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'