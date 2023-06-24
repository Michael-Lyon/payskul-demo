import uuid

from django.core.mail import send_mail
from payskul.settings import ADMIN_USER
from payskul.settings import EMAIL_HOST_USER as admin_mail

def get_code():
   return  str(uuid.uuid1())[:6]


def send_verification_code(email, verification_code):
  
   subject = f"PaySkul Password Reset Pin"
   message = f"""
   Dear {email},
   A password reset has been requested on yor account.
   Your reset pin is {verification_code}.
   """
   send_mail(subject, message, ADMIN_USER,[email] )