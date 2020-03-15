from django import forms


class OfferSearchForm(forms.Form):
    where = forms.CharField(label='where', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Wo?'}))
    when = forms.DateTimeField(label='when', input_formats=['%d.%m.%Y %H:%M'],
                               widget=forms.TextInput(attrs={'placeholder': 'Wann?'}))
