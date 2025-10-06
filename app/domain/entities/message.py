from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict

@dataclass
class Message:
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender : str
    metadata: Optional[Dict] = None