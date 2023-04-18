import requests
url = "https://payskul-demo.up.railway.app/account/login/"
# url = "http://localhost:9000/account/login/"
# url = "http://localhost:8000/account/login/"
# url = "http://localhost:8000/api/token/"

data = {
    "username":"michaellyon",
    "password":"1234rewqasdf"
}
# data = {
#     "username":"TesDem8e2",
#     "password":"11234dd56"
# }


AUTH = {'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNzc1MTkxMSwiaWF0IjoxNjgxNzUxOTExLCJqdGkiOiJiZjU5YjE3Y2Q5OTE0MmE4OWVhZjU2ZDFiMzQ1ZDk2YiIsInVzZXJfaWQiOjExM30.OWwzsBkXydBJ25U9Fl5II2m3puuksy_7bNJEi1RjRZU', 'access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE3NzUxOTExLCJpYXQiOjE2ODE3NTE5MTEsImp0aSI6ImFhOWNmODRmODcyNjQyZWQ5N2NlMmEyNmNhZWQ2NjYwIiwidXNlcl9pZCI6MTEzfQ.5SPfAxQm5C0iwPFhFX9QqaszXGQieieWu8jRJ6-s6Zk'}

response = requests.post(url=url, json=data)
print(response.json())
