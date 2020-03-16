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

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)

    location = models.PointField()
    radius = models.IntegerField(choices=RADIUS_CHOICES, default=2000, verbose_name='Umkreis')
    address = models.CharField(max_length=150, blank=True, verbose_name='Adresse (Straße, Hausnummer)')
    city = models.CharField(max_length=100, blank=True, verbose_name='Stadt')

    mobility = models.TextField(choices=MOBILITY_CHOICES, default='NA', verbose_name='Fortbewegungsmittel')
    comment = models.TextField(blank=True, verbose_name='Kommentar')

    def save(self, *args, **kwargs):
        self.location = location_from_address("{}, {}".format(self.address, self.city))
        super().save(*args, **kwargs)


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

    start_time = models.DateTimeField(default=next_hour, verbose_name='Verfügbar ab')
    end_time = models.DateTimeField(default=next_plus_1_hour, verbose_name='Verfügbar bis')

    def __str__(self):
        return '{} bis {} von {}'.format(self.start_time, self.end_time.time, self.user.get_full_name())

    @staticmethod
    def offers_in_range(query_location):
        return Offer.objects.annotate(distance=Distance('user__profile__location', query_location))\
            .filter(distance__lte=F('user__profile__radius')).order_by('-distance')

    @staticmethod
    def offers_in_range_and_time(query_location, time):
        return Offer.offers_in_range(query_location).filter(start_time__lte=time, end_time__gte=time)
