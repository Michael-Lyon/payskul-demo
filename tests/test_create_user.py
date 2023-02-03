import requests
BASE = "http://localhost:8000/"
ENDPOINT = "account/create-user/"

data = {
    "fullname": "Benny John Kosi",
    "email": "Kenny@1234.com",
    "phone_number":"1234567890",
    "password": "123456",
    "confirm_password": "123456",
}


user_response = requests.post(url=BASE+ENDPOINT, json=data)
print(user_response.json())