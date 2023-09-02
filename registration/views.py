# from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django import forms
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import UserCreationFormWithEmail, ProfileForm
from  .models import Profile
from django.views.generic.list import ListView

# Create your views here.
class SignUpView(CreateView):
  form_class = UserCreationFormWithEmail
  template_name = 'registration/signup.html'
  # success_url = reverse_lazy('login')
  
  def get_success_url(self):
    return reverse_lazy('login') + '?register'

  def get_form(self, form_class=None):
    form = super(SignUpView, self).get_form()
    # Modificar en tiempo real
    form.fields['username'].widget = forms.TextInput(
        attrs={'class':'form-control mb-2', 'placeholder':'Nombre de usuario'})
    form.fields['email'].widget = forms.EmailInput(
        attrs={'class':'form-control mb-2', 'placeholder':'Dirección email'})
    return form

@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
  # model = Profile
  # fields = ['avatar','bio','link']
  form_class = ProfileForm
  success_url = reverse_lazy('profile')
  template_name = 'registration/profile_form.html'

  def get_object(self):
    #recuperar el objeto que se va a editar
    profile, created =  Profile.objects.get_or_create(user = self.request.user)
    return profile

class ProfileListView(ListView):# ListView para usar una Lista de instancias de la clase Profile
    model = Profile