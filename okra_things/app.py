from dotenv import load_dotenv
import os

load_dotenv()

import requests
from pprint import pprint
secret = os.getenv("OKRA_SECRET")
API_KEY = os.getenv("OKRA_PUBLIC")

BASE_URL = "https://api.okra.ng/v2/sandbox/"

headers = {
    "accept": "application/json; charset=utf-8",
    "content-type": "application/json",
    "authorization": f"Bearer {secret}"
}

bank_list_endpoint = "banks/list"
generate_endpoint = "customers/generate"

data = {
    "number":10,
    "create":False
}


test = requests.get(url=BASE_URL+bank_list_endpoint, headers=headers,)

# pprint(test.json(), indent=4)

if "success" == test.json()['status']:
    print(test.json()['message'])
    for bank in test.json()['data']['banks']:
        print(bank['name'], bank['id'])
        print()


# 63f87b51f6e7da0080f223fe
