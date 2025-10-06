# Valid senders
VALID_SENDERS = ["user", "system"]

# Default pagination
DEFAULT_LIMIT = 10
DEFAULT_OFFSET = 0  

# Banned words for filtering 
BANNED_WORDS = ["badword", "offensive", "dummy"]

# Error definitions
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
    }
}

