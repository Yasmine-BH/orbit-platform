from datetime import date
from pydantic import BaseModel, Field
from app.models.task import TaskStatus


class CreateTaskRequest(BaseModel):
    """Request schema for creating a task."""
    intern_id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1, max_length=255)
    priority: str = Field(..., pattern="^(LOW|MEDIUM|HIGH)$")
    due_date: date | None = None


class UpdateTaskRequest(BaseModel):
    """Request schema for updating a task."""
    title: str = Field(..., min_length=1, max_length=255)
    priority: str = Field(..., pattern="^(LOW|MEDIUM|HIGH)$")
    status: TaskStatus
    due_date: date | None = None


class TaskResponse(BaseModel):
    """Response schema for a task."""
    id: int
    intern_id: int
    title: str
    priority: str
    status: TaskStatus
    due_date: date | None = None

    class Config:
        from_attributes = True
