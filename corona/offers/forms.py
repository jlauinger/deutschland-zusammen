from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django.utils.translation import gettext_lazy as _

from offers.models import Offer, ProviderProfile, DAYTIME_CHOICES


class OfferSearchForm(forms.Form):
    where = forms.CharField(label='where', max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': _('Wo? (Straße und Ort)'), 'autocomplete':'off'}))
    when = forms.DateTimeField(label='when', input_formats=['%d.%m.%Y'],
                               widget=forms.TextInput(attrs={'placeholder': _('Wann?'), 'autocomplete': 'off'}))

    mobility = forms.ChoiceField(choices=[('', _('-- Mobilität filtern --'))]+list(ProviderProfile.MOBILITY_CHOICES),
                                 required=False, initial='')
    daytime = forms.ChoiceField(choices=DAYTIME_CHOICES, required=False, initial='')


class SendMessageForm(forms.ModelForm):
    sender = forms.CharField(label=_('Dein Name'), max_length=100, required=False)
    email = forms.EmailField(label=_('Deine E-Mail-Adresse'), max_length=100, required=False)
    phone = forms.CharField(label=_('Deine Telefonnummer (optional)'), max_length=100, required=False)
    message = forms.CharField(label=_('Nachricht'), max_length=1000, widget=forms.Textarea())
    captcha = CaptchaField(label=_('Captcha'))

    class Meta:
        model = User
        fields = ['sender', 'email', 'phone', 'message']


class ProviderProfileForm(forms.ModelForm):
    display_name = forms.CharField(label=_('Anzeigename (öffentlich)'), max_length=100, required=True)
    email = forms.EmailField(label=_('E-Mail-Adresse'), disabled=True, required=False)
    street = forms.CharField(label=_('Straße (nicht öffentlich)'), max_length=200)
    city = forms.CharField(label=_('Stadt (nicht öffentlich)'), max_length=200)

    class Meta:
        model = ProviderProfile
        fields = ['display_name', 'street', 'city', 'radius', 'mobility',
                  'offers_shopping', 'offers_petsitting', 'offers_fetching_drugs', 'offers_sending_mail',
                  'offers_courier', 'phone', 'email', 'show_email', 'comment']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class OfferForm(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput())

    class Meta:
        model = Offer
        fields = ['date', 'morning', 'noon', 'afternoon', 'evening']


class BaseOfferFormSet(forms.BaseModelFormSet):
    def __iter__(self):
        return iter(sorted(self.forms, key=lambda x: x['date'].value()))

    def __getitem__(self, index):
        return list(self)[index]


OfferFormSet = modelformset_factory(Offer, form=OfferForm, formset=BaseOfferFormSet, min_num=14, max_num=14)
