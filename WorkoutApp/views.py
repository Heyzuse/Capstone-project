from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Profile, Exercise, ExerciseType, Workout, ExerciseProgress, ProfileHistory
from .forms import ProfileForm, ExerciseForm, WorkoutForm, ExerciseProgressForm, ExerciseSelectionForm, WorkoutProgressForm

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

    def form_valid(self, form):
        response = super().form_valid(form)
        ProfileHistory.objects.create(profile=self.object, height=self.object.height, weight=self.object.weight)
        return response

class UserDetailView(DetailView):
    model = User
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context

class UserUpdateView(UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'registration/profile_update.html'
    success_url = reverse_lazy('profile')

class UserDeleteView(DeleteView):
    model = User
    success_url = '/'
    template_name = 'registration/confirm_delete.html'

class WorkoutCreateView(CreateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'workout_create.html'

    def form_valid(self, form):
        form.instance.profile = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('workout_list', args=[self.request.user.profile.id])

class WorkoutDetailView(DetailView):
    model = Workout
    template_name = 'workout_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workout = get_object_or_404(Workout, pk=self.kwargs['pk'])
        
        # Fetching exercise progress for this workout and user
        exercise_progresses = ExerciseProgress.objects.filter(workout=workout, profile=self.request.user.profile)
        
        context['exercise_progresses'] = exercise_progresses
        return context

class WorkoutUpdateView(UpdateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'workout_update.html'
    success_url = reverse_lazy('home')

class WorkoutDeleteView(DeleteView):
    model = Workout
    template_name = 'workout_confirm_delete.html'
    success_url = reverse_lazy('home')
    
    def get_success_url(self):
        return reverse('workout_list', args=[self.request.user.profile.id])

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

class PublicWorkoutListView(ListView):
    model = Workout
    template_name = 'public_workout_list.html'

    def get_queryset(self):
        return Workout.objects.filter(public=True)

def home(request):
    profiles = Profile.objects.all()
    if request.user.is_authenticated:
        return render(request, 'home.html', {'profiles': profiles})
    else:
        return redirect('login')

def profile(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
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
        form = ExerciseSelectionForm(request.POST)
        if form.is_valid():
            exercises = form.cleaned_data['exercises']
            workout.exercises.add(*exercises)
            return HttpResponseRedirect(reverse('workout_detail', args=(workout.id,)))
    else:
        form = ExerciseSelectionForm()
    return render(request, 'add_exercises_to_workout.html', {'form': form, 'workout': workout, 'some_profile_id': request.user.profile.id, 'current_workout_id': workout_id})

def exercise_list(request, profile_id):
    exercises = Exercise.objects.all()
    return render(request, 'exercise_list.html', {'exercises': exercises})

def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    progress = ExerciseProgress.objects.filter(exercise=exercise)
    return render(request, 'exercise_detail.html', {'exercise': exercise, 'progress': progress})

def exercise_create(request, profile_id, workout_id=None):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            new_exercise = form.save(commit=False)
            new_exercise.profile = Profile.objects.get(pk=profile_id)
            new_exercise.save()

            if workout_id:
                return HttpResponseRedirect(reverse('add_exercises_to_workout', args=[workout_id]))
            else:
                return HttpResponseRedirect(reverse('exercise_list', args=(request.user.profile.id,))) 
    else:
        form = ExerciseForm()

    return render(request, 'exercise_create.html', {'form': form})

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

@login_required
def exercise_progress_create(request, workout_id, exercise_id):
    workout = get_object_or_404(Workout, pk=workout_id)
    exercises_in_workout = workout.exercises.all()

    current_exercise = get_object_or_404(Exercise, pk=exercise_id)

    if request.method == 'POST':
        form = ExerciseProgressForm(request.POST, exercises=exercises_in_workout)
        
        if form.is_valid():
            new_progress = form.save(commit=False)
            new_progress.workout = workout
            new_progress.exercise = current_exercise
            new_progress.profile = request.user.profile  # Set the profile for the ExerciseProgress instance
            new_progress.save()

            exercises_in_workout_list = list(exercises_in_workout)
            current_exercise_index = exercises_in_workout_list.index(current_exercise)

            try:
                next_exercise = exercises_in_workout_list[current_exercise_index + 1]
                return redirect('exercise_progress_create', workout_id=workout.id, exercise_id=next_exercise.id)
            except IndexError:
                return redirect('workout_summary', workout.id)
    else:
        form = ExerciseProgressForm(exercises=exercises_in_workout)

    return render(request, 'exercise_progress_create.html', {'form': form, 'exercise': current_exercise, 'workout': workout})

def complete_workout(request, pk):
    workout = get_object_or_404(Workout, pk=pk)

    if request.user.profile == workout.profile:
        workout.completed = True
        workout.save()
        messages.success(request, "Workout marked as complete!")
    else:
        messages.error(request, "You don't have permission to complete this workout.")

    return redirect('workout_summary')

from django.shortcuts import render

def track_workout_progress(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id)
    if request.method == "POST":
        form = WorkoutProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.workout = workout
            progress.user = request.user
            progress.save()
            return HttpResponseRedirect(reverse('workout_detail', args=(workout.id,)))
    else:
        form = WorkoutProgressForm()
    return render(request, 'track_workout_progress.html', {'form': form, 'workout': workout})


def workout_summary(request, pk):
    workout = get_object_or_404(Workout, pk=pk)

    if request.user.profile != workout.profile:
        messages.error(request, "You don't have permission to view this workout.")
        return redirect('home')  # Redirect to a fallback view or page

    context = {
        'workout': workout
    }
    return render(request, 'WorkoutApp/workout_summary.html', context)
