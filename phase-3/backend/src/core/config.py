"""Environment configuration for Phase-3 backend."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database - defaults to SQLite for local development, same as Phase-2
    database_url: str = "sqlite:///./phase3_local.db"

    # JWT - for compatibility with Phase-2 auth system
    jwt_secret: str = "change-this-secret-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    # Server
    host: str = "0.0.0.0"
    port: int = 8000  # Different port from Phase-2
    debug: bool = False

    # CORS - same as Phase-2
    cors_origins: str = "http://localhost:3000"

    # OpenAI settings for AI chatbot
    openai_api_key: str = ""
    openai_model: str = "gpt-4"
    agent_timeout: int = 30
    conversation_history_limit: int = 50

    # Better Auth (from Phase II compatibility)
    better_auth_secret: str = "mock-testing-secret-123"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()