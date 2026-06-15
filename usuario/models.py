from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    id_usuario = models.AutoField(primary_key=True)
    nome_usuario = models.CharField(max_length=75)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField(null=True, blank=True)
    
    #ADICIONE A LINHA ABAIXO PARA USAR O EMAIL COM O BACO DE DADOS:
    password = models.CharField(max_length=128, db_column='senha')
    
    # DESATIVANDO OS CAMPOS PADRÃO DO DJANGO QUE NÃO EXISTIU NO SEU MYSQL:
    last_login = None
    first_name = None
    last_name = None
    is_staff = None
    is_active = None
    is_superuser = None
    date_joined = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_usuario']
    
    class Meta:
        db_table ='usuario' # Isso força o Django a usar o nome exato do seu diagrama

    def __str__(self):
        return self.nome_usuario 
