from datetime import date
import pytest
from sqlmodel import Session
from app.models.task import Task, TaskStatus
from app.schemas.task import CreateTaskRequest, UpdateTaskRequest
from app.crud.task import (
    create_task,
    get_task,
    list_tasks,
    update_task,
    delete_task,
)


@pytest.fixture
def sample_task_request():
    return CreateTaskRequest(
        intern_id=1,
        title="Write API documentation",
        priority="HIGH",
        due_date=date(2026, 3, 15),
    )


def test_create_task(session: Session, sample_task_request):
    """Test creating a task."""
    task = create_task(session, sample_task_request)
    assert task.id is not None
    assert task.title == "Write API documentation"
    assert task.priority == "HIGH"
    assert task.status == TaskStatus.PENDING


def test_get_task(session: Session, sample_task_request):
    """Test retrieving a task."""
    created = create_task(session, sample_task_request)
    retrieved = get_task(session, created.id)
    assert retrieved is not None
    assert retrieved.title == "Write API documentation"


def test_get_nonexistent_task(session: Session):
    """Test retrieving a task that doesn't exist."""
    task = get_task(session, 999)
    assert task is None


def test_list_tasks(session: Session, sample_task_request):
    """Test listing all tasks."""
    create_task(session, sample_task_request)
    create_task(session, sample_task_request)
    tasks = list_tasks(session)
    assert len(tasks) == 2


def test_update_task(session: Session, sample_task_request):
    """Test updating a task."""
    created = create_task(session, sample_task_request)
    update = UpdateTaskRequest(
        title="Update API documentation",
        priority="MEDIUM",
        status=TaskStatus.IN_PROGRESS,
    )
    updated = update_task(session, created.id, update)
    assert updated is not None
    assert updated.title == "Update API documentation"
    assert updated.status == TaskStatus.IN_PROGRESS


def test_delete_task(session: Session, sample_task_request):
    """Test deleting a task."""
    created = create_task(session, sample_task_request)
    result = delete_task(session, created.id)
    assert result is True
    retrieved = get_task(session, created.id)
    assert retrieved is None


def test_delete_nonexistent_task(session: Session):
    """Test deleting a task that doesn't exist."""
    result = delete_task(session, 999)
    assert result is False
