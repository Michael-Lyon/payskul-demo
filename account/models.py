from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token
import bcrypt
from . import utils

User = get_user_model()


class SecurityQuestion(models.Model):
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    ref_code = models.CharField(max_length=15, null=True, blank=True)
    recomended_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='ref_by')
    signup_confirmation = models.BooleanField(default=False)
    dob = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=400, null=True, blank=True)
    nin = models.CharField(max_length=200, blank=True, null=True)
    verified = models.BooleanField(default=False)
    credit_limit = models.DecimalField(max_digits=100, decimal_places=2, default=0.0)
    has_active_loan = models.BooleanField(default=False)
    credit_validated = models.BooleanField(default=False)
    pin_set = models.BooleanField(default=False)


    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    def save(self, *args, **kwargs):
        if not self.ref_code:
            self.ref_code = self.user.username
        super().save(*args, **kwargs)

    def get_recommended_profiles(self):
        qs = Profile.objects.filter(recomended_by=self.user)
        return qs.values_list('user__username', flat=True)


class UserAuthExpiredManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(expires_at__lte=timezone.now())

class SensitiveData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="sensitive")
    transaction_pin_hash = models.CharField(max_length=128, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    security_question_1 = models.ForeignKey(SecurityQuestion, blank=True, null=True, on_delete=models.SET_NULL, related_name="q1")
    security_answer_1_hash = models.CharField(max_length=128)
    security_question_2 = models.ForeignKey(SecurityQuestion, blank=True, null=True, on_delete=models.SET_NULL, related_name="q2")
    security_answer_2_hash = models.CharField(max_length=128)
    security_question_3 = models.ForeignKey(SecurityQuestion, blank=True, null=True, on_delete=models.SET_NULL, related_name="q3")
    security_answer_3_hash = models.CharField(max_length=128, blank=True, null=True)
    



# MODELS TO STORE AUTHENTICTAION CODES
class MyUserAuth(models.Model):
    user = models.OneToOneField(User, related_name="user_auth_code", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=10, default="123456")
    expired = UserAuthExpiredManager()
    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = utils.get_code()
        self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user} ({self.code})"


class OkraLinkedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="linked_user")
    customer_id = models.CharField(max_length=100)
    registered_record = models.CharField(max_length=100)
    income_accounts = models.CharField(max_length=1000, blank=True, null=True)
    income_banks = models.CharField(max_length=1000, blank=True, null=True)
    avg_income = models.DecimalField(decimal_places=2, max_digits=100, default=0.0)
    initial_limit = models.DecimalField(decimal_places=2, max_digits=100, default=0.0)
    balance_ids = models.CharField(max_length=1000, blank=True, null=True)


    # collected_nuban = models.BooleanField(default=False)
    def __str__(self):
        return 'Linked user {}'.format(self.user.username)


