from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path

class Settings(BaseSettings):
    # API Configurations
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "PDF Chat API"

    # Security
    GEMINI_API_KEY: str

    # Storage
    UPLOAD_FOLDER: str = str(Path("storage/pdfs").absolute())
    MAX_FILE_SIZE: int = 10* 1024 * 1024 # 10MB

    # Application Settings
    DEBUG: bool = False

    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    CACHE_TTL: int = 3600  # Cache expiry in seconds (1 hour)

    class Config:
        env_file = ".env"
        case_sensitive = True

# Type definition for API response
class HTTPError(BaseModel):
    detail: str

# Create a cached instance of settings
@lru_cache
def get_settings() -> Settings:
    return Settings()