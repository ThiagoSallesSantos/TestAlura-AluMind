import requests

json = {
    "email": "test@test.com",
    "name": "test"
}

response = requests.post(
    url=f"http://localhost:9876/email/",
    json=json
)

print(response.status_code)
print(response.json())
