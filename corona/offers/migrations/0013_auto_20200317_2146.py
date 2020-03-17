# Generated by Django 3.0.4 on 2020-03-17 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0012_providerprofile_name_visibility'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providerprofile',
            name='address',
            field=models.CharField(blank=True, max_length=200, verbose_name='Adresse (Straße, Stadt. Nicht öffentlich)'),
        ),
        migrations.AlterField(
            model_name='providerprofile',
            name='mobility',
            field=models.TextField(choices=[('NA', 'keine Angabe'), ('FOOT', 'zu Fuß / ÖPNV'), ('BIKE', 'Fahrrad'), ('MOTOR_SCOOTER', 'Motorroller'), ('CAR', 'Auto')], default='NA', verbose_name='Fortbewegungsmittel (öffentlich sichtbar)'),
        ),
        migrations.AlterField(
            model_name='providerprofile',
            name='radius',
            field=models.IntegerField(choices=[(1000, '1 km'), (2000, '2 km'), (3000, '3 km'), (4000, '4 km'), (5000, '5 km'), (10000, '10 km'), (20000, '20 km'), (50000, '50 km')], default=2000, verbose_name='Umkreis (nicht öffentlich)'),
        ),
    ]
