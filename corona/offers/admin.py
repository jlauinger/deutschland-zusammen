from django.contrib.gis import admin

from offers.models import Offer, ProviderProfile


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_time', 'end_time')


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.OSMGeoAdmin):
    list_display = ('user', 'address', 'city', 'radius', 'mobility')
