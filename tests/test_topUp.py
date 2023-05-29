import requests
BASE = "http://localhost:8000/"
TOP_WALLET_URL = "core/top_wallet/"
AUTH = cc

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
