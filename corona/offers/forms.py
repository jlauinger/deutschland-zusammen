from django import forms
from django.contrib.auth.models import User

from offers.models import Offer, ProviderProfile


class OfferSearchForm(forms.Form):
    where = forms.CharField(label='where', max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'Wo? (Straße und Ort)'}))
    when = forms.DateTimeField(label='when', input_formats=['%d.%m.%Y'],
                               widget=forms.TextInput(attrs={'placeholder': 'Wann?'}))


class SendMessageForm(forms.ModelForm):
    message = forms.CharField(label='Nachricht', max_length=1000, widget=forms.Textarea())

    class Meta:
        model = User
        fields = ['message']


class OfferForm(forms.ModelForm):
    date = forms.DateField(label='Datum', input_formats=['%d.%m.%Y'],
                           widget=forms.TextInput(attrs={'placeholder': 'dd.mm.YYYY'}))

    class Meta:
        model = Offer
        fields = ['date', 'morning', 'noon', 'afternoon', 'evening']


class ProviderProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='Vorname', max_length=100)
    last_name = forms.CharField(label='Nachname', max_length=100)
    email = forms.EmailField(label='E-Mail-Adresse', disabled=True, required=False)

    class Meta:
        model = ProviderProfile
        fields = ['first_name', 'last_name', 'address', 'city', 'radius', 'mobility', 'offers_shopping',
                  'offers_petsitting', 'offers_fetching_drugs', 'offers_sending_mail', 'offers_courier',
                  'phone', 'show_phone', 'email', 'show_email', 'comment']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
