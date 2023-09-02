from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from .models import User
# Create your views here.



def sign_out(request):
  # remove_user_and_token(request)
  logout(request)
  messages.success(request, "Successfully Logged Out")
  return redirect('home')


def sign_in(request):
  try:
      user = User.objects.get(email='paulcofiis@gmail.com')
      # user.backend = 'authentication.backends.EmailAuthBackend'
      # user.backend.authenticate(username='paulcofiis@gmail.com')
  except User.DoesNotExist:
      print ('USUARIO NO EXISTE EN EL SISTEMA')

  user = authenticate(email='paulcofiis@gmail.com', password='paulcofiis@gmail.com')
  if user is not None:
      login(request,user)
      messages.success(request,"Success: You were successfully logged in.")
  else: 
      return redirect('login')
  return redirect('home')