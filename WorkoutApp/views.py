from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Profile, Exercise, ExerciseType

class UserRegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = '/'

class UserUpdateView(UpdateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/profile.html'
    success_url = '/profile/'

class UserDeleteView(DeleteView):
    model = User
    success_url = '/'
    template_name = 'registration/confirm_delete.html'

def home(request):
    profiles = Profile.objects.all()
    return render(request, 'home.html', {'profiles': profiles})

def exercise_list(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    exercises = Exercise.objects.filter(profile=profile)
    return render(request, 'exercise_list.html', {'profile': profile, 'exercises': exercises})

def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    return render(request, 'exercise_detail.html', {'exercise': exercise})

def exercise_create(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    if request.method == 'POST':
        # Assuming your Exercise model has fields 'name', 'type', and 'description'.
        new_exercise = Exercise(profile=profile, name=request.POST['name'], type=request.POST['type'], description=request.POST['description'])
        new_exercise.save()
        return HttpResponseRedirect(reverse('exercise_list', args=(profile.id,)))
    else:
        return render(request, 'exercise_create.html', {'profile': profile})

def exercise_update(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    if request.method == 'POST':
        # Update the exercise fields based on the form data.
        exercise.name = request.POST['name']
        exercise.type = request.POST['type']
        exercise.description = request.POST['description']
        exercise.save()
        return HttpResponseRedirect(reverse('exercise_detail', args=(exercise.id,)))
    else:
        return render(request, 'exercise_update.html', {'exercise': exercise})

def exercise_delete(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    if request.method == 'POST':
        exercise.delete()
        return HttpResponseRedirect(reverse('exercise_list', args=(exercise.profile.id,)))
    else:
        return render(request, 'exercise_delete.html', {'exercise': exercise})