from pprint import pprint
import requests
import os
from dotenv import load_dotenv
# curl - X POST https: // api.okra.ng/v2/products/kyc/bvn-verify

load_dotenv()

secret = os.getenv("OKRA_SECRET")
API_KEY = os.getenv("OKRA_PUBLIC")

BASE_URL = "https://api.okra.ng/v2/products/"
enpoint = "kyc/bvn-verify"

headers = {
    "accept": "application/json; charset=utf-8",
    "content-type": "application/json",
    "authorization": f"Bearer {secret}"
}

data = {
    'bvn':"22334507774"
}

test = requests.post(url=BASE_URL+enpoint, headers=headers, json=data)
pprint(test.json(), indent=4)


