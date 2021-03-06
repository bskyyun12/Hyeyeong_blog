from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/<int:pk>/', views.view_profile, name='view_profile_with_pk'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),

    path('baby_profile/', views.baby_profile, name='baby_profile'),
    path('edit_baby_profile/edit/', views.edit_baby_profile, name='edit_baby_profile'),
]
