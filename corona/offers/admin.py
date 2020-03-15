from django.contrib.gis import admin

from offers.models import Offer


@admin.register(Offer)
class OfferAdmin(admin.OSMGeoAdmin):
    list_display = ('title', 'user', 'start_time')
