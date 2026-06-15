from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome_usuario, password=None, **extra_fields):
        if not email:
            raise ValueError('O usuário deve ter um endereço de e-mail')
        email = self.normalize_email(email)
        
        # Remove campos padrão do Django que o ModelBackend injeta por engano
        extra_fields.pop('username', None)
        extra_fields.pop('is_staff', None)
        extra_fields.pop('is_superuser', None)
        
        user = self.model(email=email, nome_usuario=nome_usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome_usuario, password=None, **extra_fields):
        return self.create_user(email, nome_usuario, password, **extra_fields)


class Usuario(AbstractBaseUser):
    id_usuario = models.AutoField(primary_key=True)
    nome_usuario = models.CharField(max_length=75)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField(null=True, blank=True)
    
    # Mapeamento físico para a coluna do teu banco MySQL
    password = models.CharField(max_length=128, db_column='senha')

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_usuario']

    # PROPRIEDADES VIRTUAIS: Impedem que o Django quebre ao verificar permissões de sessão
    @property
    def is_staff(self):
        return False

    @property
    def is_superuser(self):
        return False

    @property
    def is_active(self):
        return True

    def has_perm(self, perm, obj=None):
        return False

    def has_module_perms(self, app_label):
        return False

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.nome_usuario
