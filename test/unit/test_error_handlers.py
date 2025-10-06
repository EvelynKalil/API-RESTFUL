import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.errors import MissingFieldError
from test.test_constants import (
    BASE_URL_MESSAGES,
    FIELD_ERROR,
    FIELD_CODE,
    FIELD_DETAILS,
    ERROR_CODE_MISSING_FIELD,
    ERROR_CODE_NOT_FOUND,
    ERROR_CODE_INVALID_SENDER,
    ERROR_CODE_DUPLICATE_MESSAGE_ID,
    ERROR_CODE_SERVER,
    STATUS_BAD_REQUEST,
    STATUS_CONFLICT,
    STATUS_NOT_FOUND,
    STATUS_INTERNAL_ERROR,
    STATUS_CREATED,
    VALID_SENDER,
    INVALID_SENDER,
    GENERIC_SERVER_ERROR_MESSAGE,
)

client = TestClient(app)


class TestErrorHandlers:
    """Unit tests for global error handlers."""

    # --- LOCAL CONSTANTS ---
    TEST_FORCE_MISSING_ENDPOINT = "/force-missing"
    TEST_FORCE_ERROR_ENDPOINT = "/force-error"
    SESSION_ID_INVALID = "no-exist"
    SESSION_ID_VALID = "s1"
    FIELD_NAME_MISSING = "session_id"
    INVALID_LIMIT_VALUE = "abc"
    CONTENT_VALID = "hello"
    FORCED_EXCEPTION_MESSAGE = "Unexpected failure!" 

    def test_missing_field_handler(self):
        """Should handle MissingFieldError properly."""
        @app.get(self.TEST_FORCE_MISSING_ENDPOINT)
        def force_missing():
            raise MissingFieldError(self.FIELD_NAME_MISSING)

        response = client.get(self.TEST_FORCE_MISSING_ENDPOINT)
        assert response.status_code == STATUS_BAD_REQUEST
        data = response.json()
        assert data[FIELD_ERROR][FIELD_CODE] == ERROR_CODE_MISSING_FIELD
        assert self.FIELD_NAME_MISSING in data[FIELD_ERROR][FIELD_DETAILS]

    def test_not_found_handler(self):
        """Should return 404 and NOT_FOUND code for non-existing session."""
        response = client.get(f"{BASE_URL_MESSAGES}/{self.SESSION_ID_INVALID}")
        assert response.status_code == STATUS_NOT_FOUND
        data = response.json()
        assert data[FIELD_ERROR][FIELD_CODE] == ERROR_CODE_NOT_FOUND

    def test_invalid_sender_handler(self):
        """Should return 400 and INVALID_SENDER code for invalid sender."""
        response = client.get(f"{BASE_URL_MESSAGES}/{self.SESSION_ID_VALID}?sender={INVALID_SENDER}")
        assert response.status_code == STATUS_BAD_REQUEST
        data = response.json()
        assert data[FIELD_ERROR][FIELD_CODE] == ERROR_CODE_INVALID_SENDER

    def test_request_validation_error(self):
        """Should handle request validation errors (invalid limit)."""
        response = client.get(f"{BASE_URL_MESSAGES}/{self.SESSION_ID_VALID}?limit={self.INVALID_LIMIT_VALUE}")
        assert response.status_code == STATUS_BAD_REQUEST
        data = response.json()
        assert data[FIELD_ERROR][FIELD_CODE] == ERROR_CODE_MISSING_FIELD
        assert "limit" in data[FIELD_ERROR][FIELD_DETAILS]

    def test_duplicate_message_id_handler(self):
        """Should return 409 when trying to create a message with duplicate ID."""
        base_id = str(uuid.uuid4())[:8]
        payload = {
            "message_id": base_id,
            "session_id": self.SESSION_ID_VALID,
            "content": self.CONTENT_VALID,
            "sender": VALID_SENDER,
        }

        r1 = client.post(BASE_URL_MESSAGES, json=payload)
        assert r1.status_code == STATUS_CREATED

        r2 = client.post(BASE_URL_MESSAGES, json=payload)
        assert r2.status_code == STATUS_CONFLICT
        data = r2.json()
        assert data[FIELD_ERROR][FIELD_CODE] == ERROR_CODE_DUPLICATE_MESSAGE_ID

    def test_server_error_handler(self):
        """Should handle unexpected exceptions with SERVER_ERROR response."""
        @app.get(self.TEST_FORCE_ERROR_ENDPOINT)
        def force_error():
            raise RuntimeError(self.FORCED_EXCEPTION_MESSAGE)

        with TestClient(app, raise_server_exceptions=False) as client_no_raise:
            response = client_no_raise.get(self.TEST_FORCE_ERROR_ENDPOINT)

        assert response.status_code == STATUS_INTERNAL_ERROR
        data = response.json()
        assert data[FIELD_ERROR][FIELD_CODE] == ERROR_CODE_SERVER
        assert data[FIELD_ERROR][FIELD_DETAILS] == GENERIC_SERVER_ERROR_MESSAGE
