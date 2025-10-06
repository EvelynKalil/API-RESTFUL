from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict

@dataclass
class Message:
    """
    Domain entity representing a processed chat message.
    Includes unique identifiers, message content, sender details, and optional metadata.
    """
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender : str
    metadata: Optional[Dict] = None