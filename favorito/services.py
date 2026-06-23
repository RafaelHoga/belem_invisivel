from django.db import transaction
from django.shortcuts import get_object_or_404
from ponto_turistico.models import PontoTuristico
from .models import Favorito


@transaction.atomic
def alternar_favorito(usuario, ponto_id):
    """
    Adiciona ou remove um ponto turístico dos favoritos do usuário (toggle).
    
    Args:
        usuario: Usuário que está favoritando
        ponto_id: ID do ponto turístico
    
    Returns:
        tuple: (favorito, criado)
            - favorito: Objeto Favorito (se criado) ou None (se removido)
            - criado: Boolean indicando se foi criado (True) ou removido (False)
    
    Raises:
        PontoTuristico.DoesNotExist: Se o ponto não existir
    """
    # Busca o ponto turístico
    ponto_turistico = get_object_or_404(PontoTuristico, id=ponto_id)
    
    # Verifica se já existe favorito
    favorito_existente = Favorito.objects.filter(
        usuario=usuario,
        ponto_turistico=ponto_turistico
    ).first()
    
    if favorito_existente:
        # Remove o favorito
        favorito_existente.delete()
        return None, False
    else:
        # Cria o favorito
        favorito = Favorito.objects.create(
            usuario=usuario,
            ponto_turistico=ponto_turistico
        )
        return favorito, True


def usuario_favoritou(usuario, ponto_id):
    """
    Verifica se o usuário já favoritou um ponto turístico.
    
    Args:
        usuario: Usuário a verificar
        ponto_id: ID do ponto turístico
    
    Returns:
        bool: True se favoritou, False caso contrário
    """
    return Favorito.objects.filter(
        usuario=usuario,
        ponto_turistico_id=ponto_id
    ).exists()


def listar_favoritos_usuario(usuario):
    """
    Lista todos os favoritos de um usuário com dados otimizados.
    
    Args:
        usuario: Usuário cujos favoritos serão listados
    
    Returns:
        QuerySet: Favoritos otimizados com select_related
    """
    return Favorito.objects.do_usuario(usuario)