from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Smart Customer Support"
    app_env: str = "development"
    log_level: str = "INFO"

    mongodb_uri: str
    mongodb_database: str = "smart_customer_support"

    llm_provider: str = "openai"

    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    groq_api_key: str | None = None
    groq_model: str = "llama-3.3-70b-versatile"

    embedding_model: str = "text-embedding-3-small"
    embedding_dimension: int = 1536

    rag_top_k: int = 5
    rag_similarity_threshold: float = 0.70

    mcp_enabled: bool = True
    mcp_server_url: str = "http://localhost:8001/mcp"

    cors_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()