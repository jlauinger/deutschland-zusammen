from datetime import timedelta

from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Distance
from django.db.models import F
from django.utils.datetime_safe import datetime
from django.utils.timezone import now, make_aware

from offers.helper import location_from_address


def next_hour():
    n = now() + timedelta(hours=1)
    return make_aware(datetime(year=n.year, month=n.month, day=n.day, hour=n.hour))


def next_plus_1_hour():
    return next_hour() + timedelta(hours=1)


GENDERS = (
    ('M', 'Männlich'),
    ('F', 'Weiblich'),
    ('D', 'Andere'),
    ('X', 'Keine Angabe'),
)


class ProviderProfile(models.Model):
    """
    A provider profile is in a one-to-one relationship with a user. It extends the user profile with some settings that
    are shared among the user's offers.

    The user sets the location with some radius where they want to offer help.

    Radius is in meters.
    """

    class Meta:
        verbose_name = 'Anbieterprofil'
        verbose_name_plural = 'Anbieterprofile'

    RADIUS_CHOICES = (
        (1000, '1 km'),
        (2000, '2 km'),
        (3000, '3 km'),
        (4000, '4 km'),
        (5000, '5 km'),
        (10000, '10 km'),
        (20000, '20 km'),
        (50000, '50 km'),
    )

    MOBILITY_CHOICES = (
        ('NA', 'keine Angabe'),
        ('FOOT', 'zu Fuß / ÖPNV'),
        ('BIKE', 'Fahrrad'),
        ('MOTOR_SCOOTER', 'Motorroller'),
        ('CAR', 'Auto'),
    )

    NAME_VISIBILITY_CHOICES = (
        ('FULL', 'Vor- und Nachname öffentlich'),
        ('FIRST_NAME', 'Nur Vorname öffentlich'),
        ('HIDDEN', 'Weder Vor- noch Nachname öffentlich'),
    )

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)

    location = models.PointField(null=True, default=None)
    radius = models.IntegerField(choices=RADIUS_CHOICES, default=2000,
                                 verbose_name='Umkreis (nicht öffentlich)')
    address = models.CharField(max_length=200, blank=True,
                               verbose_name='Adresse (Straße, Stadt. Nicht öffentlich)')

    mobility = models.TextField(choices=MOBILITY_CHOICES, default='NA',
                                verbose_name='Fortbewegungsmittel (öffentlich sichtbar)')
    offers_shopping = models.BooleanField(default=False, verbose_name='Einkaufen')
    offers_petsitting = models.BooleanField(default=False, verbose_name='Gassi gehen')
    offers_fetching_drugs= models.BooleanField(default=False, verbose_name='Medikamente abholen')
    offers_sending_mail = models.BooleanField(default=False, verbose_name='Briefe einwerfen')
    offers_courier = models.BooleanField(default=False, verbose_name='Kurierdienste')
    comment = models.TextField(blank=True, verbose_name='Sonstige Hilfestellungen oder Kommentare')

    phone = models.CharField(max_length=50, blank=True, verbose_name='Telefonnummer')
    gender = models.CharField(choices=GENDERS, default='X', max_length=50, verbose_name='Geschlecht')
    show_phone = models.BooleanField(default=False, verbose_name='Telefonnummer öffentlich anzeigen')
    show_email = models.BooleanField(default=False, verbose_name='E-Mail-Adresse öffentlich anzeigen')
    show_gender = models.BooleanField(default=False, verbose_name='Geschlecht öffentlich anzeigen')
    name_visibility = models.CharField(choices=NAME_VISIBILITY_CHOICES, default='FIRST_NAME', max_length=50,
                                       verbose_name='Öffentlichkeit deines Namens')

    def save(self, *args, **kwargs):
        if self.address:
            self.location = location_from_address(self.address)
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Profil für {}, {}'.format(self.user.username, self.address)

    def get_display_name(self):
        if self.name_visibility == 'FULL':
            return self.user.get_full_name()
        elif self.name_visibility == 'FIRST_NAME':
            return self.user.first_name
        else:
            return ""


class Offer(models.Model):
    """
    An offer object is an offer by a logged-in user, offering some help.

    It can be found by anybody using the frontend search.
    It can be managed by its logged-in owner user in the backend.
    """

    class Meta:
        verbose_name = 'Hilfsangebot'
        verbose_name_plural = 'Hilfsangebote'

    user = models.ForeignKey(User, related_name='offers', on_delete=models.CASCADE)

    date = models.DateField(default=now, verbose_name='Datum')

    morning = models.BooleanField(default=False, verbose_name='Morgens')
    noon = models.BooleanField(default=False, verbose_name='Mittags')
    afternoon = models.BooleanField(default=True, verbose_name='Nachmittags')
    evening = models.BooleanField(default=False, verbose_name='Abends')

    def __str__(self):
        return '{} am {}'.format(self.user.get_full_name(), self.date)

    @staticmethod
    def offers_in_range(query_location):
        return Offer.objects.annotate(distance=Distance('user__profile__location', query_location))\
            .filter(distance__lte=F('user__profile__radius')).order_by('-distance')

    @staticmethod
    def offers_in_range_and_date(query_location, date):
        return Offer.offers_in_range(query_location).filter(date=date)
