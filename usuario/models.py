from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome_usuario, password=None, **extra_fields):
        if not email:
            raise ValueError("Informe um e-mail")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            nome_usuario=nome_usuario,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome_usuario, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, nome_usuario, password, **extra_fields)


class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    descricao_perfil = models.CharField(max_length=45)

    class Meta:
        db_table = "perfil"
        managed = False


class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    nome_usuario = models.CharField(max_length=75)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField()

    perfil = models.ForeignKey(
        Perfil,
        on_delete=models.PROTECT,
        db_column="id_perfil"
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome_usuario"]

    class Meta:
        db_table = "usuario"
        managed = False

    def __str__(self):
        return self.nome_usuario


