from django.contrib.auth.forms import UserCreationForm
from django import forms
import phonenumbers

from .models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        try:
            parsed_phone = phonenumbers.parse(phone, None)
            if not phonenumbers.is_valid_number(parsed_phone):
                raise forms.ValidationError('Invalid phone number format.')
        except phonenumbers.phonenumberutil.NumberParseException:
            raise forms.ValidationError('Invalid phone number format.')

        normalized_phone = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)

        return normalized_phone
        