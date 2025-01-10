from langchain_groq import ChatGroq
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv


from utils.helper_functions import get_custom_logger

load_dotenv()
log = get_custom_logger(name=__name__)


def get_llm(model: str = "groq"):
    """Retrieve the specified language model based on the model name."""
    llm_environment_configuration = f"LLM_CONFIG_{model.upper()}"
    env_value = os.environ.get(llm_environment_configuration)

    if not env_value:
        raise ValueError(f"Invalid model name: {model}")

    model_lower = model.lower()

    if model_lower == "groq":
        model_name, api_key = env_value.split(",")
        llm = ChatGroq(api_key=api_key, model_name=model_name, temperature=0)

    elif model_lower == "ollama":
        model_name = env_value
        llm = ChatOllama(model=model_name)

    elif model_lower == "openai":
        model_name, api_key = env_value.split(",")
        llm = ChatOpenAI(
            api_key=api_key,
            model=model_name,
            temperature=0,
        )

    else:
        model_name = env_value
        llm = ChatOllama(model=model_name)

    log.info(f"Using {model} LLM: {model_name}")
    return llm
