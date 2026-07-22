from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome_usuario, password=None, **extra_fields):
        if not email:
            raise ValueError('O usuário deve ter um endereço de e-mail')
        
        email = self.normalize_email(email)
        
        # Lógica de negócio: define o perfil com base no domínio do e-mail
        if 'perfil_id' not in extra_fields and 'perfil' not in extra_fields:
            perfil_id = 1 if email.lower().endswith('@beleminvisivel.com') else 2
            extra_fields['perfil_id'] = perfil_id
            
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)

        user = self.model(email=email, nome_usuario=nome_usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome_usuario, password=None, **extra_fields):
        # Superusuários devem ter perfil_id = 1 (Administrador)
        extra_fields.setdefault('perfil_id', 1)
        
        # Garante as flags de superusuário e staff
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # Removido o hack de data_nascimento = '2000-01-01'. 
        # O campo agora é opcional (null=True, blank=True) no model.

        return self.create_user(email, nome_usuario, password, **extra_fields)


class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True, db_column='id_perfil')
    descricao_perfil = models.CharField(max_length=45, db_column='descricao_perfil')

    class Meta:
        db_table = 'perfil'
        managed = False  # Preservando a gestão externa pelo Workbench

    def __str__(self):
        return self.descricao_perfil


class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True, db_column='id_usuario')
    nome_usuario = models.CharField(max_length=75, db_column='nome_usuario')
    email = models.EmailField(max_length=100, unique=True, db_column='email')
    data_nascimento = models.DateField(null=True, blank=True, db_column='data_nascimento')
    foto_perfil = models.ImageField(upload_to='perfis/', null=True, blank=True, db_column='foto_perfil')
    
    # Relação com Perfil
    perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT, db_column='id_perfil')

    # --- CAMPOS ADICIONADOS PARA COMPATIBILIDADE COM O ADMIN E MANAGER ---
    is_active = models.BooleanField(default=True, db_column='is_active', help_text='Indica se este usuário deve ser tratado como ativo.')
    is_staff = models.BooleanField(default=False, db_column='is_staff', help_text='Indica se o usuário pode acessar o admin site.')
    # O AbstractBaseUser já fornece 'last_login', mas 'date_joined' precisa ser declarado
    date_joined = models.DateTimeField(default=timezone.now, db_column='date_joined', help_text='Data de registro do usuário.')
    # ---------------------------------------------------------------------

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_usuario']

    class Meta:
        db_table = 'usuario'
        managed = False

    def __str__(self):
        return self.nome_usuario    # Os métodos has_perm e has_module_perms NÃO são mais necessários aqui.
    # O PermissionsMixin já fornece implementações robustas e padrão para eles.