from django.urls import path
from . import views
from .views import PerfilListView, PerfilDetailView, PerfilCreateView, PerfilUpdateView,PerfilActivateUpdate,PerfilDesactivateUpdate,PerfilDeleteView, UsuarioActivateUpdate, UsuarioDeleteView, UsuarioDesactivateUpdate, UsuarioListView,UsuarioDetailView,UsuarioUpdateView,UsuarioCreateView

# urlpatterns = [
#     # path('', views.pages, name='pages'),
#     path('', PageListView.as_view(), name='pages'),
#     path('<int:pk>/<slug:slug>/', PageDetailView.as_view(), name='page'),
#     path('create/', PageCreateView.as_view(), name='create'),
#     # path('<int:page_id>/<slug:page_slug>/', views.page, name='page'),
# ]


seguridad_patterns = ([
    path('perfileslist', PerfilListView.as_view(), name='perfileslist'),
    # path('perfilview/<int:pk>', PerfilDetailView.as_view(), name='perfilview'), #slug = slug field
    path('perfilview/<int:pk>/<int:pagina>', PerfilDetailView.as_view(), name='perfilview'), #slug = slug field
    path('perfilcreate/', PerfilCreateView.as_view(), name='perfilcreate'),
    path('perfilupdate/<int:pk>/<int:pagina>', PerfilUpdateView.as_view(), name='perfilupdate'),
    path('perfildelete/', PerfilDeleteView.as_view(), name='perfildelete'),
    path('perfil_activate/<int:pk>', PerfilActivateUpdate.as_view(), name='perfil_activate'),
    path('perfil_desactivate/<int:pk>', PerfilDesactivateUpdate.as_view(), name='perfil_desactivate'),
    
    path('usuarioupdate/<int:pk>/<int:pagina>', UsuarioUpdateView.as_view(), name='usuarioupdate'),
    path('usuarioview/<int:pk>/<int:pagina>', UsuarioDetailView.as_view(), name='usuarioview'), #slug = slug field
    path('usuarioslist', UsuarioListView.as_view(), name='usuarioslist'),
    path('usuariodelete/', UsuarioDeleteView.as_view(), name='usuariodelete'),
    path('usuariocreate/', UsuarioCreateView.as_view(), name='usuariocreate'),
    path('usuario_activate/<int:pk>', UsuarioActivateUpdate.as_view(), name='usuario_activate'),
    path('usuario_desactivate/<int:pk>', UsuarioDesactivateUpdate.as_view(), name='usuario_desactivate'),
],'seguridad')