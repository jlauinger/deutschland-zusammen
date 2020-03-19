from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.test import TestCase
from django.utils.datetime_safe import datetime
from django.utils.timezone import make_aware

from offers.helper import location_from_address, address_from_location, address_autocomplete
from offers.models import Offer, ProviderProfile


class OfferTestCase(TestCase):
    # distance is roughly 2800m
    DARMSTADT_HOCHSCHULSTRASSE = Point(49.877212, 8.655164, srid=settings.SRID)
    DARMSTADT_SMARAGDWEG = Point(49.8723483, 8.6806331, srid=settings.SRID)

    THURSDAY = make_aware(datetime(year=2020, month=3, day=12))
    FRIDAY = make_aware(datetime(year=2020, month=3, day=13))

    def setUp(self):
        self.big_radius_user = User.objects.create_user('big_radius_user', first_name='Vorname Nachname')
        self.small_radius_user = User.objects.create_user('small_radius_user')
        self.big_radius_profile = ProviderProfile.objects.create(location=self.DARMSTADT_HOCHSCHULSTRASSE, radius=10000,
                                                                 user=self.big_radius_user, activated=True)
        self.small_radius_profile = ProviderProfile.objects.create(location=self.DARMSTADT_HOCHSCHULSTRASSE, radius=1,
                                                                   user=self.small_radius_user, activated=True)

    def test_offers_in_reach_are_found(self):
        offer_big_radius = Offer.objects.create(user=self.big_radius_user)
        offer_small_radius = Offer.objects.create(user=self.small_radius_user)

        offers = Offer.offers_in_range(self.DARMSTADT_SMARAGDWEG)

        self.assertIn(offer_big_radius, offers)
        self.assertNotIn(offer_small_radius, offers)

    def test_offers_in_time_period_are_found(self):
        offer_thursday = Offer.objects.create(user=self.big_radius_user, date=self.THURSDAY)
        offer_friday = Offer.objects.create(user=self.big_radius_user, date=self.FRIDAY)

        offers = Offer.offers_in_range_and_date(self.DARMSTADT_SMARAGDWEG, self.THURSDAY)

        self.assertIn(offer_thursday, offers)
        self.assertNotIn(offer_friday, offers)

    def test_only_activated_profiles_are_found(self):
        user_not_activated = User.objects.create_user('not_activated_user')
        profile_not_activated = ProviderProfile.objects.create(location=self.DARMSTADT_HOCHSCHULSTRASSE, radius=10000,
                                                               user=user_not_activated, activated=False)
        offer_activated = Offer.objects.create(user=self.big_radius_user)
        offer_not_activated = Offer.objects.create(user=user_not_activated)

        offers = Offer.offers_in_range(self.DARMSTADT_SMARAGDWEG)

        self.assertIn(offer_activated, offers)
        self.assertNotIn(offer_not_activated, offers)

    def test_address_to_point_resolution(self):
        location = location_from_address('Smaragdweg 9, 64287 Darmstadt')

        self.assertEquals(self.DARMSTADT_SMARAGDWEG.x, location.x)
        self.assertEquals(self.DARMSTADT_SMARAGDWEG.y, location.y)

    def test_point_to_address_resolution(self):
        address = address_from_location(self.DARMSTADT_SMARAGDWEG.x, self.DARMSTADT_SMARAGDWEG.y)

        self.assertEquals('14, Smaragdweg, Edelsteinviertel, Darmstadt-Ost, Darmstadt, Hessen, 64287, Deutschland',
                          address)

    def test_address_autocomplete(self):
        suggestions = address_autocomplete("Hochschulstr")

        self.assertIn('Hochschulstraße, Darmstadt', suggestions)

    def test_name_visibility_has_an_effect(self):
        user_full_name = User.objects.create_user('full-name', first_name='Vorname', last_name='Nachname')
        user_first_name = User.objects.create_user('first-name', first_name='Vorname', last_name='Nachname')
        user_hidden_name = User.objects.create_user('hidden-name', first_name='Vorname', last_name='Nachname')
        profile_full_name = ProviderProfile.objects.create(user=user_full_name, name_visibility='FULL')
        profile_first_name = ProviderProfile.objects.create(user=user_first_name, name_visibility='FIRST_NAME')
        profile_hidden_name = ProviderProfile.objects.create(user=user_hidden_name, name_visibility='HIDDEN')

        self.assertEquals(profile_full_name.get_display_name(), "Vorname Nachname")
        self.assertEquals(profile_first_name.get_display_name(), "Vorname")
        self.assertEquals(profile_hidden_name.get_display_name(), "")
