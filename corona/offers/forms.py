from django import forms
from django.contrib.auth.models import User

from offers.models import Offer, ProviderProfile


class OfferSearchForm(forms.Form):
    where = forms.CharField(label='where', max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'Wo? (Straße, Ort)'}))
    when = forms.DateTimeField(label='when', input_formats=['%d.%m.%Y %H:%M'],
                               widget=forms.TextInput(attrs={'placeholder': 'Wann?'}))


class SendMessageForm(forms.ModelForm):
    message = forms.CharField(label='Nachricht', max_length=1000, widget=forms.Textarea())

    class Meta:
        model = User
        fields = ['message']


class OfferForm(forms.ModelForm):
    start_time = forms.DateTimeField(label='Verfügbar ab', input_formats=['%d.%m.%Y %H:%M'],
                                     widget=forms.TextInput(attrs={'placeholder': 'dd.mm.YYYY hh:mm'}))
    end_time = forms.DateTimeField(label='Verfügbar bis', input_formats=['%d.%m.%Y %H:%M'],
                                   widget=forms.TextInput(attrs={'placeholder': 'dd.mm.YYYY hh:mm'}))

    class Meta:
        model = Offer
        fields = ['start_time', 'end_time']


class ProviderProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='Vorname', max_length=100)
    last_name = forms.CharField(label='Nachname', max_length=100)
    email = forms.EmailField(label='E-Mail-Adresse', disabled=True, required=False)

    class Meta:
        model = ProviderProfile
        fields = ['first_name', 'last_name', 'address', 'city', 'radius', 'mobility', 'phone', 'show_phone',
                  'email', 'show_email', 'comment']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
