from django.contrib import admin

from .models import Profile, UserAuthCodes

# Register your models here.
admin.site.register(Profile)
admin.site.register(UserAuthCodes)