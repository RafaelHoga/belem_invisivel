from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    id_usuario = models.AutoField(primary_key=True)
    nome_usuario = models.CharField(max_length=75)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_usuario']

    def __str__(self):
        return self.nome_usuario
