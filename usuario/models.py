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


class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True, db_column='id_perfil')
    descricao_perfil = models.CharField(max_length=45, db_column='descricao_perfil')

    class Meta:
        db_table = 'perfil'
        managed = False  # Informa ao Django para usar a tabela que você já criou no MySQL


class Usuario(AbstractBaseUser):
    id_usuario = models.AutoField(primary_key=True, db_column='id_usuario')
    nome_usuario = models.CharField(max_length=75)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField(null=True, blank=True)
    
    # Alterado para ForeignKey real para o Django entender o relacionamento com a tabela perfil
    id_perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT, db_column='id_perfil', default=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('password').db_column = 'senha'

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_usuario']

    last_login = models.DateTimeField(null=True, blank=True, db_column='last_login')

    @property
    def is_staff(self):
        return self.id_perfil_id == 1

    @property
    def is_superuser(self):
        return self.id_perfil_id == 1

    @property
    def is_active(self):
        return True

    def has_perm(self, perm, obj=None):
        return self.id_perfil_id == 1

    def has_module_perms(self, app_label):
        return self.id_perfil_id == 1

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.nome_usuario


class Favorito(models.Model):
    id_favorito = models.AutoField(primary_key=True, db_column='id_favorito')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    # Aponta para o app ponto_turistico e o modelo PontoTuristico
    id_ponto_turistico = models.ForeignKey('ponto_turistico.PontoTuristico', on_delete=models.CASCADE, db_column='id_ponto_turistico')

    class Meta:
        db_table = 'favorito'
        managed = False


class Avaliacao(models.Model):
    id_avaliacao = models.AutoField(primary_key=True, db_column='id_avaliacao')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_ponto_turistico = models.ForeignKey('ponto_turistico.PontoTuristico', on_delete=models.CASCADE, db_column='id_ponto_turistico')
    comentario = models.TextField(db_column='comentario', null=True, blank=True)
    nota = models.IntegerField(db_column='nota')

    class Meta:
        db_table = 'avaliacao'
        managed = False