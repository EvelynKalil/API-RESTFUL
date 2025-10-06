import pytest
from app.interfaces.schemas.error_schema import ErrorResponse
from test.test_constants import (
    FIELD_STATUS,
    FIELD_ERROR,
    FIELD_CODE,
    FIELD_MESSAGE,
    FIELD_DETAILS,
    ERROR_CODE_INVALID_SENDER,
    STATUS_ERROR_RESPONSE,
)


class TestErrorResponseSchema:
    """Unit tests for ErrorResponse Pydantic schema."""

    ERROR_MESSAGE = "Invalid sender value"
    ERROR_DETAILS = "Allowed values are 'user' or 'system'"

    def test_error_response_schema(self):
        """Should validate and serialize ErrorResponse correctly."""
        error_data = {
            FIELD_CODE: ERROR_CODE_INVALID_SENDER,
            FIELD_MESSAGE: self.ERROR_MESSAGE,
            FIELD_DETAILS: self.ERROR_DETAILS,
        }

        response = ErrorResponse(status=STATUS_ERROR_RESPONSE, error=error_data)

        # Basic validations
        assert response.status == STATUS_ERROR_RESPONSE
        assert response.error[FIELD_CODE] == ERROR_CODE_INVALID_SENDER
        assert FIELD_DETAILS in response.error

        # Pydantic serialization
        as_dict = response.dict()
        assert as_dict[FIELD_STATUS] == STATUS_ERROR_RESPONSE
        assert as_dict[FIELD_ERROR][FIELD_MESSAGE] == self.ERROR_MESSAGE
