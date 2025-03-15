from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    model_config = {
        "extra": "allow",
        "env_file": ".env",
        "case_sensitive": False
    }

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "workflow_automation"
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    DEBUG: bool = True
    
    # New settings
    GEMINI_API_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings() 
print(settings.model_dump())