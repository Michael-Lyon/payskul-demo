from datetime import datetime
import random
from dotenv import load_dotenv
import os
import requests
import json
from django.contrib.auth.models import User
from django.core.mail import send_mail
from payskul.settings import EMAIL_HOST_USER as SENDER
from account.models import OkraLinkedUser
import traceback
import logging

load_dotenv()

class OkraSetup:
    _BASE = "https://api.okra.ng/v2/"
    _LOGGER = logging.getLogger('okra_validator')

    # INCOME URLS
    _PROCESS_INCOME_URL = _BASE + "income/process"
    _INCOME_CUSTOMER_URLS = _BASE + "income/getByCustomer"
    _INCOME_ID_URL = _BASE + "income/getById"

    _GET_ACCOUNT_CUSTOMER = _BASE + "accounts/getByCustomer"

    # IDENTITY URLS
    _IDENTITY_URL =  _BASE + "products/kyc/customer-verify"
    _IDENTITY_URL_2 =  _BASE + "identity/getByCustomer"

    # BANK URLS
    _BANKS_LIST_URL = _BASE + "banks/list"

    # ACCOUNT URLS
    _ACCOUNT_CUSTOMER_URL = _BASE + "accounts/getByCustomer"

    # PAYMENT URLS
    _INITIATE_PAYMENT_URL = "https://api.paystack.co/charge"



    # KEYS
    _SECRET = os.getenv("OKRA_SECRET")
    _PUBLIC = os.getenv("OKRA_PUBLIC")
    
    _PAYSTACK_SECRET = os.getenv("PAYSATCK_SECRET")
    _PAYSTACK_PUBLIC = os.getenv("PAYSATCK_PUBLIC")

    # HEADERS
    _HEADERS = {
            "accept": "application/json; charset=utf-8",
            "content-type": "application/json",
            "authorization": f"Bearer {_SECRET}"
        }
    
    _PAYSTACK_HEADERS = {
            "accept": "application/json; charset=utf-8",
            "content-type": "application/json",
            "authorization": f"Bearer {_PAYSTACK_SECRET}"
        }
    

    # PAYSTACK URLS
    _PAYSTACK_BANKS_LIST_URL= "https://api.paystack.co/bank"




