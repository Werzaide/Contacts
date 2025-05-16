from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models

class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
            }
        )
    )

    class Meta:
        model = models.Contact
        fields = (
            'first_name', 'last_name', 'phone',
            'email', 'description', 'category',
            'picture',
            )
        

    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == last_name:
            msg = ValidationError(
                    'First name cannot be the same as Last name',
                    code='invalid'
                )
            self.add_error('first_name', msg)
            self.add_error('last_name', msg)



        return super().clean()


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=2,
    )
    last_name = forms.CharField(
        required=True,
    )
    email = forms.CharField(
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Email already in use', code='invalid')
            )

        return email