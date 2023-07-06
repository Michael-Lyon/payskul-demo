import uuid
import smtplib


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

   #  except smtplib.SMTPConnectError:
   #      print("Failed to connect to the mail server.")
   #  except smtplib.SMTPServerDisconnected:
   #      print("SMTP server disconnected unexpectedly.")
   #  except smtplib.SMTPException as e:
   #      print("SMTP error occurred:", str(e))