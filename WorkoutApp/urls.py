"""
URL configuration for workout_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import UserRegisterView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/<int:pk>/', views.UserDetailView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/delete/<int:pk>/', UserDeleteView.as_view(), name='delete-profile'),
    path('', views.home, name='home'),
    path('profile/<int:profile_id>/exercises/', views.exercise_list, name='exercise_list'),
    path('exercise/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    path('profile/<int:profile_id>/exercise/new/', views.exercise_create, name='exercise_create'),
    path('exercise/<int:exercise_id>/edit/', views.exercise_update, name='exercise_update'),
    path('exercise/<int:exercise_id>/delete/', views.exercise_delete, name='exercise_delete'),
]


