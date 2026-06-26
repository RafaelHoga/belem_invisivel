from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome_usuario, password=None, **extra_fields):
        if not email:
            raise ValueError('O usuário deve ter um endereço de e-mail')
        email = self.normalize_email(email)
        
        # Remove os campos que o Django tenta colocar automaticamente e não existem no seu banco
        extra_fields.pop('username', None)
        extra_fields.pop('last_login', None)
        extra_fields.pop('is_superuser', None)
        extra_fields.pop('is_staff', None)
        
        # Se não foi passado um perfil, define baseado no e-mail ou padrão
        if 'id_perfil' not in extra_fields:
            if email.lower().endswith('@beleminvisivel.com'):
                extra_fields['id_perfil'] = 1  # Administrador
            else:
                extra_fields['id_perfil'] = 2  # Usuário comum

        user = self.model(email=email, nome_usuario=nome_usuario, **extra_fields)
        user.set_password(password)  # Criptografa na coluna mapeada como 'senha'
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome_usuario, password=None, **extra_fields):
        # 1. Define o ID do perfil como Administrador (1)
        extra_fields['id_perfil'] = 1
        
        # 2. Força uma data padrão diretamente aqui para evitar o erro de 'cannot be null' do MySQL
        extra_fields['data_nascimento'] = '2000-01-01'
        
        return self.create_user(email, nome_usuario, password, **extra_fields)


class Usuario(AbstractBaseUser):  
    id_usuario = models.AutoField(primary_key=True)
    nome_usuario = models.CharField(max_length=75)
    email = models.EmailField(max_length=191, unique=True)
    data_nascimento = models.DateField(null=True, blank=True)
    id_perfil = models.IntegerField(default=2)

    # Caminho da foto na coluna 'foto_perfil' do MySQL
    foto_perfil = models.ImageField(upload_to='perfis/', null=True, blank=True, db_column='foto_perfil')

    password = models.CharField(max_length=128, db_column='senha')
    last_login = None

    @property
    def is_staff(self): 
        return self.id_perfil == 1

    @property
    def is_superuser(self): 
        return self.id_perfil == 1

    def has_perm(self, perm, obj=None): 
        return self.id_perfil == 1

    def has_module_perms(self, app_label): 
        return self.id_perfil == 1

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_usuario']

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.nome_usuario