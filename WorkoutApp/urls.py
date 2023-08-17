from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import UserRegisterView, UserUpdateView, UserDeleteView, DeleteExerciseView, PublicWorkoutListView

urlpatterns = [

    # Profile
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/<int:pk>/', views.UserDetailView.as_view(), name='profile'),
    path('profile/update/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/delete/<int:pk>/', UserDeleteView.as_view(), name='delete-profile'),
    path('', views.home, name='home'),

    # Workouts
    path('workout/new/', views.WorkoutCreateView.as_view(), name='workout_create'),
    path('workout/<int:pk>/', views.WorkoutDetailView.as_view(), name='workout_detail'),
    path('workout/<int:pk>/update/', views.WorkoutUpdateView.as_view(), name='workout_update'),
    path('workout/<int:pk>/delete/', views.WorkoutDeleteView.as_view(), name='workout_delete'),
    path('workout/<int:workout_id>/add_exercises/', views.add_exercises_to_workout, name='add_exercises_to_workout'),
    path('profile/<int:profile_id>/workouts/', views.WorkoutListView.as_view(), name='workout_list'),
    path('browse_workouts/', PublicWorkoutListView.as_view(), name='browse_workouts'),
    path('workout/edit/<int:pk>/', views.EditWorkoutView.as_view(), name='edit_workout'),
    path('workout/<int:pk>/complete/', views.complete_workout, name='complete_workout'),

    # Individual Exercises
    path('profile/<int:profile_id>/exercises/', views.exercise_list, name='exercise_list'),
    path('exercise/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    path('profile/<int:profile_id>/exercise/new/', views.exercise_create, name='exercise_create'),
    path('exercise/<int:exercise_id>/edit/', views.exercise_update, name='exercise_update'),
    path('exercise/delete/<int:pk>/', DeleteExerciseView.as_view(), name='delete_exercise'),

    # Exercise progress
    path('workout/<int:workout_id>/exercise/<int:exercise_id>/progress/', views.exercise_progress_create, name='exercise_progress_create'),
    path('workout/<int:pk>/summary/', views.workout_summary, name='workout_summary'),
]
