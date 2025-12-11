"""
Application Settings and Configuration
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./lingua_latina.db")
    DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "False").lower() == "true"
    
    # Application settings
    APP_NAME: str = "Lingua Latina Viva"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # User settings
    DEFAULT_USER_NAME: str = "Discipulus"
    
    # Performance settings
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "10"))
    DATABASE_MAX_OVERFLOW: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "20"))
    
    class Config:
        env_file = ".env"


settings = Settings()