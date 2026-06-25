from django.db import models
from usuario.models import Usuario                  # Importa do app usuario
from ponto_turistico.models import PontoTuristico  # Importa do app ponto_turistico

class Favorito(models.Model):
    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.DO_NOTHING, 
        db_column='USUARIO_ID_usuario'
    )
    ponto_turistico = models.ForeignKey(
        PontoTuristico, 
        on_delete=models.DO_NOTHING, 
        db_column='PONTO_TURISTICO_ID_ponto_turistico'
    )
    data_favorito = models.DateField()

    class Meta:
        db_table = 'FAVORITO'
        unique_together = (('usuario', 'ponto_turistico'),)
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
