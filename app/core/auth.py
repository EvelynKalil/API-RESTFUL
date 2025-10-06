from fastapi import Header, HTTPException, status
from app.core.config import settings

def verify_api_key(x_api_key: str = Header(default=None)):
    """Verify that the request includes a valid API key in the headers."""
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )
