from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from app.core.constants import SQLITE_PREFIX, SQLITE_CONNECT_ARGS

"""
Infrastructure module responsible for database initialization and session management.
This defines the SQLAlchemy engine, session factory, and FastAPI dependency for DB access.
"""

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=SQLITE_CONNECT_ARGS if settings.DATABASE_URL.startswith(SQLITE_PREFIX) else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Yield a database session for FastAPI dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
