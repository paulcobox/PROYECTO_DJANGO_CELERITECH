from django.db import models
from seguridad.models import Perfil

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from rest_framework_simplejwt.tokens import RefreshToken
TIPO_ESTADO_CHOICES = [
    ('001', 'Activado'),
    ('002', 'Desactivado')
    # ('003', 'Eliminado')
]

TIPO_OFICINA_CHOICES = [
    ('LIM', 'LIMA'),
    ('TRU', 'TRUJILLO'),
    ('ICA', 'ICA'),
    ('IQU', 'IQUITOS')
    # ('003', 'Eliminado')
]

TIPO_REGION_CHOICES = [
    ('NOR', 'NORTE'),
    ('ORI', 'ORIENTE'),
    ('RES', 'RESTO PAIS')
    # ('003', 'Eliminado')
]


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('El usuario no se ha ingresado')

        if email is None:
            raise TypeError('El correo no se ha ingresado')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('La contraseña no se ha ingresado')
        
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    perfil = models.ForeignKey(Perfil, related_name='usuarios',on_delete=models.SET_NULL,default=None, null=True, blank=True)
    estado = models.CharField(verbose_name="Estado", max_length=3, default='001',choices=TIPO_ESTADO_CHOICES)
    oficina = models.CharField(verbose_name="Oficina", max_length=3, default=None, null=True,choices=TIPO_OFICINA_CHOICES)
    region = models.CharField(verbose_name="Region", max_length=3, default=None ,null=True, choices=TIPO_REGION_CHOICES)
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    username = models.CharField(max_length=255, default='',unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'#campo con el que te vas a loguear
    # USERNAME_FIELD = 'username'#campo con el que te vas a loguear
    # REQUIRED_FIELDS = ['username']
    # REQUIRED_FIELDS = ['email']

    objects = UserManager()#para poder usar el usuario en el administrador

    def __str__(self):
        return self.email

    def is_active(self):
        if (self.estado == '001'):
            return True
        return False

    def is_desactive(self):
        if (self.estado == '002'):
            return True
        return False

    #  # JWT
    # def tokens(self):
    #     refresh = RefreshToken.for_user(self)
    #     return {
    #         'refresh': str(refresh),
    #         'access': str(refresh.access_token)
    #     }
