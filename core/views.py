import json

# The JSON payload as a dictionary
json_payload = {
    "method": "AUTH",
    "callback_type": "AUTH",
    "callback_code": "AUTH_SUCCESS",
    "type": "CALLBACK",
    "code": "AUTH_SUCCESS",
    "callbackURL": "https://payskul-demo.up.railway.app/core/webhook/",
    "env": "production-sandbox",
    "status": "is_success",
    "started_at": "2023-07-18T17:06:48.763Z",
    "ended_at": "2023-07-18T17:07:56.430Z",
    "message": "Successfully fetched auth",
    "options": {},
    "meta": {},
    "bankName": "Union Bank of Nigeria",
    "bankType": "5d6fe57a4099cc4b210bbeb9",
    "bankId": "5d6fe57a4099cc4b210bbeb9",
    "bankSlug": "union-bank-of-nigeria",
    "record": "64b6c6a85d9158003b90e10f",
    "recordId": "64b6c6a85d9158003b90e10f",
    "callback_url": "https://api.okra.ng/v2/callback?record=64b6c6a85d9158003b90e10f&method=AUTH",
    "customerId": "647b92b01519bc002f0c00b9",
    "country": "NG",
    "extras": {},
    "auth": {}
}

# Convert the dictionary to a JSON string
json_string = json.dumps(json_payload)

# Now, json_string contains the JSON object as a string.
print(json_string)
