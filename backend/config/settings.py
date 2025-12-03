import os
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_VERSION: str = "v1"
    DEBUG: bool = True
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    
    # Database Configuration
    DATABASE_TYPE: Literal["sqlite", "postgresql"] = "sqlite"
    
    # SQLite (Development)
    SQLITE_DB_PATH: str = "data/processed/sales.db"
    
    # PostgreSQL (Production)
    POSTGRES_USER: str = "llmdbms"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "llmdbms"
    
    # JWT Configuration
    JWT_SECRET_KEY: str = "dev-secret-key-change-in-production-use-env-variable"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # LLM Configuration
    LLM_PROVIDER: Literal["openai", "anthropic", "local", "mock"] = "mock"
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    MODEL_NAME: str = "gpt-3.5-turbo"
    LLM_TEMPERATURE: float = 0.0
    LLM_MAX_TOKENS: int = 500
    
    # LLM Caching
    ENABLE_LLM_CACHE: bool = True
    CACHE_TTL_SECONDS: int = 3600  # 1 hour
    
    # Redis Configuration (for caching)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    
    # Safety Configuration
    SAFETY_MODE: Literal["strict", "moderate", "permissive"] = "strict"
    ALLOW_DANGEROUS_QUERIES: bool = False
    REQUIRE_QUERY_APPROVAL: bool = False  # Require manual approval for certain queries
    
    # Observability
    LOG_LEVEL: str = "INFO"
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    # Vector Store (Semantic Search)
    ENABLE_SEMANTIC_SEARCH: bool = False
    VECTOR_STORE_TYPE: Literal["chroma", "faiss", "none"] = "none"
    CHROMA_PERSIST_DIR: str = "data/vector_store"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )
    
    @property
    def database_url(self) -> str:
        """Get database URL based on configuration."""
        if self.DATABASE_TYPE == "postgresql":
            return (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )
        else:
            # SQLite
            return f"sqlite:///{self.SQLITE_DB_PATH}"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT == "development"


settings = Settings()

