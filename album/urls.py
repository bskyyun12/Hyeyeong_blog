from django.urls import path
from . import views
from album.views import (
    PostDetailView,
    CalendarView,
)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(CalendarView.as_view()), name='home'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/', login_required(PostDetailView.as_view()), name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),

    # friend
    path('connect/<str:operation>/<int:pk>/', views.change_friends, name='change_friends'),

    path('image/<int:pk>/remove/', views.image_remove, name='image_remove'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    # path('entry/<int:pk>', views.details, name='details'),
    # path('entry/add', views.add, name='add'),
    # path('entry/delete/<int:pk>', views.delete, name='delete'),


]
