import requests

json = {
    "id": "4042f20a-45f4-4647-8050-139ac16f610a",
    "feedback": "Gosto muito de usar o Alumind! Está me ajudando bastante em relação a alguns problemas que tenho. Só quer ia que houvesse uma forma mais fácil de eu mesmo realizar a edição do meu perfil dentro da minha conta",
    # "options": {
    #     "model": "",
    #     "api_key": ""
    # }
}

response = requests.post(
    url=f"http://localhost:9876/feedbacks/",
    json=json
)

print(response.status_code)
print(response.json())
