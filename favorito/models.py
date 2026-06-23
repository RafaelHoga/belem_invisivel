from django.db import models
from django.conf import settings
from ponto_turistico.models import PontoTuristico


class Favorito(models.Model):
    id_favorito = models.AutoField(primary_key=True)
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favoritos'
    )
    
    ponto_turistico = models.ForeignKey(
        PontoTuristico,
        on_delete=models.CASCADE,
        related_name='favoritos'
    )
    
    # Campos de auditoria
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
        ordering = ['-criado_em']
        # Garante que um usuário favorite apenas uma vez cada ponto
        unique_together = ['usuario', 'ponto_turistico']
        indexes = [
            models.Index(fields=['usuario', '-criado_em']),
            models.Index(fields=['ponto_turistico']),
        ]
    
    def __str__(self):
        return f"{self.usuario.username} ♥ {self.ponto_turistico.nome_ponto_turistico}"