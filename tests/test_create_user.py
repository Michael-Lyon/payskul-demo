import requests
from pprint import pprint
import json
import time
# BASE = "https://payskul-demo.up.railway.app/"
BASE = "http://localhost:8000/"
ENDPOINT = "account/create-user/"

payload = {
    "fullname": "Jennyke RUmith",
    "email": "pygod.dev@mail.com",
    "phone_number":"11234567811190",
    "password": "11234dd56",
    "confirm_password": "11234dd56"
}

user_response = requests.post(url=BASE+ENDPOINT, data=payload)
pprint(user_response.json(), indent=4)