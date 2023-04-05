from dotenv import load_dotenv
import os

load_dotenv()

secret = os.getenv("OKRA_SECRET")
API_KEY = os.getenv("OKRA_PUBLIC")


GET_BANK_URL = "https://api.okra.ng/v2/sandbox/banks/list"

HEADERS = {
    "accept": "application/json; charset=utf-8",
    "content-type": "application/json",
    "authorization": f"Bearer {secret}"
}
