from datetime import date
from unittest.mock import AsyncMock, patch
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session


@pytest.fixture
def mock_http_client():
    """Mock the HTTP client to avoid calling interns-api during tests."""
    with patch("app.routers.tasks.get_http_client") as mock:
        client = AsyncMock()
        
        async def get_client():
            yield client
        
        mock.return_value = get_client()
        yield client


def test_create_task_success(client: TestClient, mock_http_client):
    """Test creating a task when intern exists."""
    mock_http_client.get.return_value.status_code = 200
    
    payload = {
        "intern_id": 1,
        "title": "Design database schema",
        "priority": "HIGH",
        "due_date": "2026-03-20",
    }
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    assert response.json()["title"] == "Design database schema"


def test_create_task_intern_not_found(client: TestClient, mock_http_client):
    """Test creating a task when intern doesn't exist."""
    mock_http_client.get.return_value.status_code = 404
    
    payload = {
        "intern_id": 999,
        "title": "Design database schema",
        "priority": "HIGH",
    }
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 404


def test_create_task_invalid_priority(client: TestClient):
    """Test creating a task with invalid priority."""
    payload = {
        "intern_id": 1,
        "title": "Some task",
        "priority": "URGENT",  # Invalid
    }
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 422  # Validation error


def test_list_tasks_empty(client: TestClient):
    """Test listing tasks when none exist."""
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_get_task_not_found(client: TestClient):
    """Test retrieving a nonexistent task."""
    response = client.get("/api/tasks/999")
    assert response.status_code == 404


def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_liveness_probe(client: TestClient):
    """Test liveness probe."""
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"


def test_readiness_probe(client: TestClient):
    """Test readiness probe."""
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"
