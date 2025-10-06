from typing import Any, Dict
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error response returned by all endpoints."""

    status: str = Field(
        "error",
        example="error",
        description="Response status indicating an error occurred",
    )

    error: Dict[str, Any] = Field(
        ...,
        example={
            "code": "INVALID_SENDER",
            "message": "Invalid sender value",
            "details": "Allowed values are 'user' or 'system'",
        },
        description=(
            "Dictionary containing error details: "
            "'code' (error identifier), 'message' (human-readable text), "
            "and optional 'details' with additional information."
        ),
    )