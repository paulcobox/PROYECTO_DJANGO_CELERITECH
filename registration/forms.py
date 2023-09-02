from django import forms
from django.contrib.auth.forms import UserCreationForm
from authentication.models import User
from .models import Profile
# from .models import Profile

class UserCreationFormWithEmail(forms.ModelForm):
    email = forms.EmailField(required=True, help_text="Requerido. 254 carácteres como máximo y debe ser válido.")

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data.get("email")#recupera el email que estamos enviando al formaulario
        if User.objects.filter(email=email).exists(): #valida si existe algun usuario con ese campo
            raise forms.ValidationError("El email ya está registrado, prueba con otro.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get("username")#recupera el email que estamos enviando al formaulario
        if User.objects.filter(username=username).exists(): #valida si existe algun usuario con ese campo
            raise forms.ValidationError("El username ya está registrado, prueba con otro.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

# class UserCreationFormWithEmail(UserCreationForm):
#     email = forms.EmailField(required=True, help_text="Requerido. 254 carácteres como máximo y debe ser válido.")

#     class Meta:
#         model = User
#         fields = ("username", "email", "password1", "password2")

#     def clean_email(self):
#         email = self.cleaned_data.get("email")#recupera el email que estamos enviando al formaulario
#         if User.objects.filter(email=email).exists(): #valida si existe algun usuario con ese campo
#             raise forms.ValidationError("El email ya está registrado, prueba con otro.")
#         return email
    
#     def clean_username(self):
#         username = self.cleaned_data.get("username")#recupera el email que estamos enviando al formaulario
#         if User.objects.filter(username=username).exists(): #valida si existe algun usuario con ese campo
#             raise forms.ValidationError("El username ya está registrado, prueba con otro.")
#         return username


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'link']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class':'form-control-file mt-3'}),
            'bio': forms.Textarea(attrs={'class':'form-control mt-3', 'rows':3, 'placeholder':'Biografía'}),
            'link': forms.URLInput(attrs={'class':'form-control mt-3', 'placeholder':'Enlace'}),
        }