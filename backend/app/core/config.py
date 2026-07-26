from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # =========================
    # App
    # =========================
    app_name: str = "LexiMind AI"
    app_version: str = "0.1.0"
    debug: bool = False

    # =========================
    # Security
    # =========================
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # =========================
    # Database
    # =========================
    database_url: str

    # =========================
    # AI
    # =========================
    openai_api_key: str = ""

    # =========================
    # Settings
    # =========================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    GROQ_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    




@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.
    """
    return Settings()


settings = get_settings()   