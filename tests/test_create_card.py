import requests
BASE = "http://localhost:8000/"
LOGIN_URL = "account/login/"
CREATE_CARD_URL = "core/card/"

session = requests.Session()
AUTH = {'access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwNzYwNjM2LCJpYXQiOjE2ODQ3NjA2MzYsImp0aSI6IjM5YmU1NTdhNTU0NjRjNGM4ZDI5Y2YyZTYzMjIzMWNkIiwidXNlcl9pZCI6MX0.r4Qj3Zz_pIGnB5tCGU53Doc0kszjTAM9OKS99VDpnws',
           'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMDc2MDYzNiwiaWF0IjoxNjg0NzYwNjM2LCJqdGkiOiI2Y2FmYmE4NjY4ZjY0ZGFlYjM1ZWY5MWZkMTliZTVmOCIsInVzZXJfaWQiOjF9.8ev1VTLVGIEm29q5eYGBHYzMtYMJItU6xDr7X0PaMVU'}

headers = {
    "accept": "application/json; charset=utf-8",
    "authorization": f"Bearer {AUTH['access']}"
}

card_data = {
    "name":"Pygod .M7. PyGod",
    "number": "123209856780",
    "cvv":"110"
}
card_create_response = requests.get(url=BASE+CREATE_CARD_URL, json=card_data, headers=headers)
print(card_create_response.json())

