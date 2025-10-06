import pytest
from fastapi.testclient import TestClient
from app.main import app
from test.test_constants import (
    BASE_URL_MESSAGES,
    FIELD_ERROR,
    FIELD_CODE,
    FIELD_MESSAGE_ID,
    FIELD_SESSION_ID,
    FIELD_CONTENT,
    FIELD_SENDER,
    VALID_SENDER,
    INVALID_SENDER,
    CONTENT_VALID,
    CONTENT_SHORT,
    SESSION_ID_VALID,
    SESSION_ID_PAGINATION,
    SESSION_ID_INVALID,
    STATUS_CREATED,
    STATUS_BAD_REQUEST,
    STATUS_NOT_FOUND,
    STATUS_OK,
    ERROR_CODE_INVALID_SENDER,
    ERROR_CODE_NOT_FOUND,
)

client = TestClient(app)


class TestMessageAPI:
    """
    Tests de integración para el endpoint /api/messages
    """

    # --- CONSTANTES PROPIAS DE ESTA CLASE ---
    MESSAGE_ID_VALID = "m100"
    MESSAGE_ID_INVALID_SENDER = "m101"
    LOCAL_SESSION_ID = "s300"  # usada solo en este archivo
    PAGINATION_LIMIT = 2
    PAGINATION_OFFSET = 0

    # --- TESTS ---
    def test_post_message_success(self):
        payload = {
            FIELD_MESSAGE_ID: self.MESSAGE_ID_VALID,
            FIELD_SESSION_ID: SESSION_ID_VALID,
            FIELD_CONTENT: CONTENT_VALID,
            FIELD_SENDER: VALID_SENDER,
        }

        response = client.post(BASE_URL_MESSAGES, json=payload)

        assert response.status_code == STATUS_CREATED
        data = response.json()
        assert data[FIELD_MESSAGE_ID] == self.MESSAGE_ID_VALID
        assert data[FIELD_SESSION_ID] == SESSION_ID_VALID

    def test_post_invalid_sender(self):
        payload = {
            FIELD_MESSAGE_ID: self.MESSAGE_ID_INVALID_SENDER,
            FIELD_SESSION_ID: self.LOCAL_SESSION_ID,
            FIELD_CONTENT: CONTENT_SHORT,
            FIELD_SENDER: INVALID_SENDER,
        }

        response = client.post(BASE_URL_MESSAGES, json=payload)

        assert response.status_code == STATUS_BAD_REQUEST
        data = response.json()
        assert data[FIELD_ERROR][FIELD_CODE] == ERROR_CODE_INVALID_SENDER

    def test_get_messages_with_pagination(self):
        # Crear varios mensajes de prueba
        for i in range(5):
            client.post(BASE_URL_MESSAGES, json={
                FIELD_MESSAGE_ID: f"m{i}",
                FIELD_SESSION_ID: SESSION_ID_PAGINATION,
                FIELD_CONTENT: CONTENT_VALID,
                FIELD_SENDER: VALID_SENDER,
            })

        response = client.get(
            f"{BASE_URL_MESSAGES}/{SESSION_ID_PAGINATION}"
            f"?limit={self.PAGINATION_LIMIT}&offset={self.PAGINATION_OFFSET}&sender={VALID_SENDER}"
        )

        assert response.status_code == STATUS_OK
        assert len(response.json()) == self.PAGINATION_LIMIT

    def test_get_messages_not_found(self):
        response = client.get(f"{BASE_URL_MESSAGES}/{SESSION_ID_INVALID}")

        assert response.status_code == STATUS_NOT_FOUND
        data = response.json()
        assert data[FIELD_ERROR][FIELD_CODE] == ERROR_CODE_NOT_FOUND
