import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import src.domain.assessment
import src.domain.clinical
# Import all models to register with SQLAlchemy metadata
import src.domain.identity  # noqa: F401
from src.api.routes import assessment_routes, auth_routes
from src.domain.base import Base
from src.infrastructure.database import engine

# In a real app, use Alembic. For this MVP, we create all tables.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Standalone Clinical Personality Platform",
    description="Secure, clinically-governed API for personality assessment and research.",
    version="0.1.0",
)


# Global Exception Handler to ensure we never leak stack traces or PII
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logging.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal system error occurred. This event has been logged."
        },
    )


app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(assessment_routes.router, tags=["assessments"])
