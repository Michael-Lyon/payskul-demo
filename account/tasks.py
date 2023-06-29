from celery import shared_task
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from django.core.mail import send_mail
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
    message = f"""
    Dear {user.first_name},
    You have successfully created an account.
    Your username is {user.username}
    This is the code to activate your account {token}.
    """
    print(user.email)
    mail_sent = send_mail(subject=subject,
                          message=message,
                          from_email=admin_mail,
                          recipient_list=[user.email],
                          fail_silently=False
                          )
    return mail_sent



# @shared_task
# def delete_ 8cd259fb-4eb4-4dbc-a8fd-036b17552ccc


# {"body": "W1sxMjFdLCB7fSwgeyJjYWxsYmFja3MiOiBudWxsLCAiZXJyYmFja3MiOiBudWxsLCAiY2hhaW4iOiBudWxsLCAiY2hvcmQiOiBudWxsfV0=", "content-encoding": "utf-8", "content-type": "application/json", "headers": {"lang": "py", "task": "account.tasks.send_auth_mail", "id": "7b3c4ecd-2f7a-4877-98f8-0a3669ed6843", "shadow": null, "eta": null, "expires": null, "group": null, "group_index": null, "retries": 0, "timelimit": [null, null], "root_id": "7b3c4ecd-2f7a-4877-98f8-0a3669ed6843", "parent_id": null, "argsrepr": "(121,)", "kwargsrepr": "{}", "origin": "gen11@railway", "ignore_result": false}, "properties": {"correlation_id": "7b3c4ecd-2f7a-4877-98f8-0a3669ed6843", "reply_to": "7e3449d8-6b14-356c-8a49-b58f0fd482cd", "delivery_mode": 2, "delivery_info": {"exchange": "", "routing_key": "celery"}, "priority": 0, "body_encoding": "base64", "delivery_tag": "2a8daa40-5744-40cb-a63c-7d9cc28081cb"}}