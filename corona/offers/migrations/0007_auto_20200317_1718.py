# Generated by Django 3.0.4 on 2020-03-17 17:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0006_auto_20200317_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='start_time',
        ),
        migrations.AddField(
            model_name='offer',
            name='afternoon',
            field=models.BooleanField(default=False, verbose_name='Nachmittags'),
        ),
        migrations.AddField(
            model_name='offer',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Datum'),
        ),
        migrations.AddField(
            model_name='offer',
            name='evening',
            field=models.BooleanField(default=False, verbose_name='Abends'),
        ),
        migrations.AddField(
            model_name='offer',
            name='morning',
            field=models.BooleanField(default=False, verbose_name='Morgens'),
        ),
        migrations.AddField(
            model_name='offer',
            name='noon',
            field=models.BooleanField(default=False, verbose_name='Mittags'),
        ),
    ]