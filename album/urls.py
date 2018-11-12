from django.urls import path
from . import views
from album.views import (
    PostDetailView,
    CalendarView,
    ImageDetailView,
)
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('test/', views.test, name='test'),

    path('like/<str:operation>/', views.like, name='like'),
    path('crop_upload/', views.crop_upload, name='crop_upload'),
    path('calendar/new/<str:date>/', views.calendar_new, name='calendar_new'),

    path('', login_required(CalendarView.as_view()), name='home'),
    path('post/<int:pk>/', login_required(PostDetailView.as_view()), name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),

    path('image/<int:post_pk>/<int:pk>/', login_required(ImageDetailView.as_view()), name='image_detail'),
    path('image/<int:pk>/edit/', views.image_edit, name='image_edit'),
    path('image/<str:operation>/<int:pk>/remove/', views.image_remove, name='image_remove'),
    path('image_comment/<int:pk>/remove/', views.image_comment_remove, name='image_comment_remove'),

    # notification
    path('notification/<str:operation>/<int:pk>/', views.notification, name='notification'),
    # friend
    path('connect/<str:operation>/<int:pk>/', views.change_friends, name='change_friends'),


    # Calendar album page
    path('calendar_view/', views.calendar_view, name='calendar_view'),

]
