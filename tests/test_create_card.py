import requests
BASE = "http://localhost:8000/apiv1/"
LOGIN_URL = "account/login/"
CREATE_CARD_URL = "core/card/"

session = requests.Session()
headers = {'Authorization': 'Bearer ee330f9bb89d142778bb844bb7712ce88df38231'}
login_data = {
    "username": "pygodtest",
    "password": "1234rewqasdf"
}
login_response = requests.post(url=BASE+LOGIN_URL, json=login_data, headers=headers)
print(login_response.json())

id = int(login_response.json()['data']['id'])

card_data = {
    "user": id,
    "name":"Pygod .M. PyGod",
    "number": "123222256789",
    "cvv":"120"
}
card_create_response = requests.post(url=BASE+CREATE_CARD_URL, json=card_data, headers=headers)
print(card_create_response.json())

