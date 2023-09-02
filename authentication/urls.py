from django.urls import path

from . import views

authentication_patterns = ([
  # /
  # path('', views.home, name='home'),
  # TEMPORARY
  path('signin', views.sign_in, name='signin'),
  # path('execute_command', views.execute_command, name='execute_command'),
  # path('main', views.main, name='main'),
  # path('callback', views.callback, name='callback'),
  path('signout', views.sign_out, name='signout'),
],'authentication')
