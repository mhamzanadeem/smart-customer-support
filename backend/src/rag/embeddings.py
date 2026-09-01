from openai import AsyncOpenAI

from src.config import get_settings


class EmbeddingService:
    def __init__(self):
        settings = get_settings()

        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is required for embeddings."
            )

        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            timeout=settings.llm_timeout,
        )

        self.model = settings.embedding_model

    async def embed(self, text: str) -> list[float]:

        response = await self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding
