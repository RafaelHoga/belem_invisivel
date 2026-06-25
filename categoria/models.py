from django.db import models

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True, db_column='ID_categoria')
    descricao_categoria = models.CharField(max_length=45)

    class Meta:
        db_table = 'CATEGORIA'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.descricao_categoria