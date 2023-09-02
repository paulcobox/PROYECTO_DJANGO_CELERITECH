from django.contrib import admin

from .models import Curso, Alumnoclase, Clase, Calificacion

# Register your models here.
class CursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','status', 'profesor')

class AlumnoclaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'clase', 'user','status')

class ClaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'curso', 'title', 'dni_teacher','date_class','status')

class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'alumnoclase', 'evaluacion', 'note','status','created')

# Register your models here.
admin.site.register(Curso,CursoAdmin)
admin.site.register(Alumnoclase,AlumnoclaseAdmin)
admin.site.register(Clase, ClaseAdmin)
admin.site.register(Calificacion, CalificacionAdmin)