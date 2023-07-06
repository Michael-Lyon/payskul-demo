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



def generate_random_credit():
    """Takes no arguments and return a random credit."""

    # Set the minimum and maximum credit limit values
    min_credit_limit = 20_000
    max_credit_limit = 200_000

    return random.randint(min_credit_limit, max_credit_limit)



def validate_national_id(national_id: str) -> bool:
    """Validates a national identity number.

    Args:
        national_id: The national identity number to be validated.

    Returns:
        True if the national identity number is valid, False otherwise.
    """
    if not national_id or len(national_id) != 11:
        return False
    return True
    # # Extract the first 12 digits of the national identity number
    # first_12_digits = national_id[:12]

    # # Calculate the 13th digit using a modulus 11 check
    # check_digit = int(national_id[12])
    # sum_ = sum(int(d) * (13 - i) for i, d in enumerate(first_12_digits))
    # calculated_check_digit = (11 - sum_ % 11) % 11

    # # Check if the calculated check digit matches the original check digit
    # return check_digit == calculated_check_digit


def validate_bvn(bvn: str) -> bool:
    """Validates a bank verification number.

    Args:
        bvn: The bank verification number to be validated.

    Returns:
        True if the bank verification number is valid, False otherwise.
    """
    if not bvn or len(bvn) != 11:
        return False
    
    return True
    # # Extract the first 10 digits of the BVN
    # first_10_digits = bvn[:10]

    # # Calculate the 11th digit using a modulus 11 check
    # check_digit = int(bvn[10])
    # sum_ = sum(int(d) * (11 - i) for i, d in enumerate(first_10_digits))
    # calculated_check_digit = (11 - sum_ % 11) % 11

    # # Check if the calculated check digit matches the original check digit
    # return check_digit == calculated_check_digit



def get_natinal_id():

    # Generate the first 12 digits of the national identity number
    first_12_digits = "01011998" + "".join([str(random.randint(0, 9)) for _ in range(4)])

    # Calculate the check digit
    sum_ = sum(int(d) * (13 - i) for i, d in enumerate(first_12_digits))
    calculated_check_digit = (11 - sum_ % 11) % 11

    # Generate the national identity number
    return first_12_digits + str(calculated_check_digit)


def get_bvn():

    # Generate the first 10 digits of the BVN
    first_10_digits = "01011998" + "".join([str(random.randint(0, 9)) for _ in range(2)])

    # Calculate the check digit
    sum_ = sum(int(d) * (11 - i) for i, d in enumerate(first_10_digits))
    calculated_check_digit = (11 - sum_ % 11) % 11

    # Generate the BVN
    bvn = first_10_digits + str(calculated_check_digit)
    return bvn






class OkraSetup:
    _BASE = "https://api.okra.ng/v2/sandbox/"
    _LOGGER = logging.getLogger('okra_validator')

    # INCOME URLS
    _PROCESS_INCOME_URL = _BASE + "income/process"
    _INCOME_CUSTOMER_URLS = _BASE + "income/getByCustomer"
    _INCOME_ID_URL = _BASE + "income/getById"

    _GET_ACCOUNT_CUSTOMER = _BASE + "accounts/getByCustomer"

    # IDENTITY URLS
    _IDENTITY_URL =  _BASE + "identity/getByCustomer"

    # BANK URLS
    _BANKS_LIST_URL = _BASE + "banks/list"

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
        accounts = ':'.join(stream["account"] for stream in streams)
        banks = ':'.join(stream["bank"] for stream in streams)
        total_income = sum(stream["avg_monthly_income"] for stream in streams)
        avg_income = total_income / len(streams)
        credit_limit = avg_income * (87.5 / 100)
        self._to_save["income_accounts"] = accounts
        self._to_save["income_banks"] = banks
        return avg_income, credit_limit
    

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

