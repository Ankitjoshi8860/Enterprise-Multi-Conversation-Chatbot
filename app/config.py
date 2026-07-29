"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the API and its integrations."""

    app_name: str = "MediAssist AI"
    app_env: str = "development"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.0-flash"
    database_path: str = "chatbot.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings object for dependency injection."""

    return Settings()
