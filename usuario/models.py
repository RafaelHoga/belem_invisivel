from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome_usuario, password=None, **extra_fields):
        if not email:
            raise ValueError('O usuário deve ter um endereço de e-mail')
        email = self.normalize_email(email)
        
        extra_fields.pop('username', None)
        extra_fields.pop('last_login', None)
        
        # REMOÇÃO CRÍTICA: Remove as propriedades dinâmicas que não possuem setter no modelo
        extra_fields.pop('is_superuser', None)
        extra_fields.pop('is_staff', None)
        
        # Garante a definição do ID do perfil antes de salvar
        if 'perfil_id' not in extra_fields and 'perfil' not in extra_fields:
            perfil_id = 1 if email.lower().endswith('@beleminvisivel.com') else 2
            extra_fields['perfil_id'] = perfil_id

        user = self.model(email=email, nome_usuario=nome_usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome_usuario, password=None, **extra_fields):
        extra_fields['perfil_id'] = 1
        extra_fields['data_nascimento'] = '2000-01-01'
        
        # Garante que não passaremos chaves indesejadas para o create_user
        extra_fields.pop('is_superuser', None)
        extra_fields.pop('is_staff', None)
        
        return self.create_user(email, nome_usuario, password, **extra_fields)


class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True, db_column='id_perfil')
    descricao_perfil = models.CharField(max_length=45, db_column='descricao_perfil')

    class Meta:
        db_table = 'perfil'
        managed = False

    def __str__(self):
        return self.descricao_perfil


class Usuario(AbstractBaseUser):
    id_usuario = models.AutoField(primary_key=True, db_column='id_usuario')
    nome_usuario = models.CharField(max_length=75, db_column='nome_usuario')
    email = models.EmailField(max_length=191, unique=True, db_column='email')
    data_nascimento = models.DateField(null=True, blank=True, db_column='data_nascimento')
    password = models.CharField(max_length=128, db_column='senha')
    foto_perfil = models.ImageField(upload_to='perfis/', null=True, blank=True, db_column='foto_perfil')
    
    # AJUSTE: Desativando o last_login para não buscar a coluna inexistente no MySQL
    last_login = None
    
    # Mapeamento da chave estrangeira conectando ao Perfil
    perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT, db_column='id_perfil')

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_usuario']

    class Meta:
        db_table = 'usuario'
        managed = False

    def __str__(self):
        return self.nome_usuario

    @property
    def is_staff(self):
        return self.perfil_id == 1

    @property
    def is_superuser(self):
        return self.perfil_id == 1

    @property
    def is_active(self):
        return True

    def has_perm(self, perm, obj=None):
        return self.perfil_id == 1

    def has_module_perms(self, app_label):
        return self.perfil_id == 1