import pytest
from datetime import datetime, timezone
from app.application.services.message_service import MessageService
from app.domain.entities.message import Message
from app.domain.repositories.message_repository import MessageRepository
from app.core.errors import MissingFieldError, InvalidSenderError
from test.test_constants import (
    VALID_SENDER,
    INVALID_SENDER,
    CONTENT_SHORT,
    CONTENT_WITH_BADWORD,
    FILTERED_WORD_REPLACEMENT,
    METADATA_WORD_COUNT_FIELD,
)


class FakeRepo(MessageRepository):
    """Fake repository used to simulate persistence layer in tests."""
    def __init__(self):
        self.saved = None

    def save(self, message: Message) -> Message:
        self.saved = message
        return message

    def get_by_session(self, session_id, limit, offset, sender=None):
        return []


@pytest.fixture
def service():
    """Fixture providing MessageService with fake repository."""
    return MessageService(FakeRepo())


class TestMessageService:
    """Unit tests for MessageService."""

    # --- LOCAL CONSTANTS ---
    MESSAGE_ID_EMPTY = ""
    MESSAGE_ID_VALID = "m1"
    MESSAGE_ID_BADWORD = "m2"
    MESSAGE_ID_NO_SESSION = "mX"
    MESSAGE_ID_NO_SENDER = "mY"
    MESSAGE_ID_NONE_TIMESTAMP = "mZ"
    SESSION_ID_VALID = "s1"
    SESSION_ID_EMPTY = ""
    BADWORD_CONTENT = CONTENT_WITH_BADWORD
    SHORT_CONTENT = CONTENT_SHORT

    def test_missing_message_id(self, service):
        """Should raise MissingFieldError if message_id is empty."""
        msg = Message(
            message_id=self.MESSAGE_ID_EMPTY,
            session_id=self.SESSION_ID_VALID,
            content=self.SHORT_CONTENT,
            timestamp= datetime.now(timezone.utc),
            sender=VALID_SENDER,
        )
        with pytest.raises(MissingFieldError):
            service.process_and_save(msg)

    def test_invalid_sender(self, service):
        """Should raise InvalidSenderError if sender is not valid."""
        msg = Message(
            message_id=self.MESSAGE_ID_VALID,
            session_id=self.SESSION_ID_VALID,
            content=self.SHORT_CONTENT,
            timestamp= datetime.now(timezone.utc),
            sender=INVALID_SENDER,
        )
        with pytest.raises(InvalidSenderError):
            service.process_and_save(msg)

    def test_adds_metadata_and_filters_badwords(self, service):
        """Should replace bad words and add metadata fields."""
        msg = Message(
            message_id=self.MESSAGE_ID_BADWORD,
            session_id=self.SESSION_ID_VALID,
            content=self.BADWORD_CONTENT,
            timestamp= datetime.now(timezone.utc),
            sender=VALID_SENDER,
        )
        saved = service.process_and_save(msg)
        assert FILTERED_WORD_REPLACEMENT in saved.content
        assert METADATA_WORD_COUNT_FIELD in saved.metadata

    def test_missing_session_id(self, service):
        """Should raise exception if session_id is missing."""
        msg = Message(
            message_id=self.MESSAGE_ID_NO_SESSION,
            session_id=self.SESSION_ID_EMPTY,
            content=self.SHORT_CONTENT,
            timestamp= datetime.now(timezone.utc),
            sender=VALID_SENDER,
        )
        with pytest.raises(Exception) as exc:
            service.process_and_save(msg)
        assert "session_id" in str(exc.value)

    def test_missing_sender(self, service):
        """Should raise exception if sender field is missing."""
        msg = Message(
            message_id=self.MESSAGE_ID_NO_SENDER,
            session_id=self.SESSION_ID_VALID,
            content=self.SHORT_CONTENT,
            timestamp= datetime.now(timezone.utc),
            sender="",
        )
        with pytest.raises(Exception) as exc:
            service.process_and_save(msg)
        assert "sender" in str(exc.value)

    def test_timestamp_auto_set(self, service):
        """Should auto-set timestamp if missing."""
        msg = Message(
            message_id=self.MESSAGE_ID_NONE_TIMESTAMP,
            session_id=self.SESSION_ID_VALID,
            content=self.SHORT_CONTENT,
            timestamp=None,
            sender=VALID_SENDER,
        )
        saved = service.process_and_save(msg)
        assert saved.timestamp is not None
