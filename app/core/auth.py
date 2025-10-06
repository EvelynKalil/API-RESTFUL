from fastapi import Header, HTTPException, status
from app.core.config import settings
from app.core.constants import API_KEY_HEADER, ERROR_DETAIL_UNAUTHORIZED

def verify_api_key(x_api_key: str = Header(default=None, alias=API_KEY_HEADER)):
    """Verify that the request includes a valid API key in the headers."""
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_DETAIL_UNAUTHORIZED,
        )
