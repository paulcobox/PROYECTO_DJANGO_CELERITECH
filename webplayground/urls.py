"""webplayground URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pages.urls import pages_patterns
from app.urls import apps_patterns
from seguridad.urls import seguridad_patterns
from authentication.urls import authentication_patterns
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('pages/', include(pages_patterns)),
    path('apps/', include(apps_patterns)),
    path('seguridad/', include(seguridad_patterns)),
    path('authentication/', include(authentication_patterns)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.urls')),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)