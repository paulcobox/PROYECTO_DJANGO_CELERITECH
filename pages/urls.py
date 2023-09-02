from django.urls import path
from . import views
from .views import PageListView, PageDetailView, PageCreateView, PageUpdateView, PageDeleteView

# urlpatterns = [
#     # path('', views.pages, name='pages'),
#     path('', PageListView.as_view(), name='pages'),
#     path('<int:pk>/<slug:slug>/', PageDetailView.as_view(), name='page'),
#     path('create/', PageCreateView.as_view(), name='create'),
#     # path('<int:page_id>/<slug:page_slug>/', views.page, name='page'),
# ]


pages_patterns = ([
    path('', PageListView.as_view(), name='pages'),
    path('<int:pk>/<slug:slug>/', PageDetailView.as_view(), name='page'),
    path('create/', PageCreateView.as_view(), name='create'),
    path('update/<int:pk>/', PageUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', PageDeleteView.as_view(), name='delete'),
],'pages')