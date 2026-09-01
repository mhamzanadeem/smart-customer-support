from functools import lru_cache

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    # -------------------------
    # OpenAI
    # -------------------------

    openai_api_key: str | None = None

    openai_model: str = "gpt-5.6-luna"


    # -------------------------
    # Groq
    # -------------------------

    groq_api_key: str | None = None

    groq_model: str = (
        "llama-3.3-70b-versatile"
    )


    # -------------------------
    # Provider
    # -------------------------

    provider: str = "openai"


    # -------------------------
    # Supabase
    # -------------------------

    supabase_url: str

    supabase_service_role_key: str

    supabase_db_url: str | None = None


    # -------------------------
    # Embeddings
    # -------------------------

    embedding_model: str = (
        "text-embedding-3-small"
    )

    embedding_dim: int = 1536


    # -------------------------
    # RAG
    # -------------------------

    top_k: int = 5

    similarity_threshold: float = 0.70


    # -------------------------
    # Checkpoint
    # -------------------------

    checkpoint_db_url: str | None = None


    # -------------------------
    # Application
    # -------------------------

    app_env: str = "development"

    log_level: str = "INFO"


    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


    def validate_keys(self) -> None:

        if (
            self.provider.lower() == "openai"
            and not self.openai_api_key
        ):
            raise ValueError(
                "OPENAI_API_KEY is required "
                "when PROVIDER=openai"
            )


        if (
            self.provider.lower() == "groq"
            and not self.groq_api_key
        ):
            raise ValueError(
                "GROQ_API_KEY is required "
                "when PROVIDER=groq"
            )


        if (
            not self.supabase_url
            or not self.supabase_service_role_key
        ):
            raise ValueError(
                "SUPABASE_URL and "
                "SUPABASE_SERVICE_ROLE_KEY "
                "are required"
            )


@lru_cache
def get_settings() -> Settings:

    settings = Settings()

    settings.validate_keys()

    return settings