from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(default=18)
    email = models.EmailField((""), max_length=254)
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')))
    height = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    weight = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    birthdate = models.DateField(null=True, blank=True)
    fitness_goal = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username
    
class ProfileHistory(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_recorded = models.DateField(auto_now_add=True)
    height = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    weight = models.DecimalField(null=True, max_digits=5, decimal_places=2)

class ExerciseType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(ExerciseType, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name

class Workout(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    exercises = models.ManyToManyField(Exercise)
    duration = models.IntegerField(help_text="Duration in minutes")
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

class ExerciseProgress(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    repetitions = models.IntegerField(default=0)
    sets = models.IntegerField(default=0)
    weight = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="Weight in kilograms or pounds.")

class WorkoutProgress(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    notes = models.TextField(blank=True)
    completed = models.BooleanField(default=False) 

class DailyTracking(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    activity = models.CharField(max_length=200, help_text="E.g., walking, running, yoga, etc.")
    duration = models.IntegerField(help_text="Duration in minutes")
    notes = models.TextField(blank=True)

class Achievement(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    date_achieved = models.DateField(auto_now_add=True)

class NutritionTracking(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    food_item = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=5, decimal_places=2, help_text="E.g., grams, ounces, cups, etc.")
    calories = models.IntegerField(help_text="Calories contained in the food item.")
    notes = models.TextField(blank=True)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()