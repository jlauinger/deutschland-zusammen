from django.conf import settings
from django.contrib.gis.geos import Point
from geopy import Nominatim


def location_from_address(address):
    locator = Nominatim(user_agent=settings.NOMINATIM_USER_AGENT)
    location = locator.geocode(address)
    return Point(location.latitude, location.longitude, srid=settings.SRID)
