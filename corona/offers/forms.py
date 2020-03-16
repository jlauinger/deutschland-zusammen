from django import forms
from django.contrib.auth.models import User


class OfferSearchForm(forms.Form):
    where = forms.CharField(label='where', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Wo?'}))
    when = forms.DateTimeField(label='when', input_formats=['%d.%m.%Y %H:%M'],
                               widget=forms.TextInput(attrs={'placeholder': 'Wann?'}))


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
