from pprint import pprint

import requests
AUTH = {'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNzU0OTUxMywiaWF0IjoxNjgxNTQ5NTEzLCJqdGkiOiIzNTg3NmExZTM1NmQ0ZTg1OGEzNzc3YWE1NGViMGYwNyIsInVzZXJfaWQiOjF9.Kv6VeChHgIG8C5lgvLDKFiXfgJDuJvt-2usZWQaqNsU', 'access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE3NTQ5NTEzLCJpYXQiOjE2ODE1NDk1MTMsImp0aSI6IjI5ZTQxYmQ3ZDYzOTQ5YjViMmE0ZTZkZTJjOTAxODY2IiwidXNlcl9pZCI6MX0.LIZqkEPryfgncDNrA9zFVuJIeV7FWMkCSC4fe1u2sFk'}

headers = {
    "accept": "application/json; charset=utf-8",
    "authorization": f"Bearer {AUTH['access']}"
}

url = "http://localhost:8000/core/details/"

response = requests.get(url, headers=headers)
pprint(response.json(), indent=4)

