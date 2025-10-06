# Chat Messages API

## Overview

**Chat Messages API** is a RESTful backend service built with **FastAPI** and **Python 3.11+** for managing chat messages in a structured, validated, and secure way.  
It was developed as part of a technical assessment to demonstrate skills in **clean architecture**, **error handling**, **testing**, and **backend best practices**.

The system allows you to:
- Register chat messages (unique ID, session, sender, and content)
- Retrieve messages by session, with pagination, filters, and search
- Automatically generate metadata (word/character count, processed timestamp)
- Validate format, sender, and required fields
- Apply rate limiting per client
- Use authentication via **API Key**
- Run unit and integration tests with **pytest**

---

## Tech Stack

| Component | Technology |
|------------|-------------|
| Language | Python 3.11+ |
| Framework | FastAPI |
| Database | SQLite (SQLAlchemy ORM) |
| Rate Limiting | SlowAPI |
| Validation | Pydantic |
| Testing | Pytest |
| Container | Docker (optional) |

---

## Architecture

The project follows a **Hexagonal (Clean Architecture)** structure, separating responsibilities clearly:

```
app/
 ├── core/              # Configuration, constants, auth, errors, limiter
 ├── domain/            # Entities and repository interfaces
 ├── application/       # Business logic and services
 ├── infrastructure/    # Database, repository implementations
 ├── interfaces/        # Pydantic schemas and FastAPI routers
 ├── main.py            # Application entry point
tests/
 ├── unit/              # Unit tests
 └── integration/       # Integration tests
```

---

## Setup Instructions

### 1️. Clone the repository
```bash
git clone https://github.com/EvelynKalil/API-RESTFUL.git
cd API-RESTFUL
```

### 2️. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3️. Install dependencies
```bash
pip install -r requirements.txt
```

### 4️. Create a .env file
```env
API_KEY=supersecretkey
```

### 5️. Run the app
```bash
uvicorn app.main:app --reload
```

API available at **http://127.0.0.1:8000**

---

## Testing

Run all tests:
```bash
pytest -v
```

Run only unit tests:
```bash
pytest test/unit
```

Run only integration tests:
```bash
pytest test/integration
```

Generate coverage report:
```bash
pytest --cov=app --cov-report=term-missing
```

> In test mode, rate limiting is disabled automatically via `TEST_ENV=true`.

---

## API Documentation

Interactive API docs:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Main Endpoints

#### POST `/api/messages`
Creates a new chat message.

**Request:**
```json
{
  "message_id": "ms001",
  "session_id": "sn001",
  "content": "Hello world!",
  "sender": "user"
}
```

**Response:**
```json
{
  "message_id": "ms001",
  "session_id": "sn001",
  "content": "Hello world!",
  "timestamp": "2025-10-06T00:48:55.204Z",
  "sender": "user",
  "metadata": {
    "word_count": 2,
    "character_count": 12,
    "processed_at": "2025-10-06T00:48:55.204Z"
  }
}
```

#### GET `/api/messages/{session_id}`
Fetch all messages for a session.

**Query parameters:**
| Param | Type | Description |
|--------|------|-------------|
| `limit` | int | Max number of results (default 10) |
| `offset` | int | Offset for pagination |
| `sender` | str | Filter by sender (`user` or `system`) |
| `query` | str | Search by text |

---

## Authentication

All endpoints require the following header:
```
x-api-key: <your_api_key>
```

Example unauthorized response:
```json
{
  "status": "error",
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or missing API key",
    "details": "You must provide a valid x-api-key header"
  }
}
```

---

## Error Handling

All errors return a unified structure:

```json
{
  "status": "error",
  "error": {
    "code": "MISSING_FIELD",
    "message": "A required field is missing or empty",
    "details": "The field 'session_id' is required and cannot be empty"
  }
}
```

| Code | Description | HTTP |
|-------|-------------|------|
| `INVALID_FORMAT` | Invalid message format | 400 |
| `MISSING_FIELD` | Missing required field | 400 |
| `INVALID_SENDER` | Invalid sender | 400 |
| `DUPLICATE_MESSAGE_ID` | Duplicate message ID | 409 |
| `NOT_FOUND` | Resource not found | 404 |
| `UNAUTHORIZED` | Invalid API key | 401 |
| `RATE_LIMIT_EXCEEDED` | Too many requests | 429 |
| `SERVER_ERROR` | Internal server error | 500 |

---

## Success Response Example

```json
{
  "status": "success",
  "data": { ... }
}
```

---

## Docker Setup (optional)

Build the image:
```bash
docker build -t chat-messages-api .
```

Run the container:
```bash
docker run -d -p 8000:8000 --env-file .env chat-messages-api
```

---

## Author

**Evelyn Kalil Rendón**  
Backend Developer — *Chat Messages API*  
[LinkedIn Profile](https://www.linkedin.com/in/evelyn-kalil-167a27170/)

---

## Assessment Checklist

| Requirement | Status |
|--------------|---------|
| RESTful API working | ✅ |
| Validation & error handling | ✅ |
| Unit & integration tests | ✅ |
| Authentication (API Key) | ✅ |
| Rate limiting | ✅ |
| API Documentation | ✅ |
| Docker support | ✅ |
| Complete README | ✅ |
| Propose Infrastructure with IaC (Infrastructure as Code) | 🕒 |
| Add WebSocket endpoint for real-time message updates | 🕒 |
---

