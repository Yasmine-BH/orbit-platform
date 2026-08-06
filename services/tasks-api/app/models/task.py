from datetime import date
from enum import Enum
from sqlmodel import SQLModel, Field


class TaskStatus(str, Enum):
    """Task status enumeration."""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class Task(SQLModel, table=True):
    """Task model for the database."""
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    intern_id: int = Field(index=True)  # No foreign key — just an integer
    title: str = Field(index=True)
    priority: str  # LOW, MEDIUM, HIGH
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    due_date: date | None = None