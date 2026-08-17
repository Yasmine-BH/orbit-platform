import pytest
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_session
from unittest.mock import MagicMock, patch

# Use SQLite in-memory for tests
sqlite_url = "sqlite:///:memory:"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

@pytest.fixture(name="session")
def session_fixture():
    """Create test database and session."""
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
        session.rollback()

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test client with mocked database session and HTTP client."""
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    
    # Mock the HTTP client for interns-api calls
    mock_response = MagicMock()
    mock_response.status_code = 200
    
    with patch("app.routers.tasks.httpx.AsyncClient") as mock_client:
        mock_instance = MagicMock()
        mock_instance.get = MagicMock(return_value=mock_response)
        mock_instance.__aenter__ = MagicMock(return_value=mock_instance)
        mock_instance.__aexit__ = MagicMock(return_value=None)
        mock_client.return_value = mock_instance
        
        client = TestClient(app)
        yield client
    
    app.dependency_overrides.clear()
