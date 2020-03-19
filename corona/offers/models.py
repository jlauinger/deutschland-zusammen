from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Distance
from django.core.mail import send_mail
from django.db.models import F
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.utils.timezone import now, make_aware
from django.utils.translation import gettext_lazy as _

from offers.helper import location_from_address, create_activation_token, create_profile_slug


def next_hour():
    n = now() + timedelta(hours=1)
    return make_aware(datetime(year=n.year, month=n.month, day=n.day, hour=n.hour))


def next_plus_1_hour():
    return next_hour() + timedelta(hours=1)


GENDERS = (
    ('M', _('Männlich')),
    ('F', _('Weiblich')),
    ('D', _('Andere')),
    ('X', _('Keine Angabe')),
)


class ProviderProfile(models.Model):
    """
    A provider profile is in a one-to-one relationship with a user. It extends the user profile with some settings that
    are shared among the user's offers.

    The user sets the location with some radius where they want to offer help.

    Radius is in meters.
    """

    class Meta:
        verbose_name = _('Anbieterprofil')
        verbose_name_plural = _('Anbieterprofile')

    RADIUS_CHOICES = (
        (1000, '1 km'),
        (2000, '2 km'),
        (3000, '3 km'),
        (4000, '4 km'),
        (5000, '5 km'),
        (10000, '10 km'),
        (20000, '20 km'),
        (50000, '50 km'),
    )

    MOBILITY_CHOICES = (
        ('NA', _('keine Angabe')),
        ('FOOT', _('zu Fuß / ÖPNV')),
        ('BIKE', _('Fahrrad')),
        ('MOTOR_SCOOTER', _('Motorroller')),
        ('CAR', _('Auto')),
    )

    NAME_VISIBILITY_CHOICES = (
        ('FULL', _('Vor- und Nachname öffentlich')),
        ('FIRST_NAME', _('Nur Vorname öffentlich')),
        ('HIDDEN', _('Weder Vor- noch Nachname öffentlich')),
    )

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)

    slug = models.CharField(max_length=20, default=create_profile_slug, unique=True, verbose_name='ID-Token')
    activation_token = models.CharField(max_length=64, default=create_activation_token,
                                        verbose_name=_('Aktivierungsschlüssel'))
    activated = models.BooleanField(default=False, verbose_name=_('Aktiviert'))

    location = models.PointField(null=True, default=None)
    radius = models.IntegerField(choices=RADIUS_CHOICES, default=2000,
                                 verbose_name=_('Umkreis (nicht öffentlich)'))
    address = models.CharField(max_length=200, blank=True,
                               verbose_name=_('Adresse (Straße, Stadt. Nicht öffentlich)'))

    mobility = models.TextField(choices=MOBILITY_CHOICES, default='NA',
                                verbose_name=_('Fortbewegungsmittel (öffentlich sichtbar)'))
    offers_shopping = models.BooleanField(default=False, verbose_name=_('Einkaufen'))
    offers_petsitting = models.BooleanField(default=False, verbose_name=_('Gassi gehen'))
    offers_fetching_drugs= models.BooleanField(default=False, verbose_name=_('Medikamente abholen'))
    offers_sending_mail = models.BooleanField(default=False, verbose_name=_('Briefe einwerfen'))
    offers_courier = models.BooleanField(default=False, verbose_name=_('Kurierdienste'))
    comment = models.TextField(blank=True, verbose_name=_('Sonstige Hilfestellungen oder Kommentare'))

    phone = models.CharField(max_length=50, blank=True, verbose_name=_('Telefonnummer'))
    gender = models.CharField(choices=GENDERS, default='X', max_length=50, verbose_name=_('Geschlecht'))
    show_phone = models.BooleanField(default=False, verbose_name=_('Telefonnummer öffentlich anzeigen'))
    show_email = models.BooleanField(default=False, verbose_name=_('E-Mail-Adresse öffentlich anzeigen'))
    show_gender = models.BooleanField(default=False, verbose_name=_('Geschlecht öffentlich anzeigen'))
    name_visibility = models.CharField(choices=NAME_VISIBILITY_CHOICES, default='FIRST_NAME', max_length=50,
                                       verbose_name=_('Öffentlichkeit deines Namens'))

    def __str__(self):
        return 'Profil für {}, {}'.format(self.user.username, self.address)

    def save(self, *args, **kwargs):
        if self.address:
            self.location = location_from_address(self.address)
        super().save(*args, **kwargs)

    def get_display_name(self):
        if self.name_visibility == 'FULL':
            return self.user.get_full_name()
        elif self.name_visibility == 'FIRST_NAME':
            return self.user.first_name
        else:
            return ""

    def send_activation_mail(self):
        activation_link = "{}{}".format(settings.HOST_NAME, reverse_lazy('activate_account',
                                                                         args=[self.slug, self.activation_token]))
        body = settings.ACTIVATION_MAIL_BODY.format(self.user.first_name, activation_link)
        send_mail(settings.ACTIVATION_MAIL_SUBJECT, body, settings.ACTIVATION_MAIL_FROM, [self.user.email],
                  fail_silently=False)


class Offer(models.Model):
    """
    An offer object is an offer by a logged-in user, offering some help.

    It can be found by anybody using the frontend search.
    It can be managed by its logged-in owner user in the backend.
    """

    class Meta:
        verbose_name = _('Hilfsangebot')
        verbose_name_plural = _('Hilfsangebote')

    user = models.ForeignKey(User, related_name='offers', on_delete=models.CASCADE)

    date = models.DateField(default=now, verbose_name=_('Datum'))

    morning = models.BooleanField(default=False, verbose_name=_('Morgens'))
    noon = models.BooleanField(default=False, verbose_name=_('Mittags'))
    afternoon = models.BooleanField(default=False, verbose_name=_('Nachmittags'))
    evening = models.BooleanField(default=False, verbose_name=_('Abends'))

    def __str__(self):
        return '{} am {}'.format(self.user.get_full_name(), self.date)

    @staticmethod
    def offers_in_range(query_location):
        return Offer.objects.annotate(distance=Distance('user__profile__location', query_location))\
            .filter(user__profile__activated=True)\
            .filter(distance__lte=F('user__profile__radius')).order_by('-distance')

    @staticmethod
    def offers_in_range_and_date(query_location, date):
        return Offer.offers_in_range(query_location).filter(date=date)


class Message(models.Model):
    """
    A message is an (e-mail) message that an anonymous user sent to a logged-in user who put in an offer.

    It is sent by mail to the logged-in user.
    It is stored in database for future troubleshooting.
    """

    class Meta:
        verbose_name = _('Gesendete Nachricht')
        verbose_name_plural = _('Gesendete Nachrichten')

    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)

    sender_name = models.CharField(max_length=100, blank=True)
    sender_email = models.CharField(max_length=100, blank=True)
    sender_phone = models.CharField(max_length=100, blank=True)
    sender_gender = models.CharField(choices=GENDERS, max_length=50, default='X')

    message = models.TextField(blank=True)

    date = models.DateTimeField(default=now)

    def __str__(self):
        return "Nachricht am {} von {} an {}".format(self.date, self.sender_name, self.recipient.get_full_name())

    def send(self):
        send_mail(settings.CONTACT_MAIL_SUBJECT, self.message, settings.CONTACT_MAIL_FROM, [self.recipient.email],
                  fail_silently=False)
