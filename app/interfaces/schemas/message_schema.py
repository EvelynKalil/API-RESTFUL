from datetime import datetime
from typing import Any, Dict, Optional
from enum import Enum
from pydantic import BaseModel, Field

class MessageIn(BaseModel):
    """Input model for creating a message."""
    message_id: str = Field(..., example="ms001", description="Unique identifier of the message")
    session_id: str = Field(..., example="sn001", description="Chat session identifier")
    content: str = Field(..., example="Hello world!", description="Message text content")
    sender: str = Field(..., example="user", description="Who sent the message (user or system)")


class MetadataOut(BaseModel):
    """Metadata information automatically generated for a message."""
    word_count: int = Field(..., example=2)
    character_count: int = Field(..., example=12)
    processed_at: str = Field(..., example="2025-10-06T00:48:55.204Z")


class MessageOut(BaseModel):
    """Output model for a stored message."""
    message_id: str = Field(..., example="ms001")
    session_id: str = Field(..., example="sn001")
    content: str = Field(..., example="Hello world!")
    timestamp: datetime = Field(..., example="2025-10-06T00:48:55.204Z")
    sender: str = Field(..., example="user")
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        example={
            "word_count": 2,
            "character_count": 12,
            "processed_at": "2025-10-06T00:48:55.204Z",
        },
        description="Automatically generated metadata about the message content",
    )
