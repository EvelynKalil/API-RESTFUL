from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database configuration
    DATABASE_URL: str = "sqlite:///./chat.db"

    # API settings
    API_PREFIX: str = "/api"
    API_VERSION: str = "1.0.0"
    PROJECT_NAME: str = "Chat Messages API"
    DESCRIPTION: str = "RESTful API for chat message processing"
    API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
