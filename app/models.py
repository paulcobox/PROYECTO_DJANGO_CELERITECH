from django.db import models
from authentication.models import User

class Curso(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="Título", max_length=200)
    status = models.IntegerField(verbose_name="Estado", default=1)
    profesor = models.ForeignKey(User, on_delete=models.CASCADE, default=None)


    class Meta:
        verbose_name = "curso"
        verbose_name_plural = "cursos"
        ordering = ['title']

    def __str__(self):
        return self.title

TIPO_EVALUACION_CHOICES = [
    ('P1', 'PRACTICA 1.'),
    ('P2', 'PRACTICA 2.'),
    ('P3', 'PRACTICA 3.'),
    ('P4', 'PRACTICA 4.'),
    ('EP', 'PARCIAL.'),
    ('EF', 'FINAL.'),
    ('ES', 'SUSTITUTORIO.'),
    ('PC', 'PARTICIPACION EN CLASE.'),
]



class Clase(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="Título", max_length=200)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    dni_teacher = models.CharField(verbose_name="DNI del Profesor", max_length=18)
    date_class = models.DateField(verbose_name="Fecha de Clase")
    status = models.IntegerField(verbose_name="Estado", default=1)

    class Meta:
        verbose_name = "clase"
        verbose_name_plural = "clases"
        ordering = ['title']

    def __str__(self):
        return self.title


class Alumnoclase(models.Model):
    id = models.AutoField(primary_key=True)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asistio = models.IntegerField(verbose_name="Asistencia", default=-1)
    status = models.IntegerField(verbose_name="Estado", default=1)


    class Meta:
        verbose_name = "alumnoclase"
        verbose_name_plural = "alumnoclases"
        ordering = ['id']

    def __str__(self):
        return str(self.id)

class Calificacion(models.Model):
    id = models.AutoField(primary_key=True)
    alumnoclase = models.ForeignKey(Alumnoclase, on_delete=models.CASCADE)
    evaluacion = models.CharField(verbose_name="Tipo de Evaluacion", max_length=3, choices=TIPO_EVALUACION_CHOICES)
    note = models.IntegerField(verbose_name="Nota", default=0)
    status = models.IntegerField(verbose_name="Estado", default=1)
    created = models.DateTimeField(verbose_name="Fecha Hora de Creacion", auto_now_add=True)

    class Meta:
        verbose_name = "calificacion"
        verbose_name_plural = "calificaciones"
        ordering = ['evaluacion','note']

    def __str__(self):
        return self.evaluacion + str(self.note)












# class Nota(models.Model):
#     id = models.AutoField(primary_key=True)
#     curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     status = models.IntegerField(verbose_name="Estado", default=1)
#     examen = models.CharField(verbose_name="Tipo de Examen", max_length=3, choices=TIPO_EXAMEN_CHOICES)
#     nota = models.IntegerField(verbose_name="Nota", default=0)
#     created = models.DateTimeField(verbose_name="Fecha Hora de Creacion", auto_now_add=True)

#     class Meta:
#         verbose_name = "nota"
#         verbose_name_plural = "notas"
#         ordering = ['id','curso', 'user']

#     def __str__(self):
#         return str(self.id)

# class Asistencia(models.Model):
#     id = models.AutoField(primary_key=True)
#     curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created = models.DateField(verbose_name="Fecha de Registro", auto_now_add=True)
#     attended = models.IntegerField(verbose_name="Asistio", default=0)

#     class Meta:
#         verbose_name = "asistencia"
#         verbose_name_plural = "asistencias"
#         ordering = ['id','curso', 'user']

#     def __str__(self):
#         return str(self.id)