import os
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True

    # Database Configuration
    DB_PATH: str = "data/processed/sales.db"

    # LLM Configuration
    LLM_PROVIDER: Literal["openai", "mock"] = "mock"
    OPENAI_API_KEY: str | None = None
    MODEL_NAME: str = "gpt-3.5-turbo"

    # Safety Configuration
    ALLOW_DANGEROUS_QUERIES: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def database_url(self) -> str:
        # Ensure the path is absolute or relative to the project root
        return f"sqlite:///{self.DB_PATH}"


settings = Settings()
