from django.db import models
from usuario.models import Usuario
from ponto_turistico.models import Categoria

class Sugestao(models.Model):
    id_sugestao = models.AutoField(primary_key=True)
    nome_sugestao = models.CharField(max_length=200)
    descricao = models.TextField()
    endereco = models.CharField(max_length=300)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='id_categoria')
    status = models.CharField(max_length=20, default='Pendente') # Pendente, Aprovado, Recusado
    data_sugestao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_sugestao

    class Meta:
        db_table = 'SUGESTAO'