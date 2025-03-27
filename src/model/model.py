from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.language_models.llms import BaseLLM

from functools import partial

from typing import Dict

dict_models_choices: Dict[str, BaseLLM] = {
    "ollama": partial(ChatOllama, model="llama3.2", num_ctx=8192, keep_alive=0),
    "openai": partial(ChatOpenAI, model="gpt-4o"),
    "gemini": partial(ChatGoogleGenerativeAI, model="gemini-1.5-flash")
}

def get_model(model: str, **kwargs) -> BaseLLM:
    return dict_models_choices[model](**kwargs)
