from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=100, null=True)
    lastName = models.CharField(max_length=100, null=True)
    company = models.CharField(max_length=100, null=True)
    phone = PhoneNumberField()
    email = models.EmailField()
    address = models.CharField(max_length=100, null=True)
