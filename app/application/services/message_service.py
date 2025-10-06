from datetime import datetime, timezone
from typing import Optional, List

from app.core.constants import VALID_SENDERS, BANNED_WORDS
from app.domain.entities.message import Message
from app.domain.repositories.message_repository import MessageRepository
from app.core.errors import InvalidSenderError, MissingFieldError, NotFoundError


class MessageService:
    def __init__(self, repository: MessageRepository):
        self.repository = repository

    # Pipeline: Validación -> Filtrado -> Metadatos -> Guardar
    def process_and_save(self, message: Message) -> Message:
        
        self._validate_message(message)
        message.content = self._filter_content(message.content)
        message.metadata = self._add_metadata(message.content)

        return self.repository.save(message)

    def _validate_message(self, message: Message) -> None:
        if not message.message_id:
            raise MissingFieldError("message_id")
        if not message.session_id:
            raise MissingFieldError("session_id")
        if not message.sender:
            raise MissingFieldError("sender")
        if message.sender not in VALID_SENDERS:
            raise InvalidSenderError()
        if not message.timestamp:
            message.timestamp = datetime.now(timezone.utc)

    def _filter_content(self, content: str) -> str:
        lowered = content.lower()
        for word in BANNED_WORDS:
            if word in lowered:
                lowered = lowered.replace(word, "***")
        return lowered

    def _add_metadata(self, content: str) -> dict:
        return {
            "word_count": len(content.split()),
            "character_count": len(content),
            "processed_at": datetime.now(timezone.utc).isoformat()
        }

    def get_messages(self, session_id: str, limit: int, offset: int, sender: Optional[str] = None) -> List[Message]:
        if sender and sender not in VALID_SENDERS:
            raise InvalidSenderError()
        results = self.repository.get_by_session(session_id, limit, offset, sender)
        if not results:
            raise NotFoundError("messages")
        return results
