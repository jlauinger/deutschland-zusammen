# Generated by Django 3.0.4 on 2020-03-23 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0011_remove_providerprofile_name_visibility'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='providerprofile',
            name='address',
        ),
    ]
