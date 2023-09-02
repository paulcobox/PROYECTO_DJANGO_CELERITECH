from django.urls import path
from .views import SignUpView,ProfileUpdate, ProfileListView


# urlpatterns = [
#     # path('', views.pages, name='pages'),
#     path('', PageListView.as_view(), name='pages'),
#     path('<int:pk>/<slug:slug>/', PageDetailView.as_view(), name='page'),
#     path('create/', PageCreateView.as_view(), name='create'),
#     # path('<int:page_id>/<slug:page_slug>/', views.page, name='page'),
# ]


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileUpdate.as_view(), name='profile'),
    path('alumnos/', ProfileListView.as_view(), name='alumnos'),
]