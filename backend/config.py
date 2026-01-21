"""
Configuration management
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # API Keys
    GEMINI_API_KEY: str
    AIRTABLE_API_KEY: str
    AIRTABLE_BASE_ID: str
    AIRTABLE_TABLE_NAME: str = "Leads"

    # API Config
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True

    # Lead Scoring Thresholds
    HIGH_SCORE_THRESHOLD: float = 80.0
    MEDIUM_SCORE_THRESHOLD: float = 60.0

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
