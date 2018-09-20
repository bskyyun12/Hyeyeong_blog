from django.urls import path
from . import views
from album.views import (
    PostDetailView
)
from django_filters.views import FilterView
from .filters import CalendarFilter

urlpatterns = [
    path('', FilterView.as_view(filterset_class = CalendarFilter, template_name='album/home.html'), name='home'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
    # path('search/', views.search, name='search'),

    path('comment/<int:pk>)/remove/', views.comment_remove, name='comment_remove'),
    # path('entry/<int:pk>', views.details, name='details'),
    # path('entry/add', views.add, name='add'),
    # path('entry/delete/<int:pk>', views.delete, name='delete'),
]
