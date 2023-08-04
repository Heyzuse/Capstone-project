from django import forms
from .models import Profile, Exercise, ExerciseType, Workout

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'birthdate', 'gender', 'height', 'weight']

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'type', 'description']

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'exercises', 'date']
