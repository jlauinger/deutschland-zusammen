from django.contrib.gis import admin

from offers.models import Offer, ProviderProfile, Message, Website


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'morning', 'noon', 'afternoon', 'evening')


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.OSMGeoAdmin):
    list_display = ('user', 'display_name', 'street', 'city', 'radius', 'mobility', 'slug')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender_name', 'sender_email', 'sender_phone', 'date')


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'language')
