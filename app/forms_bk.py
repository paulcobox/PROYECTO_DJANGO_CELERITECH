# from django import forms
# from .models import Nota, Curso
# from django.contrib.auth.models import User
# from datetime import datetime

# class NotaForm(forms.ModelForm):

#   class Meta:
#     model = Nota
#     fields = ['curso', 'user', 'nota','examen']
#     widgets = {
#         'curso': forms.Select(attrs={'class':'form-control'}),
#         'user': forms.Select(attrs={'class':'form-control'}),
#         'examen': forms.Select(attrs={'class':'form-control'}),
#         'nota': forms.NumberInput(attrs={'class':'form-control', 'required':True}),
#     }


#   def clean(self):
#       cleaned_data = super(NotaForm, self).clean()
#       curso = cleaned_data.get('curso')
#       user = cleaned_data.get('user')
#       examen = cleaned_data.get('examen')
#       nota = Nota.objects.filter(user=user,curso=curso)
#       nota_lst = list(nota)

#       if len(nota_lst) > 0:
#         nota_lst_1 = nota_lst[0]
#         fecha_dia = str(datetime.now().year)+str(datetime.now().month)+str(datetime.now().day)
#         fecha_hora = str(nota_lst_1.created.year)+str(nota_lst_1.created.month)+str(nota_lst_1.created.day)
#         if(fecha_dia == fecha_hora):
#             raise forms.ValidationError(
#                 f'''El dia de Hoy ya ingreso una nota para el alumno {user} en el curso {curso} seleccionado. Solo se permite un ingreso por dia
#                 '''
#             )
#       for nota_ in nota_lst:
#         if nota_.examen == examen:
#             raise forms.ValidationError(
#                 f'''Ya existe una nota para el tipo de examen {examen} para el alumno {user} en el curso {curso} seleccionado.
#                 '''
#             )

# class NotaFormUpdate(forms.ModelForm):

#   class Meta:
#     model = Nota
#     fields = ['curso', 'user', 'nota','examen']
#     widgets = {
#         'curso': forms.Select(attrs={'class':'form-control'}),
#         'user': forms.Select(attrs={'class':'form-control'}),
#         'examen': forms.Select(attrs={'class':'form-control'}),
#         'nota': forms.NumberInput(attrs={'class':'form-control', 'required':True}),
#     }

