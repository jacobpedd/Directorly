from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contactName = models.CharField(max_length=100, null=True, blank=True)
    firstName = models.CharField(max_length=100, null=True, blank=True)
    lastName = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    public = models.BooleanField(default=False)


class Share(models.Model):
    sharedWith = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sharedWith')
    sharing = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sharing')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    update = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
