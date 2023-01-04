from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token

from payskul.settings import ADMIN_USER
from payskul.settings import EMAIL_HOST_USER as admin_mail

from .models import UserAuthCodes

User = get_user_model()

@shared_task
def send_auth_mail(user_id):
    """
    Sends auth code mails to users
    """
    user = User.objects.get(id=user_id)
    token = UserAuthCodes.objects.get(user=user).code
    subject = f'PaySkul Pin Verification'
    message = f'Dear {user.first_name},\n\n' \
        f'You have successfully created an account.' \
        f'This is the code to activate your account {token}.'
    mail_sent = send_mail(subject,
                          message,
                          ADMIN_USER,
                          [user.email]
                          )
    return mail_sent



# @shared_task
# def delete_