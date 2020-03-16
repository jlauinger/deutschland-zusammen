from django import forms
from django.contrib.auth.models import User

from offers.models import Offer


class OfferSearchForm(forms.Form):
    where = forms.CharField(label='where', max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'Wo? (Straße, Ort)'}))
    when = forms.DateTimeField(label='when', input_formats=['%d.%m.%Y %H:%M'],
                               widget=forms.TextInput(attrs={'placeholder': 'Wann?'}))


class OfferForm(forms.ModelForm):
    start_time = forms.DateTimeField(label='Verfügbar ab', input_formats=['%d.%m.%Y %H:%M'],
                                     widget=forms.TextInput(attrs={'placeholder': 'dd.mm.YYYY hh:mm'}))
    end_time = forms.DateTimeField(label='Verfügbar bis', input_formats=['%d.%m.%Y %H:%M'],
                                   widget=forms.TextInput(attrs={'placeholder': 'dd.mm.YYYY hh:mm'}))

    class Meta:
        model = Offer
        fields = ['start_time', 'end_time']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
