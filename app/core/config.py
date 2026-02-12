"""
Application configuration settings
"""
import os
from typing import Optional, List

try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback for older pydantic versions
    from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_TITLE: str = "GitHub Portfolio API"
    API_DESCRIPTION: str = "An amazing API to showcase your GitHub profile and repositories"
    API_VERSION: str = "2.0.0"
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # GitHub API Settings
    GITHUB_API_BASE: str = "https://api.github.com"
    GITHUB_TOKEN: Optional[str] = None
    GITHUB_API_TIMEOUT: float = 10.0
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Override with environment variable if set
        if os.getenv("GITHUB_TOKEN"):
            self.GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


# Create settings instance
settings = Settings()

