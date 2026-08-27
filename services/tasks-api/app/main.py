# GitHub Actions test
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.config import settings
from app.dependencies import create_db_and_tables
from app.logger import setup_logging
from app.routers import tasks

logger = logging.getLogger("tasks_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    logger.info("Starting tasks-api")
    create_db_and_tables()
    yield
    # Shutdown
    logger.info("Shutting down tasks-api")


app = FastAPI(
    title="tasks-api",
    description="Task management service for ORBIT platform",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure logging
setup_logging()

# Include routers
app.include_router(tasks.router)


@app.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/health/live")
async def liveness() -> dict:
    """Liveness probe for Kubernetes."""
    return {"status": "alive"}


@app.get("/health/ready")
async def readiness() -> dict:
    """Readiness probe for Kubernetes."""
    return {"status": "ready"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Catch-all exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.server_port,
    )
