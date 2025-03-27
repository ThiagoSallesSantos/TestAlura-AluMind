from src.model.model import get_model

from src.model.prompt import get_prompt_classify_feedback

from src.schemas.schemas import RatedFeedbackSchema, UserFeedbackSchema

feedback = UserFeedbackSchema(
    id="4042f20a-45f4-4647-8050-139ac16f610b",
    feedback="Gosto muito de usar o Alumind! Está me ajudando bastante em relação a alguns problemas que tenho. Só quer ia que houvesse uma forma mais fácil de eu mesmo realizar a edição do meu perfil dentro da minha conta"
)

prompt = get_prompt_classify_feedback()

model = get_model(model="ollama")
model_structed = model.with_structured_output(RatedFeedbackSchema)

chain = prompt | model_structed
response = chain.invoke(feedback.model_dump())

print(response)
