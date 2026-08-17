from datetime import date
from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient


def test_create_task_success(client: TestClient):
    """Test creating a task when intern exists."""
    payload = {
        "intern_id": 1,
        "title": "Design database schema",
        "priority": "HIGH",
        "due_date": "2026-03-20",
    }
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    assert response.json()["title"] == "Design database schema"


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
