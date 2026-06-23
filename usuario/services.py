from django.db import transaction
from .models import Usuario


@transaction.atomic
def criar_usuario(email, nome_usuario, senha, data_nascimento=None):
    """
    Service responsável por criar um novo usuário no sistema.
    Centraliza a lógica de negócio do cadastro.
    
    Args:
        email: E-mail do usuário (usado como login)
        nome_usuario: Nome completo do usuário
        senha: Senha em texto puro (será hasheada pelo manager)
        data_nascimento: Data de nascimento (opcional)
    
    Returns:
        Usuario: Instância do usuário criado
    
    Raises:
        ValueError: Se os dados forem inválidos
    """
    if not email or not nome_usuario or not senha:
        raise ValueError('E-mail, nome e senha são obrigatórios.')
    
    if Usuario.objects.filter(email=email).exists():
        raise ValueError('Este e-mail já está cadastrado no sistema.')
    
    # Cria o usuário usando o manager customizado
    usuario = Usuario.objects.create_user(
        email=email,
        nome_usuario=nome_usuario,
        password=senha,
        data_nascimento=data_nascimento
    )
    
    return usuario