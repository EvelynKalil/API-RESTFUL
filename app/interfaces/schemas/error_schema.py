from typing import Any, Dict
from pydantic import BaseModel, Field
from app.core.constants import STATUS_ERROR


class ErrorResponse(BaseModel):
    """Standard error response returned by all endpoints."""

    status: str = Field(
        STATUS_ERROR,
        example=STATUS_ERROR,
        description="Response status indicating an error occurred.",
    )

    error: Dict[str, Any] = Field(
        ...,
        example={
            "code": "INVALID_SENDER",
            "message": "Invalid sender value",
            "details": "Allowed values are 'user' or 'system'.",
        },
        description=(
            "Dictionary containing error details: "
            "'code' (error identifier), 'message' (human-readable text), "
            "and optional 'details' with additional information."
        ),
    )
