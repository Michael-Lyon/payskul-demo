import requests 
local = False
BASE= "https://payskul-demo.up.railway.app/"
if local:
    BASE = "http://localhost:8000/"
LOGIN_URL = "account/login/"
APPLY_LOAN_URL = "core/apply_loan/"
TOP_WALLET_URL = "core/top_wallet/"


session = requests.Session()
headers = {'access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwNzYwNjM2LCJpYXQiOjE2ODQ3NjA2MzYsImp0aSI6IjM5YmU1NTdhNTU0NjRjNGM4ZDI5Y2YyZTYzMjIzMWNkIiwidXNlcl9pZCI6MX0.r4Qj3Zz_pIGnB5tCGU53Doc0kszjTAM9OKS99VDpnws',
           'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMDc2MDYzNiwiaWF0IjoxNjg0NzYwNjM2LCJqdGkiOiI2Y2FmYmE4NjY4ZjY0ZGFlYjM1ZWY5MWZkMTliZTVmOCIsInVzZXJfaWQiOjF9.8ev1VTLVGIEm29q5eYGBHYzMtYMJItU6xDr7X0PaMVU'}
login_data= {
    "username":"pygodtest",
    "password":"1234rewqasdf"
}
login_response = requests.post(url=BASE+LOGIN_URL, json=login_data, headers=headers)
print(login_response.json())



#  TEST LOAN APPLICATION
loan_data = {
    'service': 1,
    'down_payment': 9000,
    'amount_needed': 90000,
    'start_date': '2022-12-31',
    'end_date': '2023-12-31',
    'amount_to_pay_back': 110000,
    'pin': "12345"
}

apply_loan_response = requests.post(url=BASE+APPLY_LOAN_URL, json=loan_data, headers=headers)
print(apply_loan_response.json())

if apply_loan_response.json().get("message") == 'User has no/insufficient money in wallet':
    #  TOP UP WALLET
    wallet_data = {
        'pk':1,
        'amount': 100_000,
        'pin':"12345"
    }

    top_wallet_response = requests.post(url=BASE+TOP_WALLET_URL, json=wallet_data, headers=headers)
    print(top_wallet_response.json())
    
 