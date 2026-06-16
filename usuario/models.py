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
        
        # Identificação automática com base no e-mail
        if 'perfil_id' not in extra_fields:
            if email.lower().endswith('@beleminvisivel.com'):
                extra_fields['perfil_id'] = 1  # ID do perfil ADM no seu banco
            else:
                extra_fields['perfil_id'] = 2  # ID do perfil USUÁRIO no seu banco
                
        user = self.model(email=email, nome_usuario=nome_usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome_usuario, password=None, **extra_fields):
        extra_fields['perfil_id'] = 1  # Garante perfil ADM
        return self.create_user(email, nome_usuario, password, **extra_fields)


class Usuario(AbstractBaseUser):
    id_usuario = models.AutoField(primary_key=True)
    nome_usuario = models.CharField(max_length=75)
    email = models.EmailField(unique=True)
    
    # AJUSTE 1: Adicionado null=True para não quebrar o banco se a data não for enviada no cadastro
    data_nascimento = models.DateField(null=True, blank=True)
    
    perfil_id = models.IntegerField(db_column='PERFIL_ID_perfil')
    
    # Mapeamento físico para a coluna do teu banco MySQL
    password = models.CharField(max_length=128, db_column='senha')

    # PROPRIEDADE DO DJANGO: Corrige o bug do last_login que resolvemos antes
    @property
    def last_login(self):
        return None

    @last_login.setter
    def last_login(self, value):
        pass

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_usuario']

    # AJUSTE 2: Alterado de PERFIL_ID_perfil para perfil_id (o nome da variável Python)
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

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.nome_usuario