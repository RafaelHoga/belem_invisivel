from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from ponto_turistico.models import PontoTuristico


class Avaliacao(models.Model):
    id_avaliacao = models.AutoField(primary_key=True)
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='avaliacoes'
    )
    
    ponto_turistico = models.ForeignKey(
        PontoTuristico,
        on_delete=models.CASCADE,
        related_name='avaliacoes'
    )
    
    nota = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Nota de 1 a 5 estrelas"
    )
    
    comentario = models.TextField(
        blank=True,
        null=True,
        max_length=1000
    )
    
    # Campos de auditoria
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['-criado_em']
        # Garante que um usuário avalie apenas uma vez por ponto
        unique_together = ['usuario', 'ponto_turistico']
        indexes = [
            models.Index(fields=['ponto_turistico', '-criado_em']),
            models.Index(fields=['usuario']),
        ]
    
    def __str__(self):
        return f"{self.usuario.username} - {self.ponto_turistico.nome_ponto_turistico} ({self.nota}★)"