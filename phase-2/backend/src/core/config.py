"""Environment configuration for the backend."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database - defaults to SQLite for local development
    database_url: str = "sqlite:///./local.db"

    # JWT
    jwt_secret: str = "change-this-secret-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # CORS - required field with safe defaults for development
    cors_origins: str = "http://localhost:3000,http://localhost:3001,https://*.vercel.app,https://*.netlify.app,http://127.0.0.1:3000,http://127.0.0.1:3001,https://phase2-evolution-of-todo.vercel.app"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
