# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# class UsuarioManager(BaseUserManager):
#     def create_user(self, email, nome_usuario, password=None, **extra_fields):
#         if not email:
#             raise ValueError('O usuário deve ter um endereço de e-mail')
#         email = self.normalize_email(email)
        
#         # Remove campos padrão do Django que o ModelBackend injeta por engano
#         extra_fields.pop('username', None)
#         extra_fields.pop('is_staff', None)
#         extra_fields.pop('is_superuser', None)
        
#         # Identificação automática com base no e-mail
#         if 'perfil_id' not in extra_fields:
#             if email.lower().endswith('@beleminvisivel.com'):
#                 extra_fields['perfil_id'] = 1  # ID do perfil ADM no seu banco
#             else:
#                 extra_fields['perfil_id'] = 2  # ID do perfil USUÁRIO no seu banco
                
#         user = self.model(email=email, nome_usuario=nome_usuario, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, nome_usuario, password=None, **extra_fields):
#         extra_fields['perfil_id'] = 1  # Garante perfil ADM
#         return self.create_user(email, nome_usuario, password, **extra_fields)


# class Usuario(AbstractBaseUser):
#     id_usuario = models.AutoField(primary_key=True)
#     nome_usuario = models.CharField(max_length=75)
#     email = models.EmailField(unique=True)
    
#     # AJUSTE 1: Adicionado null=True para não quebrar o banco se a data não for enviada no cadastro
#     data_nascimento = models.DateField(null=True, blank=True)
    
#     perfil_id = models.IntegerField(db_column='PERFIL_ID_perfil')
    
#     # Mapeamento físico para a coluna do teu banco MySQL
#     password = models.CharField(max_length=128, db_column='senha')

#     # PROPRIEDADE DO DJANGO: Corrige o bug do last_login que resolvemos antes
#     @property
#     def last_login(self):
#         return None

#     @last_login.setter
#     def last_login(self, value):
#         pass

#     objects = UsuarioManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['nome_usuario']

#     # AJUSTE 2: Alterado de PERFIL_ID_perfil para perfil_id (o nome da variável Python)
#     @property
#     def is_staff(self):
#         return self.perfil_id == 1

#     @property
#     def is_superuser(self):
#         return self.perfil_id == 1

#     @property
#     def is_active(self):
#         return True

#     def has_perm(self, perm, obj=None):
#         return self.perfil_id == 1

#     def has_module_perms(self, app_label):
#         return self.perfil_id == 1

#     class Meta:
#         db_table = 'USUARIO'

#     def __str__(self):
#         return self.nome_usuario

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome_usuario, password=None, **extra_fields):
        if not email:
            raise ValueError('O usuário deve ter um endereço de e-mail')
        email = self.normalize_email(email)
        
        extra_fields.pop('username', None)
        extra_fields.pop('last_login', None)
        extra_fields.pop('is_superuser', None)
        extra_fields.pop('is_staff', None)
        
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
    email = models.EmailField(max_length=100, unique=True, db_column='email')
    data_nascimento = models.DateField(db_column='data_nascimento')
    foto_perfil = models.ImageField(upload_to='perfis/', null=True, blank=True, db_column='foto_perfil')
    
    # CORREÇÃO CRÍTICA: Apontando para a coluna correta 'password' que está no seu MySQL
    password = models.CharField(max_length=255, db_column='password')
    
    # Ajustando para usar a coluna física id_perfil do banco
    perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT, db_column='id_perfil')
    
    # REATIVAÇÃO: Seu banco possui essas colunas fisicamente, então mapeamos elas aqui
    last_login = models.DateTimeField(null=True, blank=True, db_column='last_login')
    is_superuser = models.BooleanField(default=False, db_column='is_superuser')
    is_staff = models.BooleanField(default=False, db_column='is_staff')
    is_active = models.BooleanField(default=True, db_column='is_active')
    date_joined = models.DateTimeField(auto_now_add=True, db_column='date_joined')

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_usuario']

    class Meta:
        db_table = 'usuario'
        managed = False  # Continua como False pois você gerencia o banco pelo Workbench

    def __str__(self):
        return self.nome_usuario

    # Métodos obrigatórios do Django Custom User que usam as colunas reais agora
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Favorito(models.Model):
    id_favorito = models.AutoField(db_column='id_favorito', primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario', related_name='usuario_favoritos_set')
    id_ponto_turistico = models.ForeignKey('ponto_turistico.PontoTuristico', on_delete=models.CASCADE, db_column='id_ponto_turistico', related_name='ponto_favoritos_usuario_set')

    class Meta:
        db_table = 'favorito'
        managed = False


class Avaliacao(models.Model):
    id_avaliacao = models.AutoField(primary_key=True, db_column='id_avaliacao')
    estrela = models.IntegerField(db_column='estrela')
    mensagem = models.TextField(db_column='mensagem', blank=True, null=True)
    
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario', related_name='usuario_avaliacoes_set')
    id_ponto_turistico = models.ForeignKey('ponto_turistico.PontoTuristico', models.DO_NOTHING, db_column='id_ponto_turistico', related_name='ponto_avaliacoes_usuario_set')

    class Meta:
        db_table = 'avaliacao'
        managed = False