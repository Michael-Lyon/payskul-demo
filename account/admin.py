from django.contrib import admin

from .models import Profile, UserAuthCodes, OkraLinkedUser

# Register your models here.
admin.site.register(Profile)
admin.site.register(UserAuthCodes)
admin.site.register(OkraLinkedUser)