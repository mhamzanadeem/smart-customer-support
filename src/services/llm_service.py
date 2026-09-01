from openai import AsyncOpenAI

from agents import (
    AsyncOpenAI as AgentsAsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
)

from .config import get_settings


def get_agent_model():

    settings = get_settings()


    # ----------------------------------
    # Groq
    # ----------------------------------

    if settings.provider.lower() == "groq":

        client = AgentsAsyncOpenAI(
            api_key=settings.groq_api_key,
            base_url=(
                "https://api.groq.com/openai/v1"
            ),
        )

        set_tracing_disabled(True)

        return OpenAIChatCompletionsModel(
            model=settings.groq_model,
            openai_client=client,
        )


    # ----------------------------------
    # OpenAI
    # ----------------------------------

    return settings.openai_model


def get_embeddings_client() -> AsyncOpenAI:

    settings = get_settings()

    return AsyncOpenAI(
        api_key=settings.openai_api_key
    )