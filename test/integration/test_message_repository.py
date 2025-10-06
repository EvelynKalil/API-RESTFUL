import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.infrastructure.database import Base, get_db, SessionLocal
from app.infrastructure.message_repository_impl import SQLiteMessageRepository
from app.domain.entities.message import Message
from app.core.errors import DuplicateMessageIdError
from test.test_constants import VALID_SENDER  # Constante global reutilizable


@pytest.fixture
def db_session(tmp_path):
    """Crea una base de datos SQLite temporal para cada test."""
    db_file = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_file}")
    testing_session_local = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = testing_session_local()
    yield session
    session.close()


class TestSQLiteMessageRepository:
    """Tests de integración para SQLiteMessageRepository."""

    SESSION_ID = "s1"
    MESSAGE_ID_1 = "m1"
    MESSAGE_ID_2 = "m2"
    MESSAGE_ID_3 = "m3"
    MESSAGE_ID_4 = "m4"
    CONTENT_USER = "hello"
    CONTENT_SYSTEM = "system message"
    CONTENT_SHORT = "hi" 
    SENDER_SYSTEM = "system"
    LIMIT = 10
    OFFSET = 0

    def test_save_and_get_message(self, db_session):
        repo = SQLiteMessageRepository(db_session)
        msg = Message(
            self.MESSAGE_ID_1,
            self.SESSION_ID,
            self.CONTENT_USER,
            datetime.now(timezone.utc),
            VALID_SENDER,
            None,
        )
        repo.save(msg)

        results = repo.get_by_session(self.SESSION_ID, self.LIMIT, self.OFFSET)
        assert len(results) == 1
        assert results[0].message_id == self.MESSAGE_ID_1

    def test_duplicate_message_id_raises(self, db_session):
        repo = SQLiteMessageRepository(db_session)
        msg = Message(
            self.MESSAGE_ID_2,
            self.SESSION_ID,
            self.CONTENT_SHORT,
            datetime.now(timezone.utc),
            VALID_SENDER,
            None,
        )
        repo.save(msg)
        with pytest.raises(DuplicateMessageIdError):
            repo.save(msg)

    def test_filter_by_sender(self, db_session):
        repo = SQLiteMessageRepository(db_session)
        msg1 = Message(
            self.MESSAGE_ID_3,
            self.SESSION_ID,
            self.CONTENT_USER,
            datetime.now(timezone.utc),
            VALID_SENDER,
            None,
        )
        msg2 = Message(
            self.MESSAGE_ID_4,
            self.SESSION_ID,
            self.CONTENT_SYSTEM,
            datetime.now(timezone.utc),
            self.SENDER_SYSTEM,
            None,
        )
        repo.save(msg1)
        repo.save(msg2)

        results_user = repo.get_by_session(
            self.SESSION_ID, self.LIMIT, self.OFFSET, sender=VALID_SENDER
        )
        assert len(results_user) == 1
        assert results_user[0].sender == VALID_SENDER

        results_system = repo.get_by_session(
            self.SESSION_ID, self.LIMIT, self.OFFSET, sender=self.SENDER_SYSTEM
        )
        assert len(results_system) == 1
        assert results_system[0].sender == self.SENDER_SYSTEM

    def test_get_db_yields_and_closes(self):
        gen = get_db()
        db = next(gen)
        assert db is not None
        assert isinstance(db, SessionLocal().__class__)
        gen.close()
