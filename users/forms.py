from django import forms
from django.core.exceptions import ValidationError
import re


class User(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)

    phone = forms.CharField(max_length=100, required=False)
    phone_mob = forms.CharField(max_length=100, required=False)

    def phones_clean(self, phfield):
        phone = self.cleaned_data[phfield]
        if not len(phone):
            return phone

        if not phone[0] == '+':
            raise ValidationError('Phone should be in international format')

        phone = re.sub('[\W]', '', phone)

        if not len(phone) == 12:
            raise ValidationError('Phone should be in international format')

        return '+%s' % phone

    def clean_phone(self):
        return self.phones_clean('phone')

    def clean_phone_mob(self):
        return self.phones_clean('phone_mob')

    status = forms.ChoiceField(choices=(
        (0, 'Inactive'),
        (1, 'Active'),
    ))
