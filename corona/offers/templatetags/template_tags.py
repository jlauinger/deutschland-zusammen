from django import template

register = template.Library()


@register.filter
def rounded_distance(distance):
    return int(round(distance.m, -2))
