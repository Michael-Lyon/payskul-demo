from django.shortcuts import render
from okra_utils.utils import Okra
from django.core.mail import send_mail
from payskul.settings import ADMIN_USER
from payskul.settings import EMAIL_HOST_USER as admin_mail

payload = """{
  "method": "AUTH",
  "callback_type": "AUTH",
  "callback_code": "AUTH_SUCCESS",
  "type": "CALLBACK",
  "code": "AUTH_SUCCESS",
  "callbackURL": "https://payskul-demo.up.railway.app/core/webhook/",
  "env": "production-sandbox",
  "status": "is_success",
  "started_at": "2023-06-04T00:27:46.459Z",
  "ended_at": "2023-06-04T00:27:46.521Z",
  "message": "Record callback started!",
  "meta_responses": null,
  "options": {},
  "meta": {},
  "bankName": "Guaranty Trust Bank",
  "bankType": "ind",
  "bankId": "5d6fe57a4099cc4b210bbeb3",
  "bankSlug": "guaranty-trust-bank",
  "record": "647bda64e3226c002ef77012",
  "recordId": "647bda64e3226c002ef77012",
  "callback_url": "https://api.okra.ng/v2/callback?record=647bda64e3226c002ef77012&method=AUTH",
  "login_type": "bank",
  "customerId": "647b92b01519bc002f0c00be",
  "customerEmail": [],
  "country": "NG",
  "extras": {},
  "auth": {
    "clientId": "okr-1685838433712-fc4hTcvnYzVoC9j1Xc3-G",
    "type": "validate",
    "status": true,
    "reauth": false,
    "record": "647bda64e3226c002ef77012",
    "data": {}
  },
  "current_project": "63f157fb1a0f603b1b58423f",
  "owner": "63f157fbbad20d13e7664894"
}
"""


# validate_update_user_satus(payload=payload)

# 1_349_486.0
# 1_180_800.25

def home(request):
    # ok = Okra()
    # data = ok.validate_update_user_status(payload=payload)
    # print(data)
    # subject = f'PaySkul Pin Verification'
    # message = f"""
    # Dear Mike,
    # You have successfully created an account.
    # Your username is Mike
    # This is the code to activate your account.
    # """
    # mail_sent = send_mail(subject,
    #                       message,
    #                       admin_mail,
    #                       ["pygod.dev@mail.com",],
    #                       fail_silently=False)
    # print(mail_sent)
    return render(request, "apiv1/docs.html")