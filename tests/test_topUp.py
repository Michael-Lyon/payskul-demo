import requests
BASE = "http://localhost:8000/"
TOP_WALLET_URL = "core/top_wallet/"
AUTH = {'access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwNzYwNjM2LCJpYXQiOjE2ODQ3NjA2MzYsImp0aSI6IjM5YmU1NTdhNTU0NjRjNGM4ZDI5Y2YyZTYzMjIzMWNkIiwidXNlcl9pZCI6MX0.r4Qj3Zz_pIGnB5tCGU53Doc0kszjTAM9OKS99VDpnws',
        'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMDc2MDYzNiwiaWF0IjoxNjg0NzYwNjM2LCJqdGkiOiI2Y2FmYmE4NjY4ZjY0ZGFlYjM1ZWY5MWZkMTliZTVmOCIsInVzZXJfaWQiOjF9.8ev1VTLVGIEm29q5eYGBHYzMtYMJItU6xDr7X0PaMVU'}

headers = {
    "accept": "application/json; charset=utf-8",
    "authorization": f"Bearer {AUTH['access']}"
}


wallet_data = {
    'id': 3,
    'amount': 100_000,
    'pin': "1234rewqasdf"
}

top_wallet_response = requests.post(url=BASE+TOP_WALLET_URL, json=wallet_data, headers=headers)
print(top_wallet_response.json())
