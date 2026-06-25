from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

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



class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)

    nome_usuario = models.CharField(max_length=75)

    email = models.EmailField(max_length=191, unique=True)

    data_nascimento = models.DateField(null=True, blank=True)

    id_perfil = models.IntegerField(default=2)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_usuario']

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.nome_usuario

    