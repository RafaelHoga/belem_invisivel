from django.db import models
from django.conf import settings  # <-- ADICIONE ESSE IMPORT AQUI
from categoria.models import Categoria


class PontoTuristico(models.Model):
    id_ponto_turistico = models.AutoField(primary_key=True)
    nome_ponto_turistico = models.CharField(max_length=45)
    telefone = models.CharField(max_length=20)
    descricao = models.TextField()
    rua = models.CharField(max_length=150, blank=True, null=True)
    cidade = models.CharField(max_length=100)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nome_ponto_turistico


# --- SEÇÃO DA AVALIAÇÃO ---
class Avaliacao(models.Model):
    id_avaliacao = models.AutoField(primary_key=True)
    
    # Alterado de 'Usuario' para settings.AUTH_USER_MODEL para corrigir o NameError
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
    
    nota = models.IntegerField()  # Guardará o valor das estrelas (1 a 5)
    comentario = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)  # Salva a data automaticamente

    class Meta:
        db_table = 'avaliacao'
        ordering = ['-data_criacao']

    def __str__(self):
        nome = getattr(self.usuario, 'nome_usuario', self.usuario.get_username())
        return f"Nota {self.nota} por {self.usuario.nome_usuario} em {self.ponto_turistico.nome_ponto_turistico}"
    