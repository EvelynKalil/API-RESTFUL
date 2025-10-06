from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    DATABASE_URL: str = "sqlite:///./data/chat.db"

    API_PREFIX: str = "/api"
    API_VERSION: str = "1.0.0"
    PROJECT_NAME: str = "Chat Messages API"
    DESCRIPTION: str = "RESTful API for chat message processing"

    API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()