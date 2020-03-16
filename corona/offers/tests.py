from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.test import TestCase
from django.utils.datetime_safe import datetime
from django.utils.timezone import make_aware

from offers.helper import location_from_address
from offers.models import Offer


class OfferTestCase(TestCase):
    # distance is roughly 2800m
    DARMSTADT_HOCHSCHULSTRASSE = Point(49.877212, 8.655164, srid=settings.SRID)
    DARMSTADT_SMARAGDWEG = Point(49.8723483, 8.6806331, srid=settings.SRID)

    THURSDAY_NOON = make_aware(datetime(year=2020, month=3, day=12, hour=12, minute=0))
    THURSDAY_AFTERNOON = make_aware(datetime(year=2020, month=3, day=12, hour=16, minute=12))
    THURSDAY_EVENING = make_aware(datetime(year=2020, month=3, day=12, hour=18, minute=0))
    FRIDAY_NOON = make_aware(datetime(year=2020, month=3, day=13, hour=12, minute=0))
    FRIDAY_EVENING = make_aware(datetime(year=2020, month=3, day=13, hour=18, minute=0))

    def setUp(self):
        self.user = User.objects.create_user('user')

    def test_offers_in_reach_are_found(self):
        offer_big_radius = Offer.objects.create(user=self.user, location=self.DARMSTADT_HOCHSCHULSTRASSE, radius=10000)
        offer_small_radius = Offer.objects.create(user=self.user, location=self.DARMSTADT_HOCHSCHULSTRASSE, radius=1)

        offers = Offer.offers_in_range(self.DARMSTADT_SMARAGDWEG)

        self.assertIn(offer_big_radius, offers)
        self.assertNotIn(offer_small_radius, offers)

    def test_offers_in_time_period_are_found(self):
        offer_thursday = Offer.objects.create(user=self.user, location=self.DARMSTADT_HOCHSCHULSTRASSE, radius=10000,
                                              start_time=self.THURSDAY_NOON, end_time=self.THURSDAY_EVENING)
        offer_friday = Offer.objects.create(user=self.user, location=self.DARMSTADT_HOCHSCHULSTRASSE, radius=10000,
                                            start_time=self.FRIDAY_NOON, end_time=self.FRIDAY_EVENING)

        offers = Offer.offers_in_range_and_time(self.DARMSTADT_SMARAGDWEG, self.THURSDAY_AFTERNOON)

        self.assertIn(offer_thursday, offers)
        self.assertNotIn(offer_friday, offers)

    def test_address_to_point_resolution(self):
        location = location_from_address('Smaragdweg 9, 64287 Darmstadt')

        self.assertEquals(self.DARMSTADT_SMARAGDWEG.x, location.x)
        self.assertEquals(self.DARMSTADT_SMARAGDWEG.y, location.y)
