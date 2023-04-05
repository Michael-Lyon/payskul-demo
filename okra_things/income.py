

from pprint import pprint
import requests
from dotenv import load_dotenv
import os

load_dotenv()

secret = os.getenv("OKRA_SECRET")
API_KEY = os.getenv("OKRA_PUBLIC")
url = "https://api.okra.ng/v2/income/getAll"

payload = {
    "customer": "63f87b51f6e7da0080f223fe"
}
headers = {
    "accept": "application/json; charset=utf-8",
    "content-type": "application/json",
    "authorization": f"Bearer {secret}"
}

response = requests.post(url,  headers=headers)

pprint(response.json(), indent=4)
