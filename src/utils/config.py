# Configuration (Environment variables)
from pydantic_settings import BaseSettings
from src.utils.logging import setup_logging

# Configuration du logging
logger = setup_logging()

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./observatoire.db"

    # API
    api_title: str = "Observatoire Immobilier API"
    api_version: str = "1.0.0"

    # Security
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Scraping
    scraping_delay: float = 2.0
    max_retries: int = 3

    class Config:
        env_file = ".env"

settings = Settings()