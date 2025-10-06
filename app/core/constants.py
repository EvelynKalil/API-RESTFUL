# -----------------------------------------
# GLOBAL CONSTANTS — Chat Messages API
# -----------------------------------------

# --- Validation ---
VALID_SENDERS = ["user", "system"]

# --- Pagination ---
DEFAULT_LIMIT = 10
DEFAULT_OFFSET = 0
MAX_LIMIT = 100

# --- Content filtering ---
BANNED_WORDS = ["badword", "offensive", "dummy"]
CENSOR_MASK = "***"

# --- Common field names ---
FIELDS = {
    "MESSAGE_ID": "message_id",
    "SESSION_ID": "session_id",
    "SENDER": "sender",
    "CONTENT": "content",
    "TIMESTAMP": "timestamp",
}

# --- Metadata fields ---
METADATA_FIELDS = {
    "WORD_COUNT": "word_count",
    "CHAR_COUNT": "character_count",
    "PROCESSED_AT": "processed_at",
}

# --- Domain entities ---
ENTITIES = {
    "MESSAGES": "messages",
}

# -----------------------------------------
# DATABASE CONFIGURATION
# -----------------------------------------
SQLITE_PREFIX = "sqlite"
SQLITE_CONNECT_ARGS = {"check_same_thread": False}

DB_TABLE_MESSAGES = "messages"

MESSAGE_ID_MAX_LENGTH = 64
SESSION_ID_MAX_LENGTH = 64
SENDER_MAX_LENGTH = 16

# -----------------------------------------
# ROUTING AND API
# -----------------------------------------
ROUTER_TAG_MESSAGES = "Messages"
ROUTE_PREFIX_MESSAGES = "/api/messages"

# --- Rate limiting ---
RATE_LIMIT_POST_MESSAGES = "3/minute"

# --- Response status ---
STATUS_SUCCESS = "success"
STATUS_ERROR = "error"
STATUS_FIELD = "status"
ERROR_FIELD = "error"

# --- Headers ---
API_KEY_HEADER = "x-api-key"

# --- Example values ---
EXAMPLE_TIMESTAMP = "2025-10-06T00:48:55.204Z"

# -----------------------------------------
# ERROR DEFINITIONS
# -----------------------------------------

# --- Error codes ---
ERROR_CODE_INVALID_FORMAT = "INVALID_FORMAT"
ERROR_CODE_MISSING_FIELD = "MISSING_FIELD"
ERROR_CODE_INVALID_SENDER = "INVALID_SENDER"
ERROR_CODE_DUPLICATE_MESSAGE_ID = "DUPLICATE_MESSAGE_ID"
ERROR_CODE_NOT_FOUND = "NOT_FOUND"
ERROR_CODE_SERVER_ERROR = "SERVER_ERROR"
ERROR_CODE_UNAUTHORIZED = "UNAUTHORIZED"
ERROR_CODE_RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"

# --- Error messages ---
ERROR_MSG_INVALID_FORMAT = "Invalid message format"
ERROR_MSG_MISSING_FIELD = "A required field is missing or empty"
ERROR_MSG_INVALID_SENDER = "Invalid sender value"
ERROR_MSG_DUPLICATE_MESSAGE_ID = "Message ID already exists"
ERROR_MSG_NOT_FOUND = "No results found"
ERROR_MSG_SERVER_ERROR = "Internal server error"
ERROR_MSG_UNAUTHORIZED = "Invalid or missing API key"
ERROR_MSG_RATE_LIMIT_EXCEEDED = "Rate limit exceeded"

# --- Error details ---
ERROR_DETAIL_INVALID_FORMAT = "The provided message does not meet validation rules."
ERROR_DETAIL_MISSING_FIELD = "One or more required fields are missing or blank."
ERROR_DETAIL_INVALID_SENDER = "Allowed values are 'user' or 'system'."
ERROR_DETAIL_DUPLICATE_MESSAGE_ID = "The provided message_id must be unique."
ERROR_DETAIL_NOT_FOUND = "No messages were found for the given criteria."
ERROR_DETAIL_SERVER_ERROR = "Unexpected error while processing request"
ERROR_DETAIL_UNAUTHORIZED = "You must provide a valid x-api-key header."
ERROR_DETAIL_RATE_LIMIT_EXCEEDED = "Too many requests in a short period. Please try again later."

# --- Centralized error mapping ---
ERRORS = {
    ERROR_CODE_INVALID_FORMAT: {
        "code": ERROR_CODE_INVALID_FORMAT,
        "message": ERROR_MSG_INVALID_FORMAT,
        "details": ERROR_DETAIL_INVALID_FORMAT,
    },
    ERROR_CODE_MISSING_FIELD: {
        "code": ERROR_CODE_MISSING_FIELD,
        "message": ERROR_MSG_MISSING_FIELD,
        "details": ERROR_DETAIL_MISSING_FIELD,
    },
    ERROR_CODE_INVALID_SENDER: {
        "code": ERROR_CODE_INVALID_SENDER,
        "message": ERROR_MSG_INVALID_SENDER,
        "details": ERROR_DETAIL_INVALID_SENDER,
    },
    ERROR_CODE_DUPLICATE_MESSAGE_ID: {
        "code": ERROR_CODE_DUPLICATE_MESSAGE_ID,
        "message": ERROR_MSG_DUPLICATE_MESSAGE_ID,
        "details": ERROR_DETAIL_DUPLICATE_MESSAGE_ID,
    },
    ERROR_CODE_NOT_FOUND: {
        "code": ERROR_CODE_NOT_FOUND,
        "message": ERROR_MSG_NOT_FOUND,
        "details": ERROR_DETAIL_NOT_FOUND,
    },
    ERROR_CODE_SERVER_ERROR: {
        "code": ERROR_CODE_SERVER_ERROR,
        "message": ERROR_MSG_SERVER_ERROR,
        "details": ERROR_DETAIL_SERVER_ERROR,
    },
    ERROR_CODE_UNAUTHORIZED: {
        "code": ERROR_CODE_UNAUTHORIZED,
        "message": ERROR_MSG_UNAUTHORIZED,
        "details": ERROR_DETAIL_UNAUTHORIZED,
    },
    ERROR_CODE_RATE_LIMIT_EXCEEDED: {
        "code": ERROR_CODE_RATE_LIMIT_EXCEEDED,
        "message": ERROR_MSG_RATE_LIMIT_EXCEEDED,
        "details": ERROR_DETAIL_RATE_LIMIT_EXCEEDED,
    },
}
