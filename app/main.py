from fastapi import FastAPI
from app.interfaces.api.messages_router import router as messages_router
from app.core.config import settings
from app.infrastructure.database import Base, engine
from app.core.errors import init_error_handlers

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.API_VERSION,
)

# Register global error handlers
init_error_handlers(app)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(messages_router, prefix=f"{settings.API_PREFIX}/messages", tags=["Messages"])
