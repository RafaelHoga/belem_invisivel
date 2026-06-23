from django.db import transaction
from ponto_turistico.models import PontoTuristico
from .models import Avaliacao


@transaction.atomic
def criar_avaliacao(usuario, ponto_turistico, nota, comentario=''):
    """
    Cria uma nova avaliação e atualiza a média do ponto turístico.
    
    Args:
        usuario: Usuário que está avaliando
        ponto_turistico: Ponto turístico sendo avaliado
        nota: Nota de 1 a 5
        comentario: Comentário opcional
    
    Returns:
        Avaliacao: Objeto de avaliação criado
    
    Raises:
        ValueError: Se a nota for inválida
    """
    # Validação de negócio
    if nota < 1 or nota > 5:
        raise ValueError('Nota deve estar entre 1 e 5')
    
    # Cria a avaliação
    avaliacao = Avaliacao.objects.create(
        usuario=usuario,
        ponto_turistico=ponto_turistico,
        nota=nota,
        comentario=comentario
    )
    
    # Atualiza a média do ponto turístico
    _atualizar_media_ponto(ponto_turistico)
    
    return avaliacao


@transaction.atomic
def _atualizar_media_ponto(ponto_turistico):
    """
    Calcula e atualiza a média de avaliações do ponto turístico.
    Função privada (convenção do underscore).
    """
    # Calcula a média usando agregação do Django
    media = Avaliacao.objects.filter(
        ponto_turistico=ponto_turistico
    ).aggregate(
        media=models.Avg('nota')
    )['media'] or 0
    
    # Conta total de avaliações
    total_avaliacoes = Avaliacao.objects.filter(
        ponto_turistico=ponto_turistico
    ).count()
    
    # Atualiza o ponto turístico
    ponto_turistico.media_avaliacoes = round(media, 2)
    ponto_turistico.total_avaliacoes = total_avaliacoes
    ponto_turistico.save(update_fields=['media_avaliacoes', 'total_avaliacoes'])


@transaction.atomic
def remover_avaliacao(avaliacao):
    """
    Remove uma avaliação e atualiza a média do ponto turístico.
    """
    ponto_turistico = avaliacao.ponto_turistico
    avaliacao.delete()
    _atualizar_media_ponto(ponto_turistico)