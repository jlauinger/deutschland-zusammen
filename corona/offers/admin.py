from django.contrib.gis import admin

from offers.models import Offer, ProviderProfile, Message


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'morning', 'noon', 'afternoon', 'evening')


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.OSMGeoAdmin):
    list_display = ('user', 'address', 'radius', 'mobility', 'slug')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender_name', 'sender_email', 'sender_phone', 'date')
