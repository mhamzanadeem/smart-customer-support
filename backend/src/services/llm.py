from openai import AsyncOpenAI

from src.config import get_settings


class LLMService:
    def __init__(self):
        self.settings = get_settings()

        provider = self.settings.llm_provider.lower()

        if provider == "openai":
            if not self.settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required.")

            self.client = AsyncOpenAI(
                api_key=self.settings.openai_api_key
            )

            self.model = self.settings.openai_model

        elif provider == "groq":
            if not self.settings.groq_api_key:
                raise ValueError("GROQ_API_KEY is required.")

            self.client = AsyncOpenAI(
                api_key=self.settings.groq_api_key,
                base_url="https://api.groq.com/openai/v1",
            )

            self.model = self.settings.groq_model

        else:
            raise ValueError(
                f"Unsupported LLM_PROVIDER: {provider}"
            )

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content or ""