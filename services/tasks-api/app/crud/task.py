from sqlmodel import Session, select
from app.models.task import Task
from app.schemas.task import CreateTaskRequest, UpdateTaskRequest


def create_task(session: Session, task: CreateTaskRequest) -> Task:
    """Create a new task."""
    db_task = Task(
        intern_id=task.intern_id,
        title=task.title,
        priority=task.priority,
        due_date=task.due_date,
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def get_task(session: Session, task_id: int) -> Task | None:
    """Get a task by ID."""
    return session.get(Task, task_id)


def list_tasks(session: Session) -> list[Task]:
    """List all tasks."""
    return session.exec(select(Task)).all()


def list_tasks_for_intern(session: Session, intern_id: int) -> list[Task]:
    """List all tasks for a specific intern."""
    return session.exec(
        select(Task).where(Task.intern_id == intern_id)
    ).all()


def update_task(session: Session, task_id: int, task_update: UpdateTaskRequest) -> Task | None:
    """Update an existing task."""
    db_task = session.get(Task, task_id)
    if not db_task:
        return None
    
    db_task.title = task_update.title
    db_task.priority = task_update.priority
    db_task.status = task_update.status
    db_task.due_date = task_update.due_date
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def delete_task(session: Session, task_id: int) -> bool:
    """Delete a task by ID."""
    db_task = session.get(Task, task_id)
    if not db_task:
        return False
    
    session.delete(db_task)
    session.commit()
    return True
