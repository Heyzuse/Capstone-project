# Generated by Django 4.2.3 on 2023-08-05 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkoutApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.PositiveIntegerField(default=18),
        ),
    ]
