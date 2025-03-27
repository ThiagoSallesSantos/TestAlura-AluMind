import requests

json = {
    "email": "",
    "name": ""
}

response = requests.post(
    url=f"http://localhost:9876/email/",
    json=json
)

print(response.status_code)
print(response.json())
