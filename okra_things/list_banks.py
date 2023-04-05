from pprint import pprint
import os
import requests
from .base import GET_BANK_URL as url
from dotenv import load_dotenv

load_dotenv()
secret = os.getenv("OKRA_SECRET")
API_KEY = os.getenv("OKRA_PUBLIC")

HEADERS = {
    "accept": "application/json; charset=utf-8",
    "content-type": "application/json",
    "authorization": f"Bearer {secret}"
}


def bank_list():
    try:
        response = requests.get(url, headers=HEADERS )
        data = response.json()['data']['banks']
        if not data:
            return []
        return [ {"id": bank['id'], "name":bank['name']} for bank in data]
    except Exception as e:
        print(e)
        return []
    




if __name__ == "__main__":
    pprint(bank_list())