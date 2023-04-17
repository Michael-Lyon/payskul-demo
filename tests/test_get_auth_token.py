import requests
# url = "https://payskul-demo.up.railway.app/account/login/"
url = "http://localhost:8000/account/get-auth-token/"
# url = "http://localhost:8000/api/token/"



AUTH = {'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNzc1MTkxMSwiaWF0IjoxNjgxNzUxOTExLCJqdGkiOiJiZjU5YjE3Y2Q5OTE0MmE4OWVhZjU2ZDFiMzQ1ZDk2YiIsInVzZXJfaWQiOjExM30.OWwzsBkXydBJ25U9Fl5II2m3puuksy_7bNJEi1RjRZU', 'access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE3NzUxOTExLCJpYXQiOjE2ODE3NTE5MTEsImp0aSI6ImFhOWNmODRmODcyNjQyZWQ5N2NlMmEyNmNhZWQ2NjYwIiwidXNlcl9pZCI6MTEzfQ.5SPfAxQm5C0iwPFhFX9QqaszXGQieieWu8jRJ6-s6Zk'}

headers = {
    "accept": "application/json; charset=utf-8",
    "authorization": f"Bearer {AUTH['access']}"
}

response = requests.get(url=url, headers=headers)
print(response.json())
