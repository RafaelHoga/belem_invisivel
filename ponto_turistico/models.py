from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from categoria.models import Categoria


class PontoTuristico(models.Model):
    # Mantendo sua convenção de nomenclatura, mas adicionando campos essenciais
    id_ponto_turistico = models.AutoField(primary_key=True)
    nome_ponto_turistico = models.CharField(max_length=150)  # Aumentei para 150
    telefone = models.CharField(max_length=20, blank=True, null=True)  # Tornar opcional
    descricao = models.TextField()
    rua = models.CharField(max_length=150, blank=True, null=True)
    cidade = models.CharField(max_length=100)
    
    # Campo de localização geográfica (importante para app turístico)
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        help_text="Coordenada GPS - Latitude"
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        help_text="Coordenada GPS - Longitude"
    )
    
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='pontos_turisticos'  # Permite categoria.pontos_turisticos.all()
    )
    
    # Campos para cache de avaliações (evita calcular média toda hora)
    media_avaliacoes = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_avaliacoes = models.PositiveIntegerField(default=0)
    
    # Campos de auditoria (essenciais para projeto em equipe)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)  # Soft delete
    
    class Meta:
        verbose_name = 'Ponto Turístico'
        verbose_name_plural = 'Pontos Turísticos'
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['cidade']),
            models.Index(fields=['categoria']),
            models.Index(fields=['-media_avaliacoes']),  # Para ordenar por melhor avaliados
            models.Index(fields=['latitude', 'longitude']),  # Para buscas geográficas
        ]
    
    def __str__(self):
        return f"{self.nome_ponto_turistico} - {self.cidade}"
    
    @property
    def endereco_completo(self):
        """Retorna endereço formatado"""
        partes = [self.rua, self.cidade]
        return ', '.join(filter(None, partes))