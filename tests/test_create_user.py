import requests
from pprint import pprint
BASE = "https://payskul-demo.up.railway.app/"
ENDPOINT = "account/create-user/"

data = {
    "fullname": "Aeaddl Pdygod Kodsi",
    "email": "real_1pygod123@icloud.com",
    "phone_number":"11234567890",
    "password": "11234dd56",
    "confirm_password": "11234dd56",
}


user_response = requests.post(url=BASE+ENDPOINT, json=data)
pprint(user_response.json(), indent=4)