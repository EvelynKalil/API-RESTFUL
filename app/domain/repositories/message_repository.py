from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.message import Message

class MessageRepository(ABC):
    @abstractmethod # pragma: no cover
    def save(self, message: Message):
        """Persist a message and return it (may include DB-generated fields)."""
        raise NotImplementedError
    
    @abstractmethod # pragma: no cover
    def get_by_session(self, session_id: str, limit: int, offset: int, sender: Optional[str] = None) -> List[Message]:
        """Fetch messages for a session with optional sender filter and pagination."""
        raise NotImplementedError