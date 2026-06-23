from django.db import models


class FavoritoQuerySet(models.QuerySet):
    """
    Custom QuerySet para otimizar consultas de favoritos.
    """
    
    def do_usuario(self, usuario):
        """
        Retorna favoritos de um usuário específico com dados otimizados.
        Usa select_related para evitar N+1 queries.
        """
        return self.filter(
            usuario=usuario
        ).select_related(
            'ponto_turistico',
            'ponto_turistico__categoria'  # Otimização em cascata
        ).order_by('-data_criacao')
    
    def com_detalhes(self):
        """
        Retorna favoritos com todos os detalhes necessários para exibição.
        """
        return self.select_related(
            'usuario',
            'ponto_turistico',
            'ponto_turistico__categoria'
        ).prefetch_related(
            'ponto_turistico__avaliacoes'  # Prefetch para avaliações
        )
    
    def ativos(self):
        """
        Retorna apenas favoritos ativos (não removidos).
        """
        return self.filter(ativo=True)


class FavoritoManager(models.Manager):
    """
    Manager customizado que usa o QuerySet customizado.
    """
    
    def get_queryset(self):
        return FavoritoQuerySet(self.model, using=self._db)
    
    def do_usuario(self, usuario):
        """Atalho para o QuerySet"""
        return self.get_queryset().do_usuario(usuario)
    
    def com_detalhes(self):
        """Atalho para o QuerySet"""
        return self.get_queryset().com_detalhes()