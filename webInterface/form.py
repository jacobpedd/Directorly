from django import forms
from .models import Contact, Group
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget


class ContactForm(forms.ModelForm):
    phone = PhoneNumberField(widget=PhoneNumberInternationalFallbackWidget)

    class Meta:
        model = Contact
        fields = ('contactName', 'firstName', 'lastName', 'photoURL', 'company', 'phone', 'email', 'address', 'public')


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)
