"""MCP tool for updating tasks."""
from typing import Dict, Any, Optional
from sqlmodel import Session, select
from src.models.todo import TodoTask
from datetime import datetime, timezone


def update_task(
    user_id: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
    db: Session = None
) -> Dict[str, Any]:
    """
    Update a task's properties.

    Args:
        user_id: User ID who owns the task
        task_id: Task ID to update
        title: New title (optional)
        description: New description (optional)
        completed: New completed status (optional)
        db: Database session

    Returns:
        Dict with success status and updated task details
    """
    if not db:
        return {"success": False, "error": "Database session required"}

    try:
        statement = select(TodoTask).where(
            TodoTask.id == task_id,
            TodoTask.user_id == user_id
        )
        task = db.exec(statement).first()

        if not task:
            return {"success": False, "error": "Task not found"}

        # Update fields if provided
        if title is not None:
            task.title = title.strip()
        if description is not None:
            task.description = description.strip() if description else None
        if completed is not None:
            task.completed = completed

        task.updated_at = datetime.now(timezone.utc)

        db.add(task)
        db.commit()
        db.refresh(task)

        return {
            "success": True,
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}
