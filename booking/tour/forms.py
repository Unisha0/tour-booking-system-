from django import forms
from django.contrib.auth.models import User
from .models import Tourist, Booking


class TouristSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class TouristDetailForm(forms.ModelForm):
    class Meta:
        model = Tourist
        fields = ['phone', 'address']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['persons']