from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]  # adjust so this points at gym-app/backend

class Settings(BaseSettings):
    DATABASE_URL: str
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ALLOWED_ORIGINS: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="forbid",
    )

settings = Settings()