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
    _BASE = "https://api.okra.ng/v2/sandbox/"
    _LOGGER = logging.getLogger('okra_validator')

    # INCOME URLS
    _PROCESS_INCOME_URL = _BASE + "income/process"
    _INCOME_CUSTOMER_URLS = _BASE + "income/getByCustomer"
    _INCOME_ID_URL = _BASE + "income/getById"

    # IDENTITY URLS
    _IDENTITY_URL =  _BASE + "identity/getByCustomer"

    # BANK URLS
    _BANKS_LIST_URL = _BASE + "banks/list"

    # ACCOUNT URLS
    _ACCOUNT_CUSTOMER_URL = _BASE + "accounts/getByCustomer"

    # PAYMENT URLS
    _INITIATE_PAYMENT_URL = _BASE + "pay/initiate"

    # KEYS
    _SECRET = os.getenv("OKRA_SECRET")
    _PUBLIC = os.getenv("OKRA_PUBLIC")

    # HEADERS
    _HEADERS = {
            "accept": "application/json; charset=utf-8",
            "content-type": "application/json",
            "authorization": f"Bearer {_SECRET}"
        }



class Okra(OkraSetup):
    _to_save = {}
    # def __init__(self):
        
    # @classmethod
    def validate_update_user_status(self, payload):
        data = json.loads(payload)
        print(data)
        if self._is_valid_auth_success(data):
            customerId = data["customerId"]
            self._to_save["customer_id"] = customerId
            self._to_save["registered_record"] = data["record"]
            self._to_save["registered_bank_id"] = data["bankId"]
            try:
                identity_data = self._get_identity_details(customerId)
                if self._is_identity_auth_success(identity_data):
                    identity = identity_data["data"]["identity"][0]
                    first_name = identity["firstname"]
                    last_name = identity["lastname"]
                    try:
                        user = self._get_user_from_database(first_name, last_name)
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
                                obj = OkraLinkedUser.objects.get_or_create(**self._to_save)
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
                       
                else:
                    logging.error("Identity auth: %s", identity_data)
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
                    OkraLinkedUser.objects.update(**self._to_save)
                    self._LOGGER.info(f"New user created: {self._to_save}")
                    return {"credit_limit": credit_limit}
                else:
                    self._LOGGER.error("Confidence not good enough")
            else:
                self._LOGGER.error("Failed to get income")
                self._LOGGER.error(income_data)
            return {}
        except Exception as e:
            self._LOGGER.error(f"Failed to get income from OKRA(API): {e}")
            self._send_mail("Failed to get income:", error=e)
        return None


    def get_nuban_balances(self, customer):
        okra_linked_user = OkraLinkedUser.objects.get(customer_id=customer)
        accounts_response = requests.post(url=self._ACCOUNT_CUSTOMER_URL, json={"customer":customer}, headers= self._HEADERS).json()
        if accounts_response["status"] == "success":
            details = accounts_response
            accounts = details["account"]
            nuban, balance = self._get_account_numbers(accounts)
            okra_linked_user.balance_ids = balance
            okra_linked_user.income_accounts = nuban
            okra_linked_user.save()
            return True
        else:
            return False
        
    
    def get_balance(self, balance_id):
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
        self._to_save["income_banks"] = banks
        return avg_income, credit_limit
    
    
    def _get_account_numbers(self, accounts):
            nuban = ':'.join(account["nuban"] for account in accounts)
            balance = ':'.join(account["balance"] for account in accounts)
            return nuban, balance
            

    def _initiate_payment(self, acc_deb, acc_cred, amount):
        amount = int(amount * 100) # convert amount to KOBO
        payload = {
            "account_to_debit" : acc_deb,
            "account_to_credit" : acc_cred,
            "amount" : amount
        }
        payment_response = requests.post(url=self._INITIATE_PAYMENT_URL, json=payload, headers=self._HEADERS).json()
        status = payment_response["status"]
        ref = payment_response["data"]["payment"]["ref"]

        # check for the satus
        if status in ["pending", "initiated"]:
            status = "pending"
        return {"status": status, "ref": ref}
    

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

