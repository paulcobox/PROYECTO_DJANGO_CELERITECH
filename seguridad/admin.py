from django.contrib import admin

# Register your models here.
from .models import Menu, MenuItem, Perfil, Privilegio

# Register your models here.
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['id','nombre','estado']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['id','menu','nombre','estado','url']

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['id','nombre','estado']

@admin.register(Privilegio)
class PrivilegioAdmin(admin.ModelAdmin):
    list_display = ['id','menuitem','perfil','view','create','update','delete']

# @admin.register(Usuario)
# class UsuarioAdmin(admin.ModelAdmin):
#     list_display = ['id','nombres','apellidos','correo','perfil','estado']