from django import forms
from django.core.exceptions import ValidationError
from . import models

class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs) 

       self.fields['first_name'].widget.attrs.update({
           'class': '',
           'placeholder': 'First Name',
       })

    class Meta:
        model = models.Contact
        fields = (
            'first_name', 'last_name', 'phone',
            'email', 'description', 'category',
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