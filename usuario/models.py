from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome_usuario, password=None, **extra_fields):
        if not email:
            raise ValueError('O usuário deve ter um endereço de e-mail')
        email = self.normalize_email(email)
        
        # Remove chaves redundantes geradas por formulários ou padrões do Django
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
        # Garante a definição do ID do perfil antes de salvar
        if 'perfil' not in extra_fields and 'perfil_id' not in extra_fields:
            perfil_id = 1 if email.lower().endswith('@beleminvisivel.com') else 2
            extra_fields['perfil_id'] = perfil_id
                
        # Sincroniza permissões de staff se for o perfil administrador (ID 1)
        perfil_atual_id = extra_fields.get('perfil_id') or (extra_fields['perfil'].pk if 'perfil' in extra_fields else 2)
        if perfil_atual_id == 1:
            extra_fields.setdefault('is_staff', True)

        user = self.model(email=email, nome_usuario=nome_usuario, **extra_fields)
        user.set_password(password)  # Encripta a senha usando o padrão do Django
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome_usuario, password=None, **extra_fields):
        extra_fields['perfil_id'] = 1
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
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
class Usuario(AbstractBaseUser):
    id_usuario = models.AutoField(primary_key=True, db_column='id_usuario')
    nome_usuario = models.CharField(max_length=75, db_column='nome_usuario')
    email = models.EmailField(max_length=191, unique=True, db_column='email')
    data_nascimento = models.DateField(null=True, blank=True, db_column='data_nascimento')
    
    # AJUSTE CHAVE: O Django herda implicitamente o atributo 'password'. 
    # Apontamos ele diretamente para a coluna física 'password' que está travando o banco.
    # O Django se encarregará de preenchê-lo perfeitamente com o hash gerado.
    password = models.CharField(max_length=128, db_column='password')
    
    # Mapeamento exato da chave estrangeira conforme visto no erro anterior
    perfil = models.ForeignKey('Perfil', on_delete=models.PROTECT, db_column='PERFIL_ID_perfil')

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_usuario']

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.nome_usuario
    # Colunas adicionais mapeadas a partir da estrutura da sua tabela
    last_login = models.DateTimeField(null=True, blank=True, db_column='last_login')

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
        managed = False

    def __str__(self):
        return self.nome_usuario


class Favorito(models.Model):
    id_favorito = models.AutoField(db_column='id_favorito', primary_key=True)
    # Mudamos o nome do atributo para 'id_usuario' e 'id_ponto_turistico'
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_ponto_turistico = models.ForeignKey('ponto_turistico.PontoTuristico', on_delete=models.CASCADE, db_column='id_ponto_turistico')

    class Meta:
        db_table = 'favorito'
        managed = False


class Avaliacao(models.Model):
    id_avaliacao = models.AutoField(primary_key=True, db_column='id_avaliacao')
    # Mudamos o nome do atributo para coincidir exatamente com o esperado pelo ORM legado
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_ponto_turistico = models.ForeignKey('ponto_turistico.PontoTuristico', on_delete=models.CASCADE, db_column='id_ponto_turistico')
    comentario = models.TextField(db_column='comentario', null=True, blank=True)
    nota = models.IntegerField(db_column='nota')

    class Meta:
        db_table = 'avaliacao'
        managed = False


class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True, db_column='id_perfil')
    descricao_perfil = models.CharField(max_length=45, db_column='descricao_perfil')

    class Meta:
        db_table = 'perfil'
        managed = False
