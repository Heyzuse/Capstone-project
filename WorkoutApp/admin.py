from django.contrib import admin
from .models import Exercise, Profile, Workout, ExerciseType

admin.site.register(Exercise)
admin.site.register(Profile)
admin.site.register(Workout)
admin.site.register(ExerciseType)
