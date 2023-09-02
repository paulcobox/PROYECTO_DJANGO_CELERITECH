from django import forms
from .models import Perfil
from authentication.models import User
from django.db.models import Q
from django.contrib import messages

class PerfilForm(forms.ModelForm):

  class Meta:
    model = Perfil
    fields = ['nombre', 'estado', 'descripcion','is_admin', ]

    widgets = {
        'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre', "pattern":"[A-Za-z0-9\s]+" }),
        'estado': forms.Select(attrs={'class':'form-control'}),
        'is_admin': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        'descripcion': forms.Textarea(attrs={'class':'form-control','placeholder':'Descripcion', 'rows':'2'}),
    }
    
    labels = {
        'nombre': "Nombre de Perfil",
        'estado': "Estado",
        'is_admin': "Admin",
        'descripcion': "Descripcion"
    }

  def clean_nombre(self):
    nombre = self.cleaned_data.get("nombre")
    if self.instance.id:
      if Perfil.objects.filter(nombre=nombre).filter( Q(estado='001') | Q(estado='002')).exclude(id=self.instance.id).exists():
        raise forms.ValidationError('El nombre de perfil ya está registrado, prueba con otro.')
    else:
      if Perfil.objects.filter(nombre=nombre).filter( Q(estado='001') | Q(estado='002')).exists():
          raise forms.ValidationError('El nombre de perfil ya está registrado, prueba con otro.')
    return nombre

  def clean(self):
      cleaned_data = super(PerfilForm, self).clean()
      is_admin = cleaned_data.get('is_admin')
      estado = cleaned_data.get('estado')
      print('a',is_admin)
      print('a',estado)
      if self.instance.id:
        print('a')
        if not Perfil.objects.filter(is_admin=True, estado='001').exclude(id=self.instance.id).exists():
            print('b')
            if not is_admin or not  estado == '001':
              print('c')
              msg = "No puede desactivar o dejar de ser admin, el unico perfil 'Admin' del sistema."
              self.add_error('estado', msg)


class UserCreationFormWithEmail(forms.ModelForm):
    # email = forms.EmailField(required=True, help_text="Requerido. 254 carácteres como máximo y debe ser válido.")

    class Meta:
        model = User
        fields = ["email", "oficina", "region", "estado", "perfil"]

        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'oficina': forms.Select(attrs={'class':'form-control'}),
            'region': forms.Select(attrs={'class':'form-control'}),
            'estado': forms.Select(attrs={'class':'form-control'}),
            'perfil': forms.Select(attrs={'class':'form-control','required':True}),
        }
        
        labels = {
            'Email':'', 'Oficina':'', 'Region':'',  'Estado':'', 'Perfil':''
        }


    def clean_email(self):
      email = self.cleaned_data.get("email")#recupera el email que estamos enviando al formaulario
      if self.instance.id:
        if User.objects.filter(email=email).filter( Q(estado='001') | Q(estado='002')).exclude(id=self.instance.id).exists():
          raise forms.ValidationError('El correo ya está registrado, prueba con otro.')
      else:
        if User.objects.filter(email=email).filter( Q(estado='001') | Q(estado='002')).exists(): #valida si existe algun usuario con ese campo
            raise forms.ValidationError('El correo ya está registrado, prueba con otro.')
      return email

    def clean(self):
        cleaned_data = super(UserCreationFormWithEmail, self).clean()
        perfil = cleaned_data.get('perfil')
        print(perfil.is_admin)
        estado = cleaned_data.get('estado')
        if self.instance.id:
          if not User.objects.filter(is_superuser=True, estado='001').exclude(id=self.instance.id).exists():
              if not perfil.is_admin or not  estado == '001':
                msg = "No puede desactivar o dejar de ser admin, el unico usuario 'Admin' del sistema."
                self.add_error('perfil', msg)


    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.set_password(user.email)
        user.is_staff = True
        if user.perfil:
          user.is_superuser = user.perfil.is_admin
        if commit:
            user.save()
        return user


    # def clean_email(self):
    #     email = self.cleaned_data.get("email")#recupera el email que estamos enviando al formaulario
    #     if User.objects.filter(email=email).exists(): #valida si existe algun usuario con ese campo
    #         raise forms.ValidationError("El email ya está registrado, prueba con otro.")
    #     return email
    
    # def clean_username(self):
    #     username = self.cleaned_data.get("username")#recupera el email que estamos enviando al formaulario
    #     if User.objects.filter(username=username).exists(): #valida si existe algun usuario con ese campo
    #         raise forms.ValidationError("El username ya está registrado, prueba con otro.")
    #     return username

# class UsuarioForm(forms.ModelForm):

#   pass

  # class Meta:
  #   model = User
  #   fields = ['nombres', 'apellidos', 'correo','estado','perfil']

  #   widgets = {
  #       'nombres': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}),
  #       'apellidos': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Apellido'}),
  #       'correo': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
  #       'estado': forms.Select(attrs={'class':'form-control'}),
  #       'perfil': forms.Select(attrs={'class':'form-control'}),
  #   }
    
  #   labels = {
  #       'Nombre':'', 'Apellido':'', 'Correo':'',  'Estado':'', 'Perfil':''
  #   }

  # def clean_correo(self):
  #   correo = self.cleaned_data.get("correo")#recupera el email que estamos enviando al formaulario
  #   if self.instance.id:
  #     if User.objects.filter(correo=correo).filter( Q(estado='001') | Q(estado='002')).exclude(id=self.instance.id).exists():
  #       raise forms.ValidationError('El correo ya está registrado, prueba con otro.')
  #   else:
  #     if User.objects.filter(correo=correo).filter( Q(estado='001') | Q(estado='002')).exists(): #valida si existe algun usuario con ese campo
  #         raise forms.ValidationError('El correo ya está registrado, prueba con otro.')
  #   return correo