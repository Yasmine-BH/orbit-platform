import pytest
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_session
from unittest.mock import AsyncMock, patch
import asyncio

# Use SQLite in-memory for tests
sqlite_url = "sqlite:///:memory:"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

# Create tables once
SQLModel.metadata.create_all(engine)

@pytest.fixture(name="session")
def session_fixture():
    """Create test database session."""
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test client with mocked dependencies."""
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    
    # Mock httpx.AsyncClient
    async def mock_get(*args, **kwargs):
        response = AsyncMock()
        response.status_code = 200
        response.json = AsyncMock(return_value={"id": 1, "firstName": "Test"})
        return response
    
    with patch("app.routers.tasks.httpx.AsyncClient") as mock_http:
        mock_instance = AsyncMock()
        mock_instance.get = mock_get
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=None)
        mock_http.return_value = mock_instance
        
        client = TestClient(app)
        yield client
    
    app.dependency_overrides.clear()
