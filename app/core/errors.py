from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from slowapi.errors import RateLimitExceeded

# Centralized error definitions
ERRORS = {
    "INVALID_FORMAT": {
        "code": "INVALID_FORMAT",
        "message": "Invalid message format",
        "details": "The provided message does not meet validation rules"
    },
    "MISSING_FIELD": {
        "code": "MISSING_FIELD",
        "message": "A required field is missing or empty",
        "details": "One or more required fields are missing or blank"
    },
    "INVALID_SENDER": {
        "code": "INVALID_SENDER",
        "message": "Invalid sender value",
        "details": f"Allowed values are {', '.join(['user', 'system'])}"
    },
    "DUPLICATE_MESSAGE_ID": {
        "code": "DUPLICATE_MESSAGE_ID",
        "message": "Message ID already exists",
        "details": "The provided message_id must be unique"
    },
    "NOT_FOUND": {
        "code": "NOT_FOUND",
        "message": "No results found",
        "details": "No messages were found for the given criteria"
    },
    "SERVER_ERROR": {
        "code": "SERVER_ERROR",
        "message": "Internal server error",
        "details": "Unexpected error while processing request"
    },
    "UNAUTHORIZED": {
        "code": "UNAUTHORIZED",
        "message": "Invalid or missing API key",
        "details": "You must provide a valid x-api-key header"
    },
    "RATE_LIMIT_EXCEEDED": {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "Rate limit exceeded",
        "details": "Too many requests in a short period. Please try again later."
    }
}


# Custom exceptions (domain/application)
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

# Register error handlers in FastAPI
def init_error_handlers(app: FastAPI):
    @app.exception_handler(DuplicateMessageIdError)
    async def duplicate_message_id_handler(_, __):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"status": "error", "error": ERRORS["DUPLICATE_MESSAGE_ID"]},
        )

    @app.exception_handler(InvalidSenderError)
    async def invalid_sender_handler(_, __):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "error", "error": ERRORS["INVALID_SENDER"]},
        )

    @app.exception_handler(MissingFieldError)
    async def missing_field_handler(_, exc: MissingFieldError):
        error = ERRORS["MISSING_FIELD"].copy()
        error["details"] = f"The field '{exc.field}' is required and cannot be empty"
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "error", "error": error},
        )

    @app.exception_handler(NotFoundError)
    async def not_found_handler(_, exc: NotFoundError):
        error = ERRORS["NOT_FOUND"].copy()
        error["details"] = f"No {exc.resource} were found for the given criteria"
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"status": "error", "error": error},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(_, exc: RequestValidationError):
        error = ERRORS["MISSING_FIELD"].copy()
        first_error = exc.errors()[0]
        field = ".".join(str(x) for x in first_error.get("loc", []) if isinstance(x, str))
        error["details"] = f"The field '{field}' is required and cannot be empty"
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "error", "error": error},
        )

    @app.exception_handler(Exception)
    async def generic_handler(_, __):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "error": ERRORS["SERVER_ERROR"]},
        )

    @app.exception_handler(HTTPException)
    async def unauthorized_handler(_, exc: HTTPException):
        if exc.status_code == status.HTTP_401_UNAUTHORIZED:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": "error", "error": ERRORS["UNAUTHORIZED"]},
            )

        return JSONResponse(
            status_code=exc.status_code,
            content={"status": "error", "error": ERRORS["SERVER_ERROR"]},
        )

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(_, exc: RateLimitExceeded):
        error = ERRORS["RATE_LIMIT_EXCEEDED"].copy()
        if hasattr(exc, "detail") and exc.detail:
            error["details"] = str(exc.detail)
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"status": "error", "error": error},
        )