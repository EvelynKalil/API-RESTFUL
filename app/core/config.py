import os 

class Settings:
    # Database configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./chat.db")

    # API settings
    API_PREFIX: str = "/api"
    API_VERSION: str = "1.0.0"
    PROJECT_NAME: str = "Chat Messages API"
    DESCRIPTION: str = "RESTful API for chat message processing"

settings = Settings()