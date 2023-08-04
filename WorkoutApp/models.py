from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')))
    height = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    weight = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    birthdate = models.DateField(null=True, blank=True)
    fitness_goal = models.CharField(max_length=200)
    
class ExerciseType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Exercise(models.Model):
    type = models.ForeignKey(ExerciseType, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    repetitions = models.IntegerField()
    sets = models.IntegerField()

class Workout(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField()
    exercises = models.ManyToManyField(Exercise)
    duration = models.IntegerField(help_text="Duration in minutes")
