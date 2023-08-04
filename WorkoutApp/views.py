from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Profile, Exercise, ExerciseType
from .forms import ProfileForm, ExerciseForm, WorkoutForm


class UserRegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = '/'

    def form_valid(self, form):
        messages.success(self.request, 'Form submission successful')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Form submission unsuccessful')
        return super().form_invalid(form)
    
class UserDetailView(DetailView):
    model = User
    template_name = 'registration/profile.html'

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

def profile(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', profile_id=profile.id)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form, 'profile': profile})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            form = AuthenticationForm()
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

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
        form = ExerciseForm(request.POST)
        if form.is_valid():
            new_exercise = form.save(commit=False)
            new_exercise.profile = profile
            new_exercise.save()
            return HttpResponseRedirect(reverse('exercise_list', args=(profile.id,)))
    else:
        form = ExerciseForm()

    return render(request, 'exercise_create.html', {'form': form, 'profile': profile})

def exercise_update(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('exercise_detail', args=(exercise.id,)))
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, 'exercise_update.html', {'form': form})

def exercise_delete(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    profile_id = exercise.profile.id
    if request.method == 'POST':
        exercise.delete()
        return HttpResponseRedirect(reverse('exercise_list', args=(profile_id,)))
    else:
        return render(request, 'exercise_delete.html', {'exercise': exercise})
