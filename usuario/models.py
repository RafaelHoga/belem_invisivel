from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome_usuario, password=None, **extra_fields):
        if not email:
            raise ValueError('O usuário deve ter um endereço de e-mail')
        email = self.normalize_email(email)
        
        extra_fields.pop('username', None)
        extra_fields.pop('is_staff', None)
        extra_fields.pop('is_superuser', None)
        
        # Ajustado para usar o nome correto do campo: id_perfil
        if 'id_perfil' not in extra_fields:
            if email.lower().endswith('@beleminvisivel.com'):
                extra_fields['id_perfil'] = 1
            else:
                extra_fields['id_perfil'] = 2
                
        user = self.model(email=email, nome_usuario=nome_usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome_usuario, password=None, **extra_fields):
        extra_fields['id_perfil'] = 1
        return self.create_user(email, nome_usuario, password, **extra_fields)


class Usuario(AbstractBaseUser):
    id_usuario = models.AutoField(primary_key=True)
    nome_usuario = models.CharField(max_length=75)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField(null=True, blank=True)
    
    # CORREÇÃO 1: Apontando para o nome exato da coluna do seu MySQL Workbench
    id_perfil = models.IntegerField(db_column='id_perfil', default=2)

    # CORREÇÃO 2: Removida a linha duplicada 'password = ...' 
    # O Django já possui o campo password por padrão. Para mapear o nome da coluna física 
    # para 'senha', nós apenas sobrescrevemos o db_column do campo herdado na inicialização:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('password').db_column = 'senha'

    @property
    def last_login(self):
        return None

    @last_login.setter
    def last_login(self, value):
        pass

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_usuario']

    @property
    def is_staff(self):
        return self.id_perfil == 1

    @property
    def is_superuser(self):
        return self.id_perfil == 1

    @property
    def is_active(self):
        return True

    def has_perm(self, perm, obj=None):
        return self.id_perfil == 1

    def has_module_perms(self, app_label):
        return self.id_perfil == 1

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.nome_usuario
    