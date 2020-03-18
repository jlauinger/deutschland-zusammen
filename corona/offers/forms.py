from django import forms
from django.contrib.auth.models import User
from django.forms import formset_factory, modelformset_factory

from offers.models import Offer, ProviderProfile, GENDERS


class OfferSearchForm(forms.Form):
    where = forms.CharField(label='where', max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'Wo? (Straße und Ort)', 'autocomplete':'off'}))
    when = forms.DateTimeField(label='when', input_formats=['%d.%m.%Y'],
                               widget=forms.TextInput(attrs={'placeholder': 'Wann?', 'autocomplete': 'off'}))


class SendMessageForm(forms.ModelForm):
    sender = forms.CharField(label='Dein Name', max_length=100, required=False)
    email = forms.EmailField(label='Deine E-Mail-Adresse', max_length=100, required=False)
    phone = forms.CharField(label='Deine Telefonnummer (optional)', max_length=100, required=False)
    gender = forms.ChoiceField(label='Dein Geschlecht (optional)', choices=GENDERS, required=False)
    message = forms.CharField(label='Nachricht', max_length=1000, widget=forms.Textarea())

    class Meta:
        model = User
        fields = ['sender', 'email', 'phone', 'gender', 'message']


class ProviderProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='Vorname', max_length=100)
    last_name = forms.CharField(label='Nachname', max_length=100)
    email = forms.EmailField(label='E-Mail-Adresse', disabled=True, required=False)
    address = forms.CharField(label='Adresse (Straße, Stadt. Nicht öffentlich)', max_length=200,
                              widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    class Meta:
        model = ProviderProfile
        fields = ['first_name', 'last_name', 'name_visibility', 'address', 'radius', 'mobility', 'offers_shopping',
                  'offers_petsitting', 'offers_fetching_drugs', 'offers_sending_mail', 'offers_courier',
                  'phone', 'show_phone', 'email', 'show_email', 'gender', 'show_gender',
                  'comment']


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
