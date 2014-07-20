from django import forms

class SponsoredMessageForm(forms.Form):
    message = forms.CharField()
    channel = forms.CharField()
    latitude = forms.DateField()
    longitude = forms.DateField()
    time = forms.DateTimeField()