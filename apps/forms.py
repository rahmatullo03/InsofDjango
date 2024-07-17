import re

from django.contrib.auth.hashers import make_password
from django.forms import ModelForm

from apps.models import User, Booking


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'phone_number', 'email', 'password')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return make_password(password)

    def clean_phone_number(self):
        phone_number = re.sub('\D', '',self.cleaned_data.get('phone_number'))
        return phone_number


class OrderForm(ModelForm):
    class Meta:
        model = Booking
        fields = ('name','phone_number','product')

    def clean_phone_number(self):
        phone_number = re.sub('\D', '',self.cleaned_data.get('phone_number'))
        return phone_number


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'email', 'phone_number')

    def clean_phone_number(self):
        phone_number = re.sub('\D', '',self.cleaned_data.get('phone_number'))
        return phone_number
