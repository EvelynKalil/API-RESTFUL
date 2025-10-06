from __future__ import annotations

from typing import List, Optional
from datetime import datetime

from sqlalchemy import String, Text, DateTime, JSON, select
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy.exc import IntegrityError

from app.infrastructure.database import Base
from app.domain.entities.message import Message
from app.domain.repositories.message_repository import MessageRepository
from app.core.errors import DuplicateMessageIdError


class MessageModel(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    session_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    sender: Mapped[str] = mapped_column(String(16), nullable=False)

    # Column "metadata" renamed to avoid conflict with SQLAlchemy reserved word
    metadata_json: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)

    def to_domain(self) -> Message:
        return Message(
            message_id=self.message_id,
            session_id=self.session_id,
            content=self.content,
            timestamp=self.timestamp,
            sender=self.sender,
            metadata=self.metadata_json,
        )

    @staticmethod
    def from_domain(m: Message) -> "MessageModel":
        return MessageModel(
            message_id=m.message_id,
            session_id=m.session_id,
            content=m.content,
            timestamp=m.timestamp,
            sender=m.sender,
            metadata_json=m.metadata,
        )


class SQLiteMessageRepository(MessageRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, message: Message) -> Message:
        model = MessageModel.from_domain(message)
        try:
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return model.to_domain()
        except IntegrityError:
            self.db.rollback()
            # Raise our custom exception so the global handler returns proper JSON
            raise DuplicateMessageIdError()

    def get_by_session(
        self, session_id: str, limit: int, offset: int, sender: Optional[str] = None
    ) -> List[Message]:
        stmt = select(MessageModel).where(MessageModel.session_id == session_id)
        if sender:
            stmt = stmt.where(MessageModel.sender == sender)
        stmt = stmt.order_by(MessageModel.timestamp.asc()).offset(offset).limit(limit)
        rows = self.db.execute(stmt).scalars().all()
        return [row.to_domain() for row in rows]
