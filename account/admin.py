from django.contrib import admin

from .models import Profile, UserAuthCodes, OkraLinkedUser
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Profile)
admin.site.register(UserAuthCodes)
admin.site.register(OkraLinkedUser)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("get_first_name", "get_last_name", "get_email", "credit_limit")
    search_fields = ("get_first_name__icontains", "get_last_name__icontains")

    def get_first_name(self, obj):
        name = User.objects.get(id=obj.user.id)
        return  name.first_name
    
    get_first_name.short_description = "First Name"

    def get_last_name(self, obj):
        name = User.objects.get(id=obj.user.id)
        return  name.last_name
    
    get_last_name.short_description = "Last Name"

    def get_email(self, obj):
        email = User.objects.get(id=obj.user.id)
        return email.email
    
    get_email.short_description = "Email"