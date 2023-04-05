import requests
AUTH = {'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNjYzMjg3NSwiaWF0IjoxNjgwNjMyODc1LCJqdGkiOiI3YjZhYzFlY2RkMzU0MzEwOTE4Yjk1MTBiZjdkMjM3MyIsInVzZXJfaWQiOjF9.OLSB0Ij_1QFut2pkRaKjJnuKCB1CbKpj8pWZT85vGQQ',
        'access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2NjMyODc1LCJpYXQiOjE2ODA2MzI4NzUsImp0aSI6IjA0NDQyZGVjZDcyYjRmZTc5OTZiNjk4Y2FiMDQ4NmI5IiwidXNlcl9pZCI6MX0.Y9yqlmGkRQjyk4acoKP35HtDtwjEgxKxfjJXF9hKQlQ'}

headers = {
    "accept": "application/json; charset=utf-8",
    "authorization": f"Bearer {AUTH['access']}"
}

url = "http://localhost:8000/account/change-password/"

data = {
    "old_password": "1234rewqasdf",
    "password":"1234qwerasdf",
    "password2":"1234qwerasdf",
    
}

response = requests.put(url, headers=headers, json=data)
print(response.json())