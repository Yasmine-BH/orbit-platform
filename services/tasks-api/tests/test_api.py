from fastapi.testclient import TestClient
import pytest


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


def test_list_tasks_empty(client: TestClient):
    """Test listing tasks when none exist."""
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_get_task_not_found(client: TestClient):
    """Test retrieving a nonexistent task."""
    response = client.get("/api/tasks/999")
    assert response.status_code == 404

