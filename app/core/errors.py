from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from slowapi.errors import RateLimitExceeded

from app.core.constants import (
    STATUS_ERROR,
    STATUS_FIELD,
    ERROR_FIELD,
    ERRORS,
    ERROR_CODE_MISSING_FIELD,
    ERROR_CODE_INVALID_SENDER,
    ERROR_CODE_DUPLICATE_MESSAGE_ID,
    ERROR_CODE_NOT_FOUND,
    ERROR_CODE_UNAUTHORIZED,
    ERROR_CODE_SERVER_ERROR,
    ERROR_CODE_RATE_LIMIT_EXCEEDED,
)

# --- Custom exceptions ---
class DuplicateMessageIdError(Exception):
    pass

class InvalidSenderError(Exception):
    pass

class MissingFieldError(Exception):
    def __init__(self, field: str):
        self.field = field

class NotFoundError(Exception):
    def __init__(self, resource: str = "messages"):
        self.resource = resource


def init_error_handlers(app: FastAPI):
    """Register centralized exception handlers."""
    @app.exception_handler(DuplicateMessageIdError)
    async def duplicate_message_id_handler(_, __):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={STATUS_FIELD: STATUS_ERROR, ERROR_FIELD: ERRORS[ERROR_CODE_DUPLICATE_MESSAGE_ID]},
        )

    @app.exception_handler(InvalidSenderError)
    async def invalid_sender_handler(_, __):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={STATUS_FIELD: STATUS_ERROR, ERROR_FIELD: ERRORS[ERROR_CODE_INVALID_SENDER]},
        )

    @app.exception_handler(MissingFieldError)
    async def missing_field_handler(_, exc: MissingFieldError):
        error = ERRORS[ERROR_CODE_MISSING_FIELD].copy()
        error["details"] = f"The field '{exc.field}' is required and cannot be empty"
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={STATUS_FIELD: STATUS_ERROR, ERROR_FIELD: error},
        )

    @app.exception_handler(NotFoundError)
    async def not_found_handler(_, exc: NotFoundError):
        error = ERRORS[ERROR_CODE_NOT_FOUND].copy()
        error["details"] = f"No {exc.resource} were found for the given criteria"
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={STATUS_FIELD: STATUS_ERROR, ERROR_FIELD: error},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(_, exc: RequestValidationError):
        error = ERRORS[ERROR_CODE_MISSING_FIELD].copy()
        first_error = exc.errors()[0]
        field = ".".join(str(x) for x in first_error.get("loc", []) if isinstance(x, str))
        error["details"] = f"The field '{field}' is required and cannot be empty"
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={STATUS_FIELD: STATUS_ERROR, ERROR_FIELD: error},
        )

    @app.exception_handler(Exception)
    async def generic_handler(_, __):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={STATUS_FIELD: STATUS_ERROR, ERROR_FIELD: ERRORS[ERROR_CODE_SERVER_ERROR]},
        )

    @app.exception_handler(HTTPException)
    async def unauthorized_handler(_, exc: HTTPException):
        if exc.status_code == status.HTTP_401_UNAUTHORIZED:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={STATUS_FIELD: STATUS_ERROR, ERROR_FIELD: ERRORS[ERROR_CODE_UNAUTHORIZED]},
            )
        return JSONResponse(
            status_code=exc.status_code,
            content={STATUS_FIELD: STATUS_ERROR, ERROR_FIELD: ERRORS[ERROR_CODE_SERVER_ERROR]},
        )

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(_, exc: RateLimitExceeded):
        error = ERRORS[ERROR_CODE_RATE_LIMIT_EXCEEDED].copy()
        if hasattr(exc, "detail") and exc.detail:
            error["details"] = str(exc.detail)
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={STATUS_FIELD: STATUS_ERROR, ERROR_FIELD: error},
        )
