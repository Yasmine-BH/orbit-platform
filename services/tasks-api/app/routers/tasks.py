import logging
import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.config import settings
from app.dependencies import get_session, get_http_client
from app.models.task import Task
from app.schemas.task import CreateTaskRequest, UpdateTaskRequest, TaskResponse
from app.crud.task import (
    create_task,
    get_task,
    list_tasks,
    list_tasks_for_intern,
    update_task,
    delete_task,
)

logger = logging.getLogger("tasks_api")
router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
async def create_task_endpoint(
    request: CreateTaskRequest,
    session: Session = Depends(get_session),
    http_client: httpx.AsyncClient = Depends(get_http_client),
) -> TaskResponse:
    """
    Create a new task.
    
    Before creating, validates that the intern exists by calling interns-api.
    This demonstrates service-to-service communication and config from environment.
    """
    # Validate intern exists before creating task
    try:
        intern_check_url = f"{settings.interns_api_url}/api/interns/{request.intern_id}/exists"
        response = await http_client.get(intern_check_url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Intern {request.intern_id} not found",
            )
    except httpx.RequestError as e:
        logger.error(f"Failed to validate intern: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Intern service unavailable",
        )

    task = create_task(session, request)
    return TaskResponse.from_orm(task)


@router.get("", response_model=list[TaskResponse])
def list_tasks_endpoint(session: Session = Depends(get_session)) -> list[TaskResponse]:
    """List all tasks."""
    tasks = list_tasks(session)
    return [TaskResponse.from_orm(t) for t in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_endpoint(task_id: int, session: Session = Depends(get_session)) -> TaskResponse:
    """Get a specific task by ID."""
    task = get_task(session, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    return TaskResponse.from_orm(task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    task_id: int,
    request: UpdateTaskRequest,
    session: Session = Depends(get_session),
) -> TaskResponse:
    """Update an existing task."""
    task = update_task(session, task_id, request)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    return TaskResponse.from_orm(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(task_id: int, session: Session = Depends(get_session)) -> None:
    """Delete a task."""
    if not delete_task(session, task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )


@router.get("/intern/{intern_id}", response_model=list[TaskResponse])
def list_intern_tasks_endpoint(
    intern_id: int, session: Session = Depends(get_session)
) -> list[TaskResponse]:
    """List all tasks for a specific intern."""
    tasks = list_tasks_for_intern(session, intern_id)
    return [TaskResponse.from_orm(t) for t in tasks]