class Okra(OkraSetup):
    _to_save = {}
    # def __init__(self):
        
    # @classmethod
    def validate_update_user_status(self, payload, user=None):
        data = payload
        print("DATA RECIEVED: ",data)
        if data["method"] == "IDENTITY":
            customerId = data["customerId"]
            self._to_save["customer_id"] = customerId
            self._to_save["registered_record"] = data["record"]
            self._to_save["registered_bank_id"] = data["bankId"]
            try:
                # TODO: IF IT'S NOT SECCESS AND DUMMY DATA TO JUST TEST WITH
                
                # if self._is_identity_auth_success(identity_data):
                identity = data["identity"]
                dob = identity["dob"]
                phone_number = identity["phone"][0]
                bvn = identity["bvn"]
                address = identity["address"][0]
                try:
                    if user == None:
                        # identity = identity_data["data"]["identity"]
                        first_name = identity["firstname"]
                        last_name = identity["lastname"]
                        user = self._get_user_from_database(first_name, last_name)
                    profile = user.profile
                    # TODO: These should be re-activated upon update from OKRA
                    profile.dob = datetime.strptime(dob, "%Y-%m-%d").date()
                    profile.phone_number = phone_number
                    profile.nin = bvn
                    profile.address = address
                    self._to_save["user"] = user
                    income_data = self._get_processed_income(customerId)
                    if self._is_income_processing_success(income_data):
                        income = income_data['data']["income"]
                        confidence = self._get_income_confidence(income)
                        if confidence > 50:
                            avg_income, credit_limit = self._calculate_credit_limit(income)
                            self._to_save["avg_income"] = avg_income
                            self._to_save["initial_limit"] = credit_limit
                            profile.credit_limit = credit_limit
                            profile.credit_validated = True
                            profile.save()
                            obj, created = OkraLinkedUser.objects.get_or_create(**self._to_save)
                            obj.save()
                            return True
                        else:
                            self._LOGGER.error("Confidence not good enough")
                    else:
                        self._LOGGER.error("Failed to get income")
                        self._LOGGER.error(income_data)
                except User.DoesNotExist as e:
                    self._LOGGER.exception("OKRA_VALIDATION CAUGHT USERERROR: %s", str(e))
                    self._send_mail("OKRA_VALIDATION CAUGHT USERERROR:", e)
                    
                # else:
                #     logging.error("Identity auth: %s", identity_data)
            except Exception as e:
                self._LOGGER.exception("OKRA_VALIDATION CAUGHT IDENTIFY USER ERROR: %s", str(e))
                self._send_mail("OKRA_VALIDATION CAUGHT IDENTIFY USER ERROR", e)
        else:
           self._LOGGER.error("Auth auth: %s", data)
        return  False
    
    
    def update_customer_income_data(self, user, customerId):
        try:
            profile = user.profile
            self._to_save["user"] = user
            income_data = self._get_processed_income(customerId)
            if self._is_income_processing_success(income_data):
                income = income_data['data']["income"]
                confidence = self._get_income_confidence(income)
                if confidence > 50:
                    avg_income, credit_limit = self._calculate_credit_limit(income)
                    self._to_save["avg_income"] = avg_income
                    self._to_save["initial_limit"] = credit_limit
                    profile.credit_limit = credit_limit
                    profile.credit_validated = True
                    profile.save()
                    obj = OkraLinkedUser.objects.filter(user=profile.user)
                    obj.update(**self._to_save)
                    self._LOGGER.info(f"New user created: {self._to_save}")
                    return {"credit_limit": credit_limit}
                else:
                    self._LOGGER.error("Confidence not good enough")
            else:
                self._LOGGER.error("Failed to get income")
                self._LOGGER.error(income_data)
            return {}
        except Exception as e:
            traceback.print_exc()
            self._LOGGER.error(f"Failed to get income from OKRA(API): {e}")
            self._send_mail("Failed to get income:", error=e)
        return None


    def get_nuban_balances(self, customer):
        print("Getting nuban balances")
        okra_linked_user = OkraLinkedUser.objects.get(customer_id=customer)
        accounts_response = requests.post(url=self._ACCOUNT_CUSTOMER_URL, json={"customer":customer}, headers= self._HEADERS).json()
        if accounts_response["status"] == "success":
            details = accounts_response
            accounts = details["account"]
            nuban, balance, names = self._get_account_numbers(accounts)
            okra_linked_user.balance_ids = balance
            okra_linked_user.income_accounts = nuban
            okra_linked_user.income_banks = names
            okra_linked_user.save()
            return True
        else:
            return False
        
    
    def get_balance(self, balance_id):
        print("getting balance")
        response = requests.post(url=self._ACCOUNT_CUSTOMER_URL, json={"id":balance_id}, headers= self._HEADERS).json()

        return self._parse_balance(response)



    def _is_valid_auth_success(self, data):
        return (
            data["method"] == "AUTH" and
            data["code"] == "AUTH_SUCCESS" and
            data["status"] == "is_success"
        )
    

    def _is_identity_auth_success(self, identity_data):
        return identity_data["status"] == "success"
    


    # A call to OKRA API
    def _get_identity_details(self, customerId):
        id_payload = {"customer": customerId}
        identity_response = requests.post(url=self._IDENTITY_URL, json=id_payload, headers=self._HEADERS)
        return identity_response.json()
    

    # Get user from DB using first_name and last_name fields
    def _get_user_from_database(self, first_name, last_name):
        return User.objects.get(first_name=first_name, last_name=last_name)
    

    def _is_income_processing_success(self, income_data):
        return income_data["status"] == "success"
    

    def _get_processed_income(self, customerId):
        print("Getting processed income")
        income_response = requests.post(url=self._PROCESS_INCOME_URL,
                                        json={"customer_id": customerId},
                                        headers=self._HEADERS)
        return income_response.json()
    

    def _get_income_confidence(self, income):
        confidence = income["confidence"]
        if isinstance(confidence, str):
            confidence = float(confidence[:-1])
        return confidence
    

    def _calculate_credit_limit(self, income):
        streams = income["streams"]
        # accounts = ':'.join(stream["account"] for stream in streams)
        banks = ':'.join(stream["bank"] for stream in streams)
        total_income = sum(stream["avg_monthly_income"] for stream in streams)
        avg_income = total_income / len(streams)
        credit_limit = avg_income * (87.5 / 100)
        # self._to_save["income_accounts"] = accounts
        # self._to_save["income_banks"] = banks
        return avg_income, credit_limit
    
    
    def _get_account_numbers(self, accounts):
            """Gets the user nuban, balance id and bank names"""
            nuban = ':'.join(account["nuban"] for account in accounts)
            balance = ':'.join(account["balance"] for account in accounts)
            names = ":".join(account["bank"]["name"] for account in accounts)
            return nuban, balance, names
            

    def _initiate_payment(self, acc_deb, user, bank_code, amount):
        profile = profile.objects.get(user=user)
        amount = str(amount * 100) # convert amount to KOBO
        payload = { "email": user.email, 
            "amount": amount, 
            "bank": {
                "code": f"{bank_code}", 
                "account_number": f"{acc_deb}" 
            },
            "birthday": profile.dob.strftime("%Y-%m-%d")
        }
        payment_response = requests.post(url=self._INITIATE_PAYMENT_URL, json=payload, headers=self._HEADERS).json()
        if payment_response["status"] == True:
            status = payment_response["data"]["status"]
            ref = payment_response["data"]["reference"]

            return status, ref
        return None
    

    # GET THE BALANCE
    def _parse_balance(self, response):
        if "data" in response and "balance" in response["data"]:
            balance_data = response["data"]["balance"]
            if "available_balance" in balance_data:
                return balance_data["available_balance"]
        return None

    def _send_mail(self, message, error):
        try:
            send_mail(
                    "PaySkul Error On Okra validation", f"{message}: {error}", 
                    from_email=SENDER, recipient_list=["pygod.dev@mail.com"], fail_silently=False
                   )
        except Exception as e:
           self._LOGGER.error("Send mail error: %s", e)

    
    @staticmethod
    def bank_list():
        try:
            response = requests.get(url=Okra._BANKS_LIST_URL, headers=Okra._HEADERS)
            data = response.json()['data']['banks']
            if not data:
                return []
            return [ {"id": bank['id'], "name":bank['name']} for bank in data]
        except Exception as e:
            print(e)
        return []
    

    @staticmethod
    def paystack_banks():
        try:
            response = requests.get(url=Okra._PAYSTACK_BANKS_LIST_URL, headers=Okra._PAYSTACK_HEADERS)
            data = response.json()['data']
            if not data:
                return []
            return [ {"code": bank['code'], "name":bank['name']} for bank in data]
        except Exception as e:
            print(e)
        return []

