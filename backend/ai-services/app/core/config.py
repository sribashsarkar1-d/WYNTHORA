import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Wynthora AI Services - Enterprise Edition"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development" # development, testing, staging, production
    DEBUG: bool = True

    # Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "world_sim"
    
    # Connection Pooling
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 3600
    DB_POOL_PRE_PING: bool = True

    @property
    def sync_database_uri(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def async_database_uri(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    
    @property
    def redis_url(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    # Security
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION_UUID_OR_SECURE_RANDOM_STRING"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # API Keys for External Services
    WORLD_BANK_API_KEY: Optional[str] = None
    FRED_API_KEY: Optional[str] = None
    NOAA_API_KEY: Optional[str] = None
    UN_COMTRADE_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    GDELT_API_KEY: Optional[str] = None
    
    # Ingestion Settings
    MAX_RETRIES: int = 3
    RATE_LIMIT_BURST: int = 10

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore")

settings = Settings()
