
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import  MyUserAuth
from core.models import Wallet

User = get_user_model()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_auth_codes(sender, instance=None, created=False, **kwargs):
    if created:
        MyUserAuth.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_wallet(sender, instance=None, created=False, **kwargs):
    if created:
        Wallet.objects.create(user=instance)

