
from sqlalchemy.orm import Session
from app.core.constants import DEFAULT_LIMIT, DEFAULT_OFFSET, ROUTER_TAG_MESSAGES, RATE_LIMIT_POST_MESSAGES
from app.core.auth import verify_api_key
from app.domain.entities.message import Message
from app.application.services.message_service import MessageService
from app.infrastructure.database import get_db
from app.infrastructure.message_repository_impl import SQLiteMessageRepository
from app.interfaces.schemas.message_schema import MessageIn, MessageOut
from app.interfaces.schemas.error_schema import ErrorResponse

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status, Request
from app.core.limiter import limiter

router = APIRouter(tags=[ROUTER_TAG_MESSAGES], dependencies=[Depends(verify_api_key)])

# --- Dependency injection ---
def get_service(db: Session) -> MessageService:
    repo = SQLiteMessageRepository(db)
    return MessageService(repo)


# --- POST /api/messages ---
@router.post(
    "",
    response_model=MessageOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create Message",
    description=(
            "Creates a new message for a specific chat session. "
            "The message must include a unique `message_id`, valid `sender` (`user` or `system`), "
            "and non-empty `content`."
    ),
    responses={
        201: {
            "description": "Message created successfully",
            "model": MessageOut,
        },
        400: {
            "description": "Bad Request (invalid format, sender or missing fields)",
            "model": ErrorResponse,
        },
        401: {"description": "Unauthorized",
              "model": ErrorResponse
        },
        409: {
            "description": "Conflict (duplicate message_id)",
            "model": ErrorResponse,
        },
        500: {
            "description": "Internal Server Error",
            "model": ErrorResponse,
        },
    },
)
@limiter.limit(RATE_LIMIT_POST_MESSAGES)
def create_message(request: Request, payload: MessageIn, db: Session = Depends(get_db)):
    """
    Create a new message for the given session.
    - **message_id**: unique identifier for the message
    - **session_id**: chat session identifier
    - **content**: message body
    - **sender**: must be either `"user"` or `"system"`
    """
    service = get_service(db)

    domain_msg = Message(
        message_id=payload.message_id,
        session_id=payload.session_id,
        content=payload.content,
        timestamp=None,  # will be set by the service if missing
        sender=payload.sender,
    )

    saved = service.process_and_save(domain_msg)
    return MessageOut(**saved.__dict__)


# --- GET /api/messages/{session_id} ---
@router.get(
    "/{session_id}",
    response_model=List[MessageOut],
    summary="List Messages by Session",
    description=(
            "Retrieves all messages associated with a given session ID. "
            "Supports pagination (`limit`, `offset`) and optional filtering by `sender`."
    ),
    responses={
        200: {
            "description": "Successful retrieval of messages",
            "model": List[MessageOut],
        },
        400: {
            "description": "Bad Request (invalid query parameters)",
            "model": ErrorResponse,
        },
        401: {"description": "Unauthorized",
              "model": ErrorResponse
        },
        404: {
            "description": "No messages found for the given session ID",
            "model": ErrorResponse,
        },
        500: {
            "description": "Internal Server Error",
            "model": ErrorResponse,
        },
    },
)
def list_messages(
        session_id: str,
        db: Session = Depends(get_db),
        limit: Optional[int] = Query(DEFAULT_LIMIT, ge=0, le=100, description="Maximum number of results to return"),
        offset: Optional[int] = Query(DEFAULT_OFFSET, ge=0, description="Starting position of results"),
        sender: Optional[str] = Query(None, description="Filter messages by sender (`user` or `system`)"),
        query: Optional[str] = Query(None, description="Search text within message content"),
):
    """
    List all messages belonging to a given session.
    Returns a list of messages ordered by insertion time.
    """
    service = get_service(db)

    results = service.get_messages(
        session_id=session_id, limit=limit, offset=offset, sender=sender, query=query
    )
    return [MessageOut(**m.__dict__) for m in results]
