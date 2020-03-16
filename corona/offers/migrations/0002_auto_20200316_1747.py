# Generated by Django 3.0.4 on 2020-03-16 17:47

from django.db import migrations, models
import offers.models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='offer',
            options={'verbose_name': 'Hilfsangebot', 'verbose_name_plural': 'Hilfsangebote'},
        ),
        migrations.RemoveField(
            model_name='offer',
            name='title',
        ),
        migrations.AddField(
            model_name='offer',
            name='mobility',
            field=models.TextField(choices=[('NA', 'keine Angabe'), ('FOOT', 'zu Fuß / ÖPNV'), ('BIKE', 'Fahrrad'), ('MOTOR_SCOOTER', 'Motorroller'), ('CAR', 'Auto')], default='NA', verbose_name='Fortbewegungsmittel'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='address',
            field=models.CharField(blank=True, max_length=150, verbose_name='Adresse (Straße, Hausnummer)'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='city',
            field=models.CharField(blank=True, max_length=100, verbose_name='Stadt'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Kommentar'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='end_time',
            field=models.DateTimeField(default=offers.models.next_plus_1_hour, verbose_name='Verfügbar bis'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='radius',
            field=models.IntegerField(choices=[(1000, '1 km'), (2000, '2 km'), (3000, '3 km'), (4000, '4 km'), (5000, '5 km'), (10000, '10 km'), (20000, '20 km'), (50000, '50 km')], default=2000, verbose_name='Umkreis'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='start_time',
            field=models.DateTimeField(default=offers.models.next_hour, verbose_name='Verfügbar ab'),
        ),
    ]
