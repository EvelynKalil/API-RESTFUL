from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.interfaces.api.messages_router import router as messages_router
from app.core.config import settings
from app.infrastructure.database import Base, engine
from app.core.errors import init_error_handlers
from app.core.limiter import limiter

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.API_VERSION,
)

app.state.limiter = limiter

# Register global error handlers
init_error_handlers(app)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(messages_router, prefix=f"{settings.API_PREFIX}/messages", tags=["Messages"])
