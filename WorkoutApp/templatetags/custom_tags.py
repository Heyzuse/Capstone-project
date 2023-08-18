from django import template

register = template.Library()

@register.filter(name='get_progress')
def get_progress(queryset, exercise):
    return queryset.filter(exercise=exercise).first()
