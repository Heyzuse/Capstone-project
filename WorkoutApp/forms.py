from django import forms
from .models import Profile, Exercise, ExerciseType, Workout, ExerciseProgress

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'gender', 'height', 'weight', 'birthdate', 'fitness_goal']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'age', 'email', 'gender', 'height', 'weight', 'birthdate', 'fitness_goal']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Profile.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Email address must be unique.')
        return email

class ExerciseForm(forms.ModelForm):
    TYPE_CHOICES = [
        ('Upper Body', 'Upper Body'),
        ('Core', 'Core'),
        ('Lower Body', 'Lower Body'),
        ('Full Body', 'Full Body'),
    ]

    type = forms.ChoiceField(choices=TYPE_CHOICES)

    class Meta:
        model = Exercise
        fields = ['name', 'type', 'description']

class ExerciseProgressForm(forms.ModelForm):
    class Meta:
        model = ExerciseProgress
        fields = ['exercise', 'repetitions', 'sets', 'weight']  

class WorkoutForm(forms.ModelForm):
    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Workout
        fields = ['name', 'duration', 'exercises', 'profile']

    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('profile', None)
        super(WorkoutForm, self).__init__(*args, **kwargs)
        if profile:
            self.fields['exercises'].queryset = Exercise.objects.filter(profile=profile)
            
    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if not duration:
            raise forms.ValidationError("Duration is required.")
        return duration

class ExerciseSelectionForm(forms.Form):
    exercises = forms.ModelMultipleChoiceField(queryset=Exercise.objects.all())
