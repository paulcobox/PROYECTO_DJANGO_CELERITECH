from django import forms
from .models import Calificacion
from authentication.models import User
from datetime import datetime

class CalificacionForm(forms.ModelForm):

  class Meta:
    model = Calificacion
    fields = ['alumnoclase','evaluacion', 'note']
    widgets = {
        'evaluacion': forms.Select(attrs={'class':'form-control'}),
        'nota': forms.NumberInput(attrs={'class':'form-control', 'required':True}),
    }