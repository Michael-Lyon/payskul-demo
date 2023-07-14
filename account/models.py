from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token

from . import utils

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    ref_code = models.CharField(max_length=15, null=True, blank=True)
    pin = models.CharField(max_length=15, blank=True, null=True)
    recomended_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='ref_by')
    signup_confirmation = models.BooleanField(default=False)
    dob = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=400, null=True, blank=True)
    nin = models.CharField(max_length=200, blank=True, null=True)
    verified = models.BooleanField(default=False)
    credit_limit = models.DecimalField(max_digits=100, decimal_places=2, default=0.0)
    has_active_loan = models.BooleanField(default=False)
    credit_validated = models.BooleanField(default=False)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    def get_recommened_profiles(self):
        qs = Profile.objects.all()
        my_recs = []
        for profile in qs:
            try:
                if profile.recomended_by == self.user:
                    my_recs.append(profile.user.username)
            except Exception as e:
                pass
        return my_recs


class Education(models.Model):
    pass


class UserAuthExpiredManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(expires_at__lte=timezone.now())


# MODELS TO STORE AUTHENTICTAION CODES
class UserAuthCodes(models.Model):
    user = models.OneToOneField(User, related_name="user_auth_code", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    code = models.CharField(max_length=10)
    expired = UserAuthExpiredManager()
    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.code = utils.get_code()
        self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user} ({self.code})"


class OkraLinkedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="linked_user")
    customer_id = models.CharField(max_length=100)
    registered_bank_id = models.CharField(max_length=100)
    registered_record = models.CharField(max_length=100)
    income_accounts = models.CharField(max_length=1000, blank=True, null=True)
    income_banks = models.CharField(max_length=1000, blank=True, null=True)
    avg_income = models.DecimalField(decimal_places=2, max_digits=100, default=0.0)
    initial_limit = models.DecimalField(decimal_places=2, max_digits=100, default=0.0)
    balance_ids = models.CharField(max_length=1000, blank=True, null=True)
    
    # collected_nuban = models.BooleanField(default=False)
    def __str__(self):
        return 'Linked user {}'.format(self.user.username)
