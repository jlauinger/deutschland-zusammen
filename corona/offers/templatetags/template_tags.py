from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from offers.models import Website

register = template.Library()


@register.filter
def get_zoom(radius):
    if radius == 1000:
        return 14
    elif radius == 2000:
        return 13
    elif radius == 3000:
        return 13
    elif radius == 4000:
        return 12
    elif radius == 5000:
        return 12
    elif radius == 10000:
        return 11
    elif radius == 20000:
        return 10
    elif radius == 50000:
        return 9
    else:
        return 13


@register.simple_tag
def cms_page(name):
    website = Website.objects.filter(name=name, language=get_language()).first()
    return mark_safe(website.content) if website else ""
