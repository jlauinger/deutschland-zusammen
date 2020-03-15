from datetime import timedelta

from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Distance
from django.db.models import F
from django.utils.datetime_safe import datetime
from django.utils.timezone import now, make_aware


def next_hour():
    n = now() + timedelta(hours=1)
    return make_aware(datetime(year=n.year, month=n.month, day=n.day, hour=n.hour))


def next_plus_1_hour():
    return next_hour() + timedelta(hours=1)


class Offer(models.Model):
    """
    An offer object is an offer by a logged-in user at some point with a radius, offering some help.

    It can be found by anybody using the frontend search.
    It can be managed by its logged-in owner user in the backend.

    Radius is in meters.
    """

    class Meta:
        verbose_name = 'Hilfeangebot'
        verbose_name_plural = 'Hilfeangebote'

    user = models.ForeignKey(User, related_name='offers', on_delete=models.CASCADE)

    location = models.PointField()
    radius = models.IntegerField(default=1000)
    address = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100, blank=True)

    start_time = models.DateTimeField(default=next_hour)
    end_time = models.DateTimeField(default=next_plus_1_hour)

    title = models.CharField(max_length=100)
    comment = models.TextField(blank=True)

    def __str__(self):
        return '{} von {} am {}'.format(self.title, self.user.get_full_name(), self.start_time)

    @staticmethod
    def offers_in_range(query_location):
        return Offer.objects.annotate(distance=Distance('location', query_location)).filter(distance__lte=F('radius'))

    @staticmethod
    def offers_in_range_and_time(query_location, time):
        return Offer.offers_in_range(query_location).filter(start_time__lte=time, end_time__gte=time)
