from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contactName = models.CharField(max_length=100, null=True, blank=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    company = models.CharField(max_length=100, null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    photoURL = models.URLField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.contactName


class Share(models.Model):
    sharedWith = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sharedWith')
    sharing = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sharing')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    update = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)


class Group(models.Model):
    name = models.CharField(max_length=100)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    contacts = models.ManyToManyField(Contact)

    def __str__(self):
        return self.name


class GroupInvite(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    invited = models.ForeignKey(User, on_delete=models.CASCADE)
