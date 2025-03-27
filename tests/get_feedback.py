import requests

feedback_id = "4042f20a-45f4-4647-8050-139ac16f610b"

response = requests.get(
    url=f"http://localhost:9876/feedbacks/{feedback_id}",
)

print(response.status_code)
print(response.json())
