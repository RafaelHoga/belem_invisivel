from django.db import models

class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True, db_column='ID_perfil')
    descricao_perfil = models.CharField(max_length=45)

    class Meta:
        db_table = 'PERFIL'
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return self.descricao_perfil
