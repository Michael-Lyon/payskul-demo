import requests
from pprint import pprint
BASE = "http://localhost:8000/"
ENDPOINT = "account/create-user/"

data = {
    "fullname": "lilola Demo",
    "email": "pygod.dev@mail.com",
    "phone_number":"11234567811190",
    "password": "11234dd56",
    "confirm_password": "11234dd56"
}


user_response = requests.Session().post(url=BASE+ENDPOINT, data=data)
pprint(user_response.json(), indent=4)