# Generated by Django 3.0.4 on 2020-03-23 14:51

from django.db import migrations
from django.db.migrations import RunPython


def fill_display_name(apps, schema_editor):
    ProviderProfile = apps.get_model('offers', 'ProviderProfile')

    for profile in ProviderProfile.objects.all():
        profile.display_name = get_display_name(profile)
        profile.save()


def get_display_name(profile):
    if profile.name_visibility == 'FULL':
        return profile.user.first_name + " " + profile.user.last_name
    elif profile.name_visibility == 'FIRST_NAME':
        return profile.user.first_name
    else:
        return ""



def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0009_providerprofile_display_name'),
    ]

    operations = [
        RunPython(fill_display_name, reverse)
    ]