import httpx
from sqlmodel import SQLModel, create_engine, Session
from app.config import settings

# Database setup
database_url = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
engine = create_engine(database_url, echo=False)


def create_db_and_tables():
    """Create database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency for database session."""
    with Session(engine) as session:
        yield session


# HTTP client for calling interns-api
async def get_http_client():
    """Dependency for HTTP client."""
    async with httpx.AsyncClient() as client:
        yield client
