from datetime import datetime, timezone
from typing import Optional, List

from app.core.constants import VALID_SENDERS, BANNED_WORDS, CENSOR_MASK
from app.domain.entities.message import Message
from app.domain.repositories.message_repository import MessageRepository
from app.core.errors import InvalidSenderError, MissingFieldError, NotFoundError
from app.core.constants import FIELDS, METADATA_FIELDS, ENTITIES

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
            raise MissingFieldError(FIELDS["MESSAGE_ID"])
        if not message.session_id:
            raise MissingFieldError(FIELDS["SESSION_ID"])
        if not message.sender:
            raise MissingFieldError(FIELDS["SENDER"])
        if message.sender not in VALID_SENDERS:
            raise InvalidSenderError()
        if not message.timestamp:
            message.timestamp = datetime.now(timezone.utc)

    def _filter_content(self, content: str) -> str:
        lowered = content.lower()
        for word in BANNED_WORDS:
            if word in lowered:
                lowered = lowered.replace(word, CENSOR_MASK)
        return lowered

    def _add_metadata(self, content: str) -> dict:
        return {
            METADATA_FIELDS["WORD_COUNT"]: len(content.split()),
            METADATA_FIELDS["CHAR_COUNT"]: len(content),
            METADATA_FIELDS["PROCESSED_AT"]: datetime.now(timezone.utc).isoformat(),
        }

    def get_messages(self,session_id: str,limit: int,offset: int,sender: Optional[str] = None,query: Optional[str] = None) -> List[Message]:
        if sender and sender not in VALID_SENDERS:
            raise InvalidSenderError()
        results = self.repository.get_by_session(session_id, limit, offset, sender)
        if not results:
            raise NotFoundError(ENTITIES["MESSAGES"])
        # Apply simple search filter if 'query' is provided
        if query:
            results = [msg for msg in results if query.lower() in msg.content.lower()]
        if not results:
            raise NotFoundError(ENTITIES["MESSAGES"])

        return results
