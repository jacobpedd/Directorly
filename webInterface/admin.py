from django.contrib import admin
from .models import Contact, Share, Group, GroupInvite

admin.site.register(Contact)
admin.site.register(Share)
admin.site.register(Group)
admin.site.register(GroupInvite)

