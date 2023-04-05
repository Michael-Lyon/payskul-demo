from pprint import pprint
import requests
from dotenv import load_dotenv
import os

load_dotenv()

secret = os.getenv("OKRA_SECRET")
API_KEY = os.getenv("OKRA_PUBLIC")
url = "https://api.okra.ng/v2/sandbox/sandbox/customers/generate"

payload = [
    {
        "name": "Asomugha Michaelpp Chinonso",
        "bank": "5d6fe57a4099cc4b210bbeb2",
        "username": "pygo1111d",
        "password": "compu6345",
        "type": "ind",
    },
   
]
headers = {
    "accept": "application/json; charset=utf-8",
    "content-type": "application/json",
    "authorization": f"Bearer {secret}"
}

# response = requests.post(url, json=payload, headers=headers)
# # # 
# pprint(response.json()['data']['customers'], indent=4)

print("List of customers")


url = "https://api.okra.ng/v2/sandbox/customers/list"

response = requests.post(url, headers=headers)

pprint(response.json()['data'], indent=4)


