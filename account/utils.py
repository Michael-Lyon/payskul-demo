import uuid
import smtplib
import random
import re

from django.core.mail import send_mail
from payskul.settings import ADMIN_USER
from payskul.settings import EMAIL_HOST_USER as admin_mail

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta


def check_pin(pin):
   pattern = r'^\d{6}$'
   if re.match(pattern, pin):
      return True
   return  False
class UniqueRandomNumberGenerator:
   def __init__(self):
      self.generated_numbers = set()

   def generate_unique_random(self):
      while True:
         new_number = random.randint(0, 999999)
         new_number_str = f"{new_number:06d}"
         if new_number_str not in self.generated_numbers:
               self.generated_numbers.add(new_number_str)
               return new_number_str



def schedule_email_task(email_function, email_function_args, delay_seconds):
   # Create and start the scheduler
   scheduler = BackgroundScheduler()
   scheduler.start()

   # Calculate the future time for the task
   future_time = datetime.now() + timedelta(seconds=delay_seconds)

   # Create a DateTrigger for the specified run_date
   trigger = DateTrigger(run_date=future_time)

   # Schedule the email sending function with the trigger
   scheduler.add_job(email_function, args=email_function_args, trigger=trigger)



def get_code():
   gen = UniqueRandomNumberGenerator()
   return gen.generate_unique_random()



def send_signup_email(user):
   try:
      subject = "Welcome to Our Website"
      message = f"""
      Dear {user.first_name},

      Thank you for signing up for our platform! Your account has been successfully created.
      Your username is {user.username}.

      If you have any questions or need assistance, please don't hesitate to contact us.

      Best regards,
      PaySkul LTD.
      """
      send_mail(
         subject=subject,
         message=message,
         from_email="your_email@example.com",  # Replace with your email
         recipient_list=[user.email],
         fail_silently=False,
      )
   except Exception as e:
      print("Email sending failed:", e)


def send_verification_code(email, verification_code):
   subject = f"PaySkul Password Reset Pin"
   message = f"""
   Dear {email},
   A password reset has been requested on yor account.
   Your reset code is {verification_code}.
   Expires in 5 minutes
   """
   send_mail(subject, message, ADMIN_USER,[email] )




def verify_email_smtp(email):
   domain = email.split('@')[1]
   #  try:
      # Establish an SMTP connection with the mail server
   with smtplib.SMTP(domain) as smtp:
      # Send a test email to verify if the server accepts it
      response_code, _ = smtp.rcpt(email)
      if response_code == 250:
         return True
      else:
         return False






