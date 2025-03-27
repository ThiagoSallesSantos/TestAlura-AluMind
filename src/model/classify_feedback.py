from langchain_core.language_models.llms import BaseLLM

from langchain_core.prompts import ChatPromptTemplate

from src.schemas.schemas import UserFeedbackSchema, RatedFeedbackSchema

def classify_feedback(model: BaseLLM, prompt: ChatPromptTemplate, feedback: UserFeedbackSchema) -> RatedFeedbackSchema:
    model_structed = model.with_structured_output(RatedFeedbackSchema)

    chain = prompt | model_structed
    response: RatedFeedbackSchema = chain.invoke(feedback.model_dump())

    return response