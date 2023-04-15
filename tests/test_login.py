import requests
url = "http://localhost:8000/account/login/"
# url = "http://localhost:8000/api/token/"

data = {
    "username":"michaellyon",
    "password":"1234rewqasdf"
}

AUTH = {'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNzU0OTUxMywiaWF0IjoxNjgxNTQ5NTEzLCJqdGkiOiIzNTg3NmExZTM1NmQ0ZTg1OGEzNzc3YWE1NGViMGYwNyIsInVzZXJfaWQiOjF9.Kv6VeChHgIG8C5lgvLDKFiXfgJDuJvt-2usZWQaqNsU', 'access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE3NTQ5NTEzLCJpYXQiOjE2ODE1NDk1MTMsImp0aSI6IjI5ZTQxYmQ3ZDYzOTQ5YjViMmE0ZTZkZTJjOTAxODY2IiwidXNlcl9pZCI6MX0.LIZqkEPryfgncDNrA9zFVuJIeV7FWMkCSC4fe1u2sFk'}

response = requests.post(url=url, json=data)
print(response.json())
