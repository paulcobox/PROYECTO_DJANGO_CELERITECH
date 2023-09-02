from django.db import models

TIPO_ESTADO_CHOICES = [
    ('001', 'Activado'),
    ('002', 'Desactivado')
    # ('003', 'Eliminado')
]


# Create your models here.

class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name="Nombre", max_length=200, unique=True)
    estado = models.CharField(verbose_name="Estado", max_length=3, default='001',choices=TIPO_ESTADO_CHOICES)
    orden = models.IntegerField(verbose_name="Orden", default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "menu"
        verbose_name_plural = "menus"
        ordering = ['orden']

    def __str__(self):
        return self.nombre


class MenuItem(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.ForeignKey(Menu, related_name='menuitems',on_delete=models.CASCADE)
    # father = models.ForeignKey('Menu', on_delete=models.CASCADE, default=None, null=True, blank=True)
    nombre = models.CharField(verbose_name="Nombre", max_length=200)
    estado = models.CharField(verbose_name="Estado", max_length=3, default='001',choices=TIPO_ESTADO_CHOICES)
    url = models.CharField(verbose_name="Url", max_length=200)
    orden = models.IntegerField(verbose_name="Orden", default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "menuitem"
        verbose_name_plural = "menuitems"
        ordering = ['orden']

    def __str__(self):
        return self.nombre

    @property
    def get_privilegio_by_perfil(self, perfil):
        privilegio = Privilegio.objects.filter(perfil=perfil,menuitem__id=self.id).first()
        return privilegio


class Perfil(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name="Nombre de Perfil",help_text = "Ingrese solo alfanumericos", max_length=200)
    descripcion = models.TextField(verbose_name="Descripcion", blank=True, null=True)
    estado = models.CharField(verbose_name="Estado", max_length=3, default='001',choices=TIPO_ESTADO_CHOICES)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfiles"
        ordering = ['created']

    def __str__(self):
        return self.nombre


    def is_active(self):
        if (self.estado == '001'):
            return True
        return False

    def is_desactive(self):
        if (self.estado == '002'):
            return True
        return False

class Privilegio(models.Model):
    id = models.AutoField(primary_key=True)
    menuitem = models.ForeignKey(MenuItem, related_name='privilegios',on_delete=models.CASCADE)
    perfil = models.ForeignKey(Perfil, related_name='privilegios',on_delete=models.CASCADE)
    view = models.CharField(verbose_name="view", default='0',max_length=1)
    create = models.CharField(verbose_name="create", default='0',max_length=1)
    update = models.CharField(verbose_name="update", default='0',max_length=1)
    delete = models.CharField(verbose_name="delete", default='0',max_length=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "privilegio"
        verbose_name_plural = "privilegios"
        ordering = ['perfil','menuitem']

    def __str__(self):
        return '{}'.format(self.perfil,self.menuitem)




# class Usuario(models.Model):
#     id = models.AutoField(primary_key=True)
#     perfil = models.ForeignKey(Perfil, related_name='usuarios',on_delete=models.CASCADE)
#     nombres = models.CharField(max_length=100, default='')
#     apellidos = models.CharField(max_length=100, default='')
#     correo = models.EmailField(max_length=50)
#     estado = models.CharField(verbose_name="Estado", max_length=3, default='001',choices=TIPO_ESTADO_CHOICES)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = "usuario"
#         verbose_name_plural = "usuarios"
#         ordering = ['created','updated']

#     def __str__(self):
#         return '{}'.format(self.correo)

#     def is_active(self):
#         if (self.estado == '001'):
#             return True
#         return False

#     def is_desactive(self):
#         if (self.estado == '002'):
#             return True
#         return False