from django.contrib import admin

from .models import Profile, MyUserAuth, OkraLinkedUser

# Register your models here.
admin.site.register(Profile)
admin.site.register(MyUserAuth)
admin.site.register(OkraLinkedUser)