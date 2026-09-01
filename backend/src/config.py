from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    app_name: str = "Smart Customer Support"
    app_env: str = "development"
    log_level: str = "INFO"
    debug: bool = False

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

    cors_origins: str = "*"

    llm_timeout: int = 30
    mongo_timeout: int = 10
    request_timeout: int = 60

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        raw = self.cors_origins.strip()
        if raw == "*":
            return ["*"]
        return [
            origin.strip()
            for origin in raw.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    key = settings.openai_api_key
    if key:
        masked = key[:4] + "..." + key[-4:]
        print(f"[CONFIG] OPENAI_API_KEY loaded: True (key: {masked})")
    else:
        print("[CONFIG] OPENAI_API_KEY loaded: False (key is None or empty)")
    print(f"[CONFIG] debug={settings.debug}, llm_provider={settings.llm_provider}, model={settings.openai_model}")
    return settings
