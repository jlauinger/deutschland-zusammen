from django.conf import settings
from django.contrib.gis.geos import Point
from geopy import Nominatim


DEFAULT_POINT = Point(49.877212, 8.655164, srid=settings.SRID)


def location_from_address(address):
    locator = Nominatim(user_agent=settings.NOMINATIM_USER_AGENT)
    location = locator.geocode(address)
    if location:
        return Point(location.latitude, location.longitude, srid=settings.SRID)
    else:
        return DEFAULT_POINT
