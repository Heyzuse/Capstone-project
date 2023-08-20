from django import forms
from .models import Profile, Exercise, ExerciseType, Workout, ExerciseProgress, WorkoutProgress

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(label='Email:')
    
    height = forms.CharField(
        label='Height (e.g., 5\'4")',
        max_length=5,
        widget=forms.TextInput(attrs={'placeholder': "5'4"})
    )
    
    weight = forms.FloatField(
        label='Weight (in pounds)',
        widget=forms.NumberInput(attrs={'placeholder': "150"})
    )

    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'age', 'email', 'gender', 'height', 'weight', 'birthdate', 'fitness_goal']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Profile.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Email address must be unique.')
        return email

    def clean_height(self):
        height_str = self.cleaned_data.get('height')
        
        try:
            feet, inches = height_str.split("'")
            inches = inches.strip().replace('"', '')
        
            total_inches = int(feet) * 12 + int(inches)
        except ValueError:
            raise forms.ValidationError('Invalid height format. Please use format like 5\'4" or 5\'4.')
        return total_inches

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'type', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].queryset = ExerciseType.objects.filter(name__in=['Upper Body', 'Core', 'Lower Body', 'Full Body'])

class ExerciseProgressForm(forms.ModelForm):
    repetitions = forms.IntegerField(initial=0)
    sets = forms.IntegerField(initial=0)
    weight = forms.FloatField(initial=0.0)

    class Meta:
        model = ExerciseProgress
        fields = ['repetitions', 'sets', 'weight']

class WorkoutProgressForm(forms.ModelForm):
    class Meta:
        model = WorkoutProgress
        fields = ['date', 'notes', 'completed']

class WorkoutForm(forms.ModelForm):

    class Meta:
        model = Workout
        fields = ['name', 'duration']

    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if not duration:
            raise forms.ValidationError("Duration is required.")
        return duration

class ExerciseSelectionForm(forms.Form):
    exercises = forms.ModelMultipleChoiceField(queryset=Exercise.objects.all())
