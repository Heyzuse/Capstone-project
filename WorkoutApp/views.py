from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.views.generic.edit import DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Profile, Exercise, ExerciseType, Workout
from .forms import ProfileForm, ExerciseForm, WorkoutForm


class UserRegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=username, password=raw_password)
        if user is not None:
            login(self.request, user)
            Profile.objects.get_or_create(user=user)  # Get or Create an associated Profile
            messages.success(self.request, 'Registration successful')
        else:
            messages.error(self.request, 'Registration unsuccessful. Please try again.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Form submission unsuccessful')
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('profile_update', kwargs={'pk': self.object.profile.pk})

class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile_update.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None): 
        return self.request.user.profile
    
class UserDetailView(DetailView):
    model = User
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.object)  # get the Profile of the User
        return context

class UserUpdateView(UpdateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/profile_update.html'
    success_url = '/profile/'

class UserDeleteView(DeleteView):
    model = User
    success_url = '/'
    template_name = 'registration/confirm_delete.html'

class WorkoutCreateView(CreateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'workout_create.html'
    success_url = reverse_lazy('workout_list')

    def form_valid(self, form):
        form.instance.profile = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

class WorkoutDetailView(DetailView):
    model = Workout
    template_name = 'workout_detail.html'


class WorkoutUpdateView(UpdateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'workout_update.html'
    success_url = reverse_lazy('home')


class WorkoutDeleteView(DeleteView):
    model = Workout
    template_name = 'workout_confirm_delete.html'
    success_url = reverse_lazy('home')

class WorkoutListView(ListView):
    model = Workout
    template_name = 'workout_list.html'

    def get_queryset(self):
        return Workout.objects.filter(profile=self.request.user.profile)

class EditWorkoutView(UpdateView):
    model = Workout
    template_name = 'edit_workout.html'
    form_class = WorkoutForm

    def get_form_kwargs(self):
        kwargs = super(EditWorkoutView, self).get_form_kwargs()
        kwargs['profile'] = self.object.profile
        return kwargs
    
    def get_success_url(self):
        profile_id = self.object.profile.id
        return reverse('workout_list', args=[profile_id])
    
class DeleteExerciseView(DeleteView):
    model = Exercise
    template_name = 'exercise_confirm_delete.html'
    
    def get_success_url(self):
        profile_id = self.object.profile.id
        return reverse('exercise_list', args=[profile_id])

def home(request):
    profiles = Profile.objects.all()
    if request.user.is_authenticated:
        return render(request, 'home.html', {'profiles': profiles})
    else:
        return redirect('login')

def profile(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    print(profile.id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()
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
            form = ProfileForm()
    else:
        form = ProfileForm()
    return render(request, 'login.html', {'form': form})

def add_exercises_to_workout(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id)
    if request.method == 'POST':
        form = exercise_list(request.POST)
        if form.is_valid():
            exercises = form.cleaned_data['exercises']
            workout.exercises.add(*exercises)
            return HttpResponseRedirect(reverse('workout_detail', args=(workout.id,)))
    else:
        form = exercise_list()
    return render(request, 'add_exercises_to_workout.html', {'form': form, 'workout': workout})


# Maybe these
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
