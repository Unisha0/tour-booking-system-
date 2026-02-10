from django import forms
from django.contrib.auth.models import User
from .models import Tourist, Booking


class TouristSignupForm(forms.Form):
    name = forms.CharField(max_length=150, label='Name')
    email = forms.EmailField(label='Email')
    phone_number = forms.CharField(max_length=10, label='Phone Number')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password', strip=False)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password', strip=False)

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone or not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        if not (phone.startswith('98') or phone.startswith('97')):
            raise forms.ValidationError("Phone number must start with 98 or 97.")
        if Tourist.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Phone number already registered.")
        return phone

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') != cleaned.get('password2'):
            self.add_error('password2', "Passwords do not match.")
        return cleaned


class TouristDetailForm(forms.ModelForm):
    class Meta:
        model = Tourist
        fields = ['name', 'email', 'phone', 'dob']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if not phone.isdigit() or len(phone) != 10:
                raise forms.ValidationError("Enter a valid 10-digit phone number.")
            if not (phone.startswith('98') or phone.startswith('97')):
                raise forms.ValidationError("Phone number must start with 98 or 97.")
            qs = Tourist.objects.filter(phone=phone)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Phone number already registered.")
        return phone


class TouristLoginForm(forms.Form):
    identifier = forms.CharField(max_length=150, label='Username or Phone')
    # allow any characters in password and keep whitespace as-is
    password = forms.CharField(widget=forms.PasswordInput, label='Password', strip=False)

from django import forms
from .models import Booking, Hotel, Addon

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['hotel', 'addons', 'days']

    addons = forms.ModelMultipleChoiceField(
        queryset=Addon.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
