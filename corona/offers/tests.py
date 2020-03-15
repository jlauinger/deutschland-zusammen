from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.test import TestCase

from offers.models import Offer


class OfferTestCase(TestCase):

    # distance is roughly 2800m
    DARMSTADT_HOCHSCHULSTRASSE = Point(49.877212, 8.655164, srid=4326)
    DARMSTADT_SMARAGDWEG = Point(49.872352, 8.680696, srid=4326)

    def setUp(self):
        self.user = User.objects.create_user('user')
        self.offer_big_radius = Offer.objects.create(title='Angebot', user=self.user,
                                                     location=self.DARMSTADT_HOCHSCHULSTRASSE, radius=10000)
        self.offer_small_radius = Offer.objects.create(title='Angebot 2', user=self.user,
                                                       location=self.DARMSTADT_HOCHSCHULSTRASSE, radius=1)

    def test_offers_in_reach_are_found(self):
        offers = Offer.offers_in_range(self.DARMSTADT_SMARAGDWEG)

        self.assertIn(self.offer_big_radius, offers)
        self.assertNotIn(self.offer_small_radius, offers)
