
import requests
url = "https://payskul-demo.up.railway.app/account/email-verify/"
# url = "http://localhost:8000/account/login/"
# url = "http://localhost:8000/api/token/"

data = {
    "id": 113,
    "code": "8e5adb",
}


response = requests.post(url=url, json=data)
print(response.json())