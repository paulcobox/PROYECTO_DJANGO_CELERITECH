from django.urls import path, register_converter
from . import views, converters
from .views import AlumnoclaseListView, CalificacionCreateView,CalificacionListView

# urlpatterns = [
#     # path('', views.pages, name='pages'),
#     path('', PageListView.as_view(), name='pages'),
#     path('<int:pk>/<slug:slug>/', PageDetailView.as_view(), name='page'),
#     path('create/', PageCreateView.as_view(), name='create'),
#     # path('<int:page_id>/<slug:page_slug>/', views.page, name='page'),
# ]
register_converter(converters.EmptyOrSlugConverter, 'emptyorslug')

apps_patterns = ([

    path('calificacionlist', CalificacionListView.as_view(), name='calificacionlist'),
    path('asistencialist', AlumnoclaseListView.as_view(), name='asistencialist'),
    path('asistencia/<int:alumnoclase_id>/<int:asistencia>/<emptyorslug:curso_select>/<emptyorslug:asistencia_select>/<emptyorslug:date>', views.asistencia, name='asistencia'),
    path('create_asistencia/<str:id>/<str:curso_id>', CalificacionCreateView.as_view(), name='create_asistencia'),
],'apps')