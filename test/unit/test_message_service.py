import pytest
from datetime import datetime, timezone
from app.application.services.message_service import MessageService
from app.domain.entities.message import Message
from app.domain.repositories.message_repository import MessageRepository
from app.core.errors import MissingFieldError, InvalidSenderError, NotFoundError
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
    def __init__(self, messages=None):
        self.saved = None
        self._messages = messages or []

    def save(self, message: Message) -> Message:
        self.saved = message
        return message

    def get_by_session(self, session_id, limit, offset, sender=None):
        # Simula paginación y filtrado básico por sender
        filtered = [m for m in self._messages if m.session_id == session_id]
        if sender:
            filtered = [m for m in filtered if m.sender == sender]
        return filtered[offset:offset + limit]


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

    # --- CONSTANTS FOR SEARCH TESTS ---
    QUERY_TERM_MATCH = "hello"
    QUERY_TERM_NO_MATCH = "notmatch"
    MESSAGE_ID_1 = "m1"
    MESSAGE_ID_2 = "m2"
    SESSION_ID_SEARCH = "s1"
    CONTENT_MATCH = "hello world"
    CONTENT_NO_MATCH = "bye universe"

    def test_missing_message_id(self, service):
        """Should raise MissingFieldError if message_id is empty."""
        msg = Message(
            message_id=self.MESSAGE_ID_EMPTY,
            session_id=self.SESSION_ID_VALID,
            content=self.SHORT_CONTENT,
            timestamp=datetime.now(timezone.utc),
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
            timestamp=datetime.now(timezone.utc),
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
            timestamp=datetime.now(timezone.utc),
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
            timestamp=datetime.now(timezone.utc),
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
            timestamp=datetime.now(timezone.utc),
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

    def test_get_messages_with_query_filters_results(self):
        """Should return only messages matching the query string."""
        messages = [
            Message(
                message_id=self.MESSAGE_ID_1,
                session_id=self.SESSION_ID_SEARCH,
                content=self.CONTENT_MATCH,
                timestamp=datetime.now(timezone.utc),
                sender="user",
            ),
            Message(
                message_id=self.MESSAGE_ID_2,
                session_id=self.SESSION_ID_SEARCH,
                content=self.CONTENT_NO_MATCH,
                timestamp=datetime.now(timezone.utc),
                sender="system",
            ),
        ]
        repo = FakeRepo(messages)
        service = MessageService(repo)

        results = service.get_messages(
            session_id=self.SESSION_ID_SEARCH,
            limit=10,
            offset=0,
            query=self.QUERY_TERM_MATCH,
        )

        assert len(results) == 1
        assert results[0].content == self.CONTENT_MATCH

    def test_get_messages_query_no_results_raises_notfound(self):
        """Should raise NotFoundError when query yields no results."""
        messages = [
            Message(
                message_id=self.MESSAGE_ID_1,
                session_id=self.SESSION_ID_SEARCH,
                content=self.CONTENT_MATCH,
                timestamp=datetime.now(timezone.utc),
                sender="user",
            ),
        ]
        repo = FakeRepo(messages)
        service = MessageService(repo)

        with pytest.raises(NotFoundError):
            service.get_messages(
                session_id=self.SESSION_ID_SEARCH,
                limit=10,
                offset=0,
                query=self.QUERY_TERM_NO_MATCH,
            )
