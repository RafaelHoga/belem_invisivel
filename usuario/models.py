from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome_usuario, password=None, **extra_fields):
        if not email:
            raise ValueError('O usuário deve ter um endereço de e-mail')
        email = self.normalize_email(email)
        
        # Limpeza preventiva de campos não utilizados pelo modelo personalizado
        extra_fields.pop('username', None)
        
        # Atribuição dinâmica do perfil de acesso (1 para admin/staff, 2 para comum)
        if 'id_perfil' not in extra_fields:
            if email.lower().endswith('@beleminvisivel.com'):
                extra_fields['id_perfil'] = 1
            else:
                extra_fields['id_perfil'] = 2
                
        # Sincroniza is_staff se for perfil 1
        if extra_fields.get('id_perfil') == 1:
            extra_fields.setdefault('is_staff', True)

        user = self.model(email=email, nome_usuario=nome_usuario, **extra_fields)
        user.set_password(password)  # Realiza o hashing seguro da senha automaticamente
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome_usuario, password=None, **extra_fields):
        extra_fields['id_perfil'] = 1
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True.')

        return self.create_user(email, nome_usuario, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    nome_usuario = models.CharField(max_length=75)
    email = models.EmailField(max_length=191, unique=True)
    data_nascimento = models.DateField(null=True, blank=True)
    id_perfil = models.IntegerField(default=2)

    # ADICIONE ESTA LINHA: Ela faz a ponte entre o Django e a coluna existente no MySQL
    password = models.CharField(max_length=128, db_column='senha')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # ... resto do seu código igual

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_usuario']

    class Meta:
        db_table = 'usuario'  # Garante vinculação direta com a tabela existente do MySQL

    def __str__(self):
        return self.nome_usuario